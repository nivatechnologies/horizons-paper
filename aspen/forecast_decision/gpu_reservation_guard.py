"""Conservative resource guard; reads training and validation receipts only.

GPU RESERVATION WALL UPPER BOUND is not measured GPU time. Process lifetime
includes CPU preparation, CUDA initialization, waits, and GPU ownership.
No frozen scientific recipe, checkpoint rule, or completion receipt is changed.
"""
import argparse
import datetime
import json
import math
import os
from pathlib import Path
import signal
import socket
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "GUARD_STATUS"
CAPS = {"CNN-roll": 18000, "CNN-resp": 18000, "CNN-cost": 36000,
        "CNN-R2": 36000, "CNN-5k": 3600, "CNN-80k": 18000,
        "CNN-20k-s2": 7200, "CNN-20k-s3": 7200, "CNN2-20k": 10800,
        "CNN2-roll": 7200, "CNN2-R2": 25200, "CNN2-cost": 28800}
COUNTS = {"CNN-roll": 10000, "CNN-resp": 10000, "CNN-5k": 5000,
          "CNN-80k": 80000, "CNN-20k-s2": 20000, "CNN-20k-s3": 20000,
          "CNN2-20k": 20000, "CNN2-roll": 10000}
INITIAL = {"CNN-roll": 283638, "CNN-resp": 283639,
           "CNN-cost": 285573, "CNN-R2": 286883}


def boot():
    return time.clock_gettime(time.CLOCK_BOOTTIME)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def load(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".guard-tmp")
    tmp.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    tmp.replace(path)


def process(pid):
    try:
        p = Path(f"/proc/{pid}")
        stat = (p / "stat").read_text().rsplit(") ", 1)[1].split()
        args = (p / "cmdline").read_bytes().replace(b"\0", b" ").decode()
        return dict(pid=pid, state=stat[0], parent=int(stat[1]),
                    start_ticks=int(stat[19]), clock_ticks_per_second=os.sysconf("SC_CLK_TCK"),
                    start_boottime_seconds=int(stat[19]) / os.sysconf("SC_CLK_TCK"),
                    command=args)
    except (FileNotFoundError, ProcessLookupError):
        return None


def selector_charge(directory, now_boottime=None):
    """Each raw checkpoint inference once; R2 zero is folded into step2000 ack."""
    charges = []
    reservations = []
    errors = []
    for path in sorted(directory.glob("validation_*.json")):
        r = load(path)
        value = r.get("checkpoint_validation_gpu_seconds", r["charged_gpu_seconds"])
        if not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
            raise ValueError(f"invalid selector receipt: {path}")
        charges.append(dict(receipt=str(path), seconds=value))
        wall = r.get("selector_reservation_wall_seconds")
        provenance = "measured supervisor SSH wall upper bound; includes setup/lockwait"
        if wall is None:
            checkpoint = directory / path.name.replace("validation_", "checkpoint_")
            try:
                wall = path.stat().st_mtime - checkpoint.stat().st_mtime
            except FileNotFoundError:
                wall = None
            provenance = ("legacy local receipt mtime minus checkpoint JSON mtime; "
                          "includes queuewait; filesystem timestamps, not actual GPU time")
        if (not isinstance(wall, (float, int)) or not math.isfinite(wall)
                or wall < 0 or wall < value):
            errors.append(f"{path.name}: completed selector reservation unavailable/invalid relative to actual charge")
            wall = None
        reservations.append(dict(receipt=str(path), seconds=wall, provenance=provenance))
    active = load(directory / "selection_in_progress.json")
    extra = 0.
    if active and active.get("active"):
        # Selection manager uses this same host's CLOCK_BOOTTIME before remote launch.
        if active.get("clock_host") != socket.gethostname():
            raise ValueError("active selector clock_host mismatch/unavailable")
        extra = max(0., (boot() if now_boottime is None else now_boottime) - active["launch_boottime_seconds"])
        # A committed receipt ends the reservation even before active=false publish.
        ack = directory / f"validation_{int(active['step']):06d}.json"
        if ack.exists():
            extra = 0.
    reservation = None if errors else sum(c["seconds"] for c in reservations)
    return sum(c["seconds"] for c in charges), extra, charges, active, reservation, reservations, errors


def stop_tree(pid, expected_start):
    """Never signal a reused PID or any unrelated service."""
    head = process(pid)
    if not head or head["start_boottime_seconds"] != expected_start:
        return []
    targets = {pid}
    records = [process(int(p.name)) for p in Path("/proc").iterdir() if p.name.isdigit()]
    for _ in range(len(records)):
        new = {r["pid"] for r in records if r and r["parent"] in targets}
        if new <= targets:
            break
        targets |= new
    for sig in [signal.SIGSTOP, signal.SIGKILL]:
        for target in targets:
            try:
                os.kill(target, sig)
            except ProcessLookupError:
                pass
    return sorted(targets)


def run(interval, enforce):
    if socket.gethostname() != "baccus":
        raise RuntimeError("must run on Baccus; process clocks must be host-local")
    OUT.mkdir(exist_ok=True)
    state = load(OUT / "state.json") or {}
    boot_id = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
    snapshot_last = 0.
    previous_alerts = None
    previous_events = None
    while True:
        now_boottime = boot()
        recorded_at = utc()
        rows = {}
        alerts = []
        control = load(ROOT / "runs/campaign_control.json")
        authorization = load(ROOT / "runs/stage2_authorization.json")
        campaign_stop = bool(control and control.get("campaign") == "aspen-forecast-decision"
                             and control.get("execution") == "stop")
        cutoff = datetime.datetime(2026, 10, 8, tzinfo=datetime.timezone.utc)
        two_scale_cutoff = datetime.datetime.now(datetime.timezone.utc) >= cutoff
        if campaign_stop:
            alerts.append("Root campaign control requests stop: " + str(control.get("reason", "")))
        # Admission uses observed selector residency bounds, independently of
        # scientific checkpoint rules. State/cost inference share their own pool.
        selector_pools = {"state": [], "cost": []}
        for candidate in CAPS:
            candidate_directory = ROOT / "runs/training" / candidate
            candidate_values = selector_charge(candidate_directory, now_boottime)
            pool = "cost" if candidate.endswith("cost") else "state"
            selector_pools[pool].extend(r["seconds"] for r in candidate_values[5]
                                        if r["seconds"] is not None)
        for name, cap in CAPS.items():
            directory = ROOT / "runs/training" / name
            pidpath = directory / "detached_worker_pid.txt"
            pid = int(pidpath.read_text()) if pidpath.exists() else INITIAL.get(name)
            if pid is None:
                continue
            current = process(pid)
            old = state.get(name)
            if current and current["state"] != "Z":
                if f"--name {name} " not in current["command"]:
                    alerts.append(f"{name}: PID identity mismatch; no signal sent")
                    continue
                start = current["start_boottime_seconds"]
                if old and (old["start_boottime_seconds"] != start or old["boot_id"] != boot_id):
                    alerts.append(f"{name}: generation changed; review required")
                    continue
                state.setdefault(name, dict(start_boottime_seconds=start, boot_id=boot_id, pid=pid))
                state[name].update(start_ticks=current["start_ticks"],
                                   clock_ticks_per_second=current["clock_ticks_per_second"])
                reservation = now_boottime - start
                alive = True
            elif old:
                old.setdefault("end_boottime_upper_bound_seconds", now_boottime)
                reservation = old["end_boottime_upper_bound_seconds"] - old["start_boottime_seconds"]
                start = old["start_boottime_seconds"]
                alive = False
            else:
                alerts.append(f"{name}: process absent before guard registration; startup reservation unavailable")
                continue
            receipt = load(directory / "training_complete.json")
            actual, active, sources, active_record, selector_reservation, reservation_sources, reservation_errors = selector_charge(directory, now_boottime)
            alerts.extend(f"{name}: {error}" for error in reservation_errors)
            base = 0.
            base_components = None
            if name == "CNN2-R2":
                # Individual R2 includes base; aggregate counts base only once.
                base_row = rows.get("CNN2-20k")
                base = base_row["individual_reservation_upper_bound_seconds"] if base_row else None
                if base_row:
                    base_components = {key: base_row[key] for key in [
                        "process_reservation_wall_upper_bound_seconds",
                        "unique_completed_selector_reservation_upper_bound_seconds",
                        "active_selector_reservation_wall_upper_bound_seconds"]}
                if base is None:
                    alerts.append("CNN2-R2: complete base reservation upper bound unavailable; no actual-timer substitution")
            bound = None if selector_reservation is None or base is None else reservation + selector_reservation + active + base
            remaining = None if bound is None else cap - bound
            pool = selector_pools["cost" if name.endswith("cost") else "state"]
            measured_selector_maximum = max(pool) if pool else None
            admission_reserve = 2 * measured_selector_maximum + 60 if pool else None
            progress = load(directory / "progress.json")
            latest = progress["log"][-1] if progress and progress.get("log") else None
            warning = None
            if latest and name in COUNTS:
                projected = (COUNTS[name] - latest["step"]) * latest["recent_update_seconds"]
                if remaining is not None and projected > remaining:
                    warning = "Measured recent update rate projects required exact count beyond conservative cap"
                    alerts.append(f"{name}: {warning}")
            stopped = old and old.get("stop_requested", False)
            if selector_reservation is None or base is None:
                state[name]["stop_requested"] = True
                state[name]["stop_reason"] = "own or included-base selector residency upper bound unavailable"
                stopped = True
            if campaign_stop or (name.startswith("CNN2-") and two_scale_cutoff):
                state[name]["stop_requested"] = True
                state[name]["stop_reason"] = ("root-issued campaign stop" if campaign_stop
                                              else "chosen operational two-scale evidence cutoff")
                stopped = True
                if alive and name.startswith("CNN2-") and two_scale_cutoff:
                    alerts.append(f"{name}: two-scale unfinished at chosen execution cutoff; report not run")
            if (alive or active > 0) and remaining is not None and remaining <= 60:
                state[name]["stop_requested"] = True
                state[name]["stop_reason"] = "conservative individual reservation cap (60-second guard margin)"
                stopped = True
            row = dict(recorded_at=recorded_at, now_boottime_seconds=now_boottime,
                       start_ticks=state[name].get("start_ticks"),
                       clock_ticks_per_second=state[name].get("clock_ticks_per_second"),
                       model=name, pid=pid, alive=alive,
                       measurement_label="GPU RESERVATION WALL UPPER BOUND",
                       actual_cuda_residency_start="unavailable",
                       start_boottime_seconds=start, process_reservation_wall_upper_bound_seconds=reservation,
                       unique_completed_selector_gpu_seconds=actual,
                       unique_completed_selector_reservation_upper_bound_seconds=selector_reservation,
                       active_selector_reservation_wall_upper_bound_seconds=active,
                       included_base_reservation_seconds=base,
                       included_base_reservation_components=base_components,
                       individual_reservation_upper_bound_seconds=bound,
                       cap_seconds=cap, remaining_conservative_seconds=remaining,
                       completion_receipt_present=receipt is not None,
                       exact_required_updates=COUNTS.get(name), latest_training_progress=latest,
                       feasibility_warning=warning, stop_requested=bool(stopped),
                       selector_admission_measured_maximum_seconds=measured_selector_maximum,
                       selector_admission_reserve_seconds=admission_reserve,
                       selector_admission_rule="two times maximum observed same-kind selector reservation plus 60-second stop margin",
                       selection_allowed=not stopped and remaining is not None and admission_reserve is not None and remaining > admission_reserve,
                       selector_charge_sources=sources, active_selector_record=active_record,
                       selector_reservation_sources=reservation_sources,
                       selector_reservation_errors=reservation_errors,
                       test_access="none; only training/validation receipts",
                       prescribed_completion_confirmed=bool(receipt and (name not in COUNTS or receipt['last_step'] == COUNTS[name])))
            if not alive and not receipt:
                alerts.append(f"{name}: worker death without completion receipt; mandatory requirement unmet if never-cut")
            write(OUT / f"{name}.json", row)
            if stopped and alive and enforce:
                state[name]["signaled_pids"] = stop_tree(pid, start)
                alerts.append(f"{name}: targeted worker stopped ({state[name].get('stop_reason')}); no completion fabricated")
            rows[name] = row
        stage = {"Stage2": 0., "Stage2b": 0.}
        for name, row in rows.items():
            key = "Stage2b" if name.startswith("CNN2-") else "Stage2"
            if row["individual_reservation_upper_bound_seconds"] is None:
                stage[key] = None
            elif stage[key] is not None:
                stage[key] += row["individual_reservation_upper_bound_seconds"] - row["included_base_reservation_seconds"]
        for key, limit in [("Stage2", 144000), ("Stage2b", 72000)]:
            if stage[key] is not None and stage[key] >= limit - 60:
                alerts.append(f"{key}: aggregate conservative ceiling reached; halt all stage workers")
                for name, row in rows.items():
                    if name.startswith("CNN2-") != (key == "Stage2b"):
                        continue
                    state[name]["stop_requested"] = True
                    row.update(stop_requested=True, selection_allowed=False)
                    write(OUT / f"{name}.json", row)
                    if enforce and row["alive"]:
                        stop_tree(row["pid"], row["start_boottime_seconds"])
        write(OUT / "state.json", state)
        summary = dict(recorded_at=recorded_at, now_boottime_seconds=now_boottime, host=socket.gethostname(),
              boot_id=boot_id, stage_reservation_wall_upper_bounds_seconds=stage,
              alerts=alerts, enforce=enforce, status="ALERT" if alerts else "MONITORING",
              root_campaign_control=control,
              stage2_generation_authorized=bool(authorization and authorization.get("authorized")),
              stage1_reading_sha256=authorization.get("stage1_reading_sha256") if authorization else None,
              two_scale_execution_cutoff_utc="2026-10-08T00:00:00Z",
              cutoff_provenance="chosen conservative execution cutoff from WO dates; WO specifies no explicit time",
              scope="training and validation only; no test results accessed",
              accounting="conservative reservation bound, not actual GPU time; no CPU-to-GPU conversion")
        write(OUT / "summary.json", summary)
        events = [(name, row["alive"], row["completion_receipt_present"],
                   row["stop_requested"], len(row["selector_charge_sources"]),
                   (row["active_selector_record"] or {}).get("active"),
                   (row["active_selector_record"] or {}).get("step"))
                  for name, row in sorted(rows.items())]
        if now_boottime - snapshot_last >= 300 or alerts != previous_alerts or events != previous_events:
            stamp = recorded_at.replace(":", "").replace("+", "_")
            snapshot_path = OUT / "snapshots" / f"{stamp}.json"
            snapshot_path.parent.mkdir(exist_ok=True)
            with snapshot_path.open("x") as handle:
                json.dump(dict(summary=summary, models=rows), handle, indent=2, allow_nan=False)
                handle.write("\n")
            snapshot_last = now_boottime
            previous_alerts = alerts
            previous_events = events
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=2)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    run(args.interval, args.enforce)
