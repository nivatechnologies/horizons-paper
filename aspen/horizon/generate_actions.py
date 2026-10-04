"""Run the two WO-mandated blinded CLI invocations, with no extra user text."""
from pathlib import Path
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
PROMPT = (ROOT / "action_prompt.txt").read_text().rstrip("\n")
OUTPUT = ROOT / "step0"
OUTPUT.mkdir(exist_ok=True)
for run in (1, 2):
    answer = OUTPUT / f"answer_{run}.txt"
    if answer.exists():
        raise SystemExit(f"Refusing to overwrite completed invocation {run}")
    with tempfile.TemporaryDirectory(prefix=f"aah-blind-{run}-") as blind:
        args = ["codex", "exec", "--ignore-user-config", "--ignore-rules",
                "--skip-git-repo-check", "--ephemeral", "--sandbox", "read-only",
                "--color", "never", "--json", "-C", blind,
                "--output-last-message", str(answer), "-"]
        print(f"Starting blinded invocation {run}", flush=True)
        with (OUTPUT / f"events_{run}.jsonl").open("w") as events, \
             (OUTPUT / f"stderr_{run}.txt").open("w") as errors:
            result = subprocess.run(args, input=PROMPT, text=True, stdout=events,
                                    stderr=errors, timeout=900)
        (OUTPUT / f"status_{run}.json").write_text(json.dumps({
            "run": run, "returncode": result.returncode,
            "prompt": PROMPT, "argv": args,
            "cli_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
        }, indent=2) + "\n")
        if result.returncode or not answer.exists():
            raise SystemExit(f"Invocation {run} failed: see step0 diagnostics")
        print(f"Completed invocation {run}: {answer.stat().st_size} bytes", flush=True)
