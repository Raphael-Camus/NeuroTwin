"""Export a small committed NeuroTwin workflow snapshot.

Unlike files in artifacts/demo/, this snapshot is intentionally small enough to
keep in Git. It gives reviewers a concrete example of the DSVL contract without
opening generated dashboards or large payloads.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "src"
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from neurotwin.contracts import compact_snapshot, summarize_demo_payload  # noqa: E402
from scripts.run_demo import build_payload  # noqa: E402

OUTPUT_DIR = PROJECT / "examples"
SNAPSHOT_JSON = OUTPUT_DIR / "workflow_snapshot.json"
SNAPSHOT_MD = OUTPUT_DIR / "workflow_snapshot.md"


def write_markdown(snapshot: dict) -> str:
    rows = [
        "| Scenario | BOLD R2 | FC Corr | Objective Delta | Readiness | Top Next Action |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in snapshot["scenarios"]:
        metrics = item["metrics"]
        rows.append(
            "| {name} | {bold:.4f} | {fc:.4f} | {objective:.4f} | {readiness:.2f} | {action} |".format(
                name=item["name"],
                bold=metrics["bold_r2"],
                fc=metrics["fc_corr"],
                objective=metrics["objective_delta"],
                readiness=metrics["readiness_score"],
                action=item["top_next_action"],
            )
        )
    return "\n".join(
        [
            "# NeuroTwin Workflow Snapshot",
            "",
            "I keep this small snapshot in Git to show that NeuroTwin produces concrete metrics, gates, and next actions. The larger dashboard and full JSON payload remain generated artifacts.",
            "",
            *rows,
            "",
            "Contract checks included in this snapshot:",
            "",
            *[f"- {check}" for check in snapshot["contract_checks"]],
            "",
        ]
    )


def main() -> None:
    payload = build_payload()
    summaries = summarize_demo_payload(payload)
    if len(summaries) != 3:
        raise RuntimeError("Expected three baseline scenarios in the workflow snapshot")

    snapshot = compact_snapshot(payload)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_JSON.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SNAPSHOT_MD.write_text(write_markdown(snapshot), encoding="utf-8")
    print(f"Wrote {SNAPSHOT_JSON}")
    print(f"Wrote {SNAPSHOT_MD}")


if __name__ == "__main__":
    main()
