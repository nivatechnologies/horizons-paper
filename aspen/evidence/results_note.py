"""Generate the stopped-at-spec-gate results note without empirical claims."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
overlap = ROOT / "QUERY_OVERLAP.md"
if not (ROOT / "CODEX_QUERIES.md").exists() or not overlap.exists():
    raise SystemExit("Complete blinded Step 0 and overlap before generating the note")
content = (
    "# Aspen evidence-alignment kill test — October 2026\n\n"
    "Status: stopped at the specification gate for affected experimental work. "
    "No empirical PASS or KILL has been measured.\n\n"
    "Branch: `paper/aspen-2026-10-evidence`. Assigned compute: GB10 Spark "
    "`192.168.88.4`, reachable by passwordless SSH and idle at inspection.\n\n"
    "The complete work order and Amendment 1 were audited before execution. "
    "Independent blinded Step 0 is complete; exact prompt and verbatim answer "
    "are committed in `aspen/evidence/CODEX_QUERIES.md`.\n\n"
    + overlap.read_text() + "\n\n" + (ROOT / "AEA_GATE.md").read_text()
)
output = ROOT / "R_Aspen-Evidence-Alignment-Kill-Test-2026-10.md"
output.write_text(content)
print(output)
