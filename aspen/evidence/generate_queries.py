"""Run WO Step 0 once, from an empty directory with exactly the frozen prompt."""
from pathlib import Path
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
prompt = (ROOT / "query_prompt.txt").read_text().rstrip("\n")
out = ROOT / "step0"
out.mkdir(exist_ok=True)
answer = out / "answer.txt"
if answer.exists():
    raise SystemExit("Refusing to overwrite the final blinded selector")
with tempfile.TemporaryDirectory(prefix="aea-blinded-") as blind:
    argv = ["codex", "exec", "--ignore-user-config", "--ignore-rules",
            "--skip-git-repo-check", "--ephemeral", "--sandbox", "read-only",
            "--color", "never", "--json", "-C", blind,
            "--output-last-message", str(answer), "-"]
    with (out / "events.jsonl").open("w") as events, (out / "stderr.txt").open("w") as errors:
        result = subprocess.run(argv, input=prompt, text=True, stdout=events, stderr=errors, timeout=900)
    (out / "status.json").write_text(json.dumps({
        "returncode": result.returncode, "prompt": prompt, "argv": argv,
        "cli_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
    }, indent=2) + "\n")
    if result.returncode or not answer.exists():
        raise SystemExit("Blinded invocation failed; inspect step0 diagnostics")
    (ROOT / "CODEX_QUERIES.md").write_text(
        "# Blinded query selector\n\n## Exact prompt\n\n" + prompt
        + "\n\n## Verbatim answer\n\n" + answer.read_text())
    print("Blinded selector complete", flush=True)
