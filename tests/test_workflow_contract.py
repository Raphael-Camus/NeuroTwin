import json
from pathlib import Path

from scripts.run_demo import build_payload

from neurotwin.contracts import compact_snapshot, summarize_demo_payload, validate_demo_payload

ROOT = Path(__file__).resolve().parents[1]


def test_generated_payload_satisfies_workflow_contract() -> None:
    payload = build_payload()

    validate_demo_payload(payload)
    summaries = summarize_demo_payload(payload)

    assert len(summaries) == 3
    assert all(item.readiness_score >= 0.0 for item in summaries)
    assert all(item.review_gate_count >= 1 for item in summaries)


def test_compact_snapshot_is_reviewable() -> None:
    snapshot = compact_snapshot(build_payload())

    assert snapshot["snapshot_type"] == "curated_workflow_contract"
    assert len(snapshot["scenarios"]) == 3
    assert "next validation packets list required outputs" in snapshot["contract_checks"]


def test_committed_workflow_snapshot_matches_current_payload() -> None:
    committed_snapshot = json.loads((ROOT / "examples" / "workflow_snapshot.json").read_text(encoding="utf-8"))

    assert committed_snapshot == compact_snapshot(build_payload())
