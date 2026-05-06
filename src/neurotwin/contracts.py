"""Workflow contract checks for NeuroTwin demo payloads.

These checks keep the generated DSVL artifacts honest. They do not validate
scientific truth; they validate that a run exposes the fields needed for
review, replay, and next-cycle planning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ContractError(ValueError):
    """Raised when a generated NeuroTwin payload misses a workflow contract."""


@dataclass(frozen=True)
class ScenarioSummary:
    scenario_key: str
    scenario_name: str
    bold_r2: float
    fc_corr: float
    objective_delta: float
    readiness_score: float
    routing: str
    top_action: str
    top_priority: float
    review_gate_count: int


def _require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{path} must be an object")
    return value


def _require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{path} must be a list")
    return value


def _require_number(value: Any, path: str) -> float:
    if not isinstance(value, int | float):
        raise ContractError(f"{path} must be numeric")
    return float(value)


def validate_demo_payload(payload: dict[str, Any]) -> None:
    """Validate the generated demo payload structure.

    A passing payload has enough information for a reviewer or downstream
    agent to inspect the DSVL cycle without opening the HTML dashboard.
    """

    root = _require_mapping(payload, "payload")
    for key in [
        "project",
        "networks",
        "scenarios",
        "evidence_cards",
        "agent_skill_registry",
        "next_validation_packets",
        "trace",
    ]:
        if key not in root:
            raise ContractError(f"payload.{key} is required")

    networks = _require_list(root["networks"], "payload.networks")
    if len(networks) < 4:
        raise ContractError("payload.networks must contain multiple brain networks")

    evidence_cards = _require_list(root["evidence_cards"], "payload.evidence_cards")
    if not evidence_cards:
        raise ContractError("payload.evidence_cards must not be empty")

    skills = _require_list(root["agent_skill_registry"], "payload.agent_skill_registry")
    skill_stages = {str(item.get("stage")) for item in skills if isinstance(item, dict)}
    for expected_stage in {"Read", "Prepare", "Build", "Compute", "Validate", "Learn"}:
        if expected_stage not in skill_stages:
            raise ContractError(f"agent skill stage {expected_stage!r} is missing")

    scenarios = _require_mapping(root["scenarios"], "payload.scenarios")
    packets = _require_mapping(root["next_validation_packets"], "payload.next_validation_packets")
    if set(scenarios) != set(packets):
        raise ContractError("scenario keys and next_validation_packets keys must match")

    for scenario_key, scenario in scenarios.items():
        scenario_path = f"payload.scenarios.{scenario_key}"
        scenario_obj = _require_mapping(scenario, scenario_path)
        metrics = _require_mapping(scenario_obj.get("metrics"), f"{scenario_path}.metrics")
        ledger = _require_mapping(scenario_obj.get("validation_ledger"), f"{scenario_path}.validation_ledger")
        learning = _require_mapping(scenario_obj.get("learning_update"), f"{scenario_path}.learning_update")

        for metric in ["bold_r2", "fc_corr", "objective_delta"]:
            _require_number(metrics.get(metric), f"{scenario_path}.metrics.{metric}")

        gates = _require_list(ledger.get("gates"), f"{scenario_path}.validation_ledger.gates")
        gate_names = {str(item.get("gate")) for item in gates if isinstance(item, dict)}
        for gate_name in ["Signal fidelity", "FC reproducibility", "Objective effect", "External evidence"]:
            if gate_name not in gate_names:
                raise ContractError(f"{scenario_path} missing ledger gate {gate_name!r}")

        review_queue = _require_list(ledger.get("review_queue"), f"{scenario_path}.validation_ledger.review_queue")
        if not review_queue:
            raise ContractError(f"{scenario_path} must expose at least one review task")

        ranked_actions = _require_list(
            learning.get("ranked_actions"), f"{scenario_path}.learning_update.ranked_actions"
        )
        if not ranked_actions:
            raise ContractError(f"{scenario_path} must expose ranked next actions")

        packet = _require_mapping(packets.get(scenario_key), f"payload.next_validation_packets.{scenario_key}")
        required_outputs = _require_list(
            packet.get("required_outputs"), f"payload.next_validation_packets.{scenario_key}.required_outputs"
        )
        if len(required_outputs) < 3:
            raise ContractError(f"payload.next_validation_packets.{scenario_key} must list concrete required outputs")


def summarize_demo_payload(payload: dict[str, Any]) -> list[ScenarioSummary]:
    """Return compact scenario summaries for examples and README snippets."""

    validate_demo_payload(payload)
    summaries: list[ScenarioSummary] = []
    for scenario_key, scenario in payload["scenarios"].items():
        metrics = scenario["metrics"]
        ledger_summary = scenario["validation_ledger"]["summary"]
        ranked_actions = scenario["learning_update"]["ranked_actions"]
        top_action = ranked_actions[0]
        review_gate_count = sum(1 for gate in scenario["validation_ledger"]["gates"] if gate["status"] == "review")
        summaries.append(
            ScenarioSummary(
                scenario_key=scenario_key,
                scenario_name=scenario["name"],
                bold_r2=float(metrics["bold_r2"]),
                fc_corr=float(metrics["fc_corr"]),
                objective_delta=float(metrics["objective_delta"]),
                readiness_score=float(ledger_summary["readiness_score"]),
                routing=str(ledger_summary["routing"]),
                top_action=str(top_action["action"]),
                top_priority=float(top_action["priority_score"]),
                review_gate_count=review_gate_count,
            )
        )
    return summaries


def compact_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    """Build a small committed snapshot that proves the workflow is concrete."""

    summaries = summarize_demo_payload(payload)
    return {
        "project": payload["project"],
        "snapshot_type": "curated_workflow_contract",
        "scenarios": [
            {
                "key": item.scenario_key,
                "name": item.scenario_name,
                "metrics": {
                    "bold_r2": item.bold_r2,
                    "fc_corr": item.fc_corr,
                    "objective_delta": item.objective_delta,
                    "readiness_score": item.readiness_score,
                },
                "top_next_action": item.top_action,
                "top_priority": item.top_priority,
                "review_gate_count": item.review_gate_count,
                "routing": item.routing,
            }
            for item in summaries
        ],
        "contract_checks": [
            "scenario metrics are present",
            "validation ledger gates are present",
            "review queue is present",
            "ranked next actions are present",
            "next validation packets list required outputs",
        ],
    }
