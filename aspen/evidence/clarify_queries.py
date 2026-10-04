"""Record the WO-permitted single clarification of forcing convention."""
from pathlib import Path
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "step0"
question = (
    "The mandated reused truth solver applies velocity body force A sin(4y) e_x, "
    "so its vorticity forcing is -4A cos(4y); the query lead is h=0.5/lambda(theta) "
    "after the last observation at each test point. For this convention, what are "
    "your final four exact scalar query formulas, retaining your four chosen quantities?"
)
answer = OUT / "clarification_answer.txt"
if answer.exists():
    raise SystemExit("Refusing a second clarification")
prompt = (
    "Original prompt:\n" + (ROOT / "query_prompt.txt").read_text()
    + "\nYour verbatim answer:\n" + (OUT / "answer.txt").read_text()
    + "\nSingle clarifying question:\n" + question
)
(OUT / "clarification_question.txt").write_text(question + "\n")
with tempfile.TemporaryDirectory(prefix="aea-clarify-") as blind:
    argv = ["codex", "exec", "--ignore-user-config", "--ignore-rules",
            "--skip-git-repo-check", "--ephemeral", "--sandbox", "read-only",
            "--color", "never", "--json", "-C", blind,
            "--output-last-message", str(answer), "-"]
    with (OUT / "clarification_events.jsonl").open("w") as events, (OUT / "clarification_stderr.txt").open("w") as errors:
        result = subprocess.run(argv, input=prompt, text=True, stdout=events, stderr=errors, timeout=900)
    (OUT / "clarification_status.json").write_text(json.dumps({
        "returncode": result.returncode, "question": question, "argv": argv,
    }, indent=2) + "\n")
    if result.returncode or not answer.exists():
        raise SystemExit("Clarification failed; inspect diagnostics")
    with (ROOT / "CODEX_QUERIES.md").open("a") as record:
        record.write("\n\n## Single clarifying question\n\n" + question
                     + "\n\n## Verbatim clarification answer\n\n" + answer.read_text())
    print("Single clarification complete", flush=True)
