"""Retain exact final responses and summarize blinded invocation provenance."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
prompt = (ROOT / "action_prompt.txt").read_text().rstrip("\n")
parts = ["# Blinded action sets: exact WO prompt and verbatim Codex answers\n\n",
         "Generated before any new experimental data. No final action-set choice has been made.\n\n"]
for run in (1, 2):
    status = json.loads((ROOT / "step0" / f"status_{run}.json").read_text())
    assert status["returncode"] == 0 and status["prompt"] == prompt
    answer = (ROOT / "step0" / f"answer_{run}.txt").read_text()
    events = [json.loads(s) for s in (ROOT / "step0" / f"events_{run}.jsonl").read_text().splitlines()]
    messages = [e["item"]["text"] for e in events
                if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "agent_message"]
    assert messages and messages[-1].rstrip("\n") == answer.rstrip("\n")
    tools = [e["item"]["type"] for e in events if e.get("type") == "item.completed"
             and e.get("item", {}).get("type") != "agent_message"]
    parts += [f"## Invocation {run}\n\nCLI: {status['cli_version']}. Empty isolated directory, read-only sandbox, ignored user configuration and policy rules. Completed tools: {tools}.\n\n",
              "### Exact prompt\n\n```text\n", prompt, "\n```\n\n"]
    for message in messages[:-1]:
        parts += ["### Verbatim preliminary assistant message\n\n", message, "\n\n"]
    parts += ["### Verbatim final answer\n\n", answer, "\n\n"]
parts += ["\n", (ROOT / "ACTION_OVERLAP.md").read_text()]
(ROOT / "CODEX_ACTIONS.md").write_text("".join(parts).rstrip() + "\n")
print(ROOT / "CODEX_ACTIONS.md")
