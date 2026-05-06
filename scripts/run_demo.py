"""Generate NeuroTwin demo artifacts.

Run:
    python scripts/run_demo.py

Outputs are written to artifacts/demo/.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from textwrap import dedent

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from neurotwin.core import (
    NETWORKS,
    SCENARIOS,
    effective_connectivity_from_surrogate,
    fit_surrogate,
    functional_connectivity,
    predict_surrogate,
    r2_score,
    simulate,
    summarize_candidate,
)


ROOT = PROJECT
DIST = ROOT / "artifacts" / "demo"

PORTFOLIO_WEIGHTS = {
    "fidelity": 0.32,
    "objective_alignment": 0.22,
    "novelty": 0.18,
    "feasibility": 0.16,
    "risk_control": 0.12,
}

PUBLIC_VALIDATION_BRIDGE = {
    "principle": "Review gates should create concrete public-data validation tasks before downstream claims are made.",
    "tiers": [
        {
            "name": "OpenNeuro BIDS smoke test",
            "dataset": "OpenNeuro",
            "access": "public BIDS datasets with validation tooling",
            "task": "Run the same ROI extraction, surrogate fit and Validation Ledger on one small task-fMRI dataset.",
            "success_gate": "Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated.",
            "url": "https://docs.openneuro.org/",
        },
        {
            "name": "HCP task-fMRI transfer check",
            "dataset": "Human Connectome Project",
            "access": "registered access for high-quality task and resting fMRI resources",
            "task": "Check whether the surrogate and acquisition policy remain stable on HCP task contrasts.",
            "success_gate": "Subject-split metrics and behavior-alignment signals are reproducible across tasks.",
            "url": "https://icb.humanconnectome.org/hcp-protocols-ya-task-fmri",
        },
        {
            "name": "ABCD cohort stress test",
            "dataset": "ABCD Study",
            "access": "controlled access; availability must be checked before use",
            "task": "Use large-cohort developmental MRI only when approved access and governance are clear.",
            "success_gate": "Generalization, site effects and QC gates are reported separately from model score.",
            "url": "https://abcdstudy.org/scientists/data-sharing/",
        },
    ],
}

LITERATURE_BACKBONE = [
    {
        "theme": "Agentic AI4S infrastructure",
        "source": "Bohrium + SciMaster",
        "url": "https://arxiv.org/abs/2512.20469",
        "insight": "Scientific agents need stable tool interfaces, recorded execution traces, reusable capabilities and governance hooks.",
        "project_move": "Frame NeuroTwin as an agent-ready virtual experiment capability with contracts, trace memory and validation gates.",
    },
    {
        "theme": "Personalised brain simulation",
        "source": "The Virtual Brain on EBRAINS",
        "url": "https://ebrains.eu/data-tools-services/tools/the-virtual-brain",
        "insight": "MRI-derived structural and functional data can support personalised brain network model creation and multiscale simulation.",
        "project_move": "Position the demo as a lightweight surrogate layer that can later interoperate with TVB-style connectome and neural mass modeling.",
    },
    {
        "theme": "Self-driving lab metrics",
        "source": "Nature Communications SDL metrics and accessibility papers",
        "url": "https://www.nature.com/articles/s41467-024-45569-5",
        "insight": "Closed-loop scientific systems need explicit autonomy level, operational lifetime, repeatability, metadata and reproducibility metrics.",
        "project_move": "Add autonomy/readiness scoring and require each validation packet to record data, model, metrics and operator assumptions.",
    },
    {
        "theme": "Hypothesis generation agents",
        "source": "AI co-scientist",
        "url": "https://arxiv.org/abs/2502.18864",
        "insight": "Generate-debate-evolve workflows can turn literature-backed evidence into testable scientific hypotheses under human objectives.",
        "project_move": "Keep literature mining as Design-layer evidence cards, then route hypotheses through surrogate simulation and review gates.",
    },
    {
        "theme": "Neuroimaging validation standards",
        "source": "OpenNeuro, BIDS Validator, HCP and ABCD",
        "url": "https://docs.openneuro.org/packages/openneuro-cli.html",
        "insight": "Public neuroimaging validation requires BIDS-compatible data access, task/behavior context, QC, motion and site/scanner checks.",
        "project_move": "Extend public validation runbooks with BIDS checks, ROI QC, subject split metrics, behavior endpoints and cohort-stress constraints.",
    },
    {
        "theme": "DBTL loop engineering",
        "source": "DBTL cycle reviews",
        "url": "https://link.springer.com/article/10.1007/s13721-024-00455-4",
        "insight": "Design-Build-Test-Learn systems become useful when each cycle preserves decisions, measurements and model updates as reusable loop memory.",
        "project_move": "Map NeuroTwin's DSVL stages to evidence cards, virtual runs, validation packets and learning-memory updates.",
    },
    {
        "theme": "Generative digital twins",
        "source": "Neuroimaging digital twin reviews",
        "url": "https://academic.oup.com/cercor/article/35/1/bhae462/7930283",
        "insight": "Brain digital twins are stronger when they move from descriptive maps toward generative models that can test counterfactual interventions.",
        "project_move": "Treat effective-connectivity perturbation and next-run acquisition as counterfactual dry experiments under explicit validation gates.",
    },
]


AGENT_SKILL_REGISTRY = [
    {
        "skill_id": "EvidenceCardBuilder",
        "stage": "Read",
        "purpose": "Convert literature, method notes and platform standards into structured Design inputs.",
        "inputs": ["research source", "method claim", "validation standard"],
        "outputs": ["evidence_cards.json", "evidence_card_schema.md"],
        "gate": "Every claim must map to a scenario input, surrogate requirement, validation gate, risk or next action.",
        "artifact": "artifacts/demo/evidence_cards.json",
    },
    {
        "skill_id": "BIDSValidationPlanner",
        "stage": "Prepare",
        "purpose": "Turn review gates into public fMRI validation protocol fields before model scores are interpreted.",
        "inputs": ["OpenNeuro/HCP/ABCD tier", "scenario objective", "operator protocol"],
        "outputs": ["public_validation_protocol_template.md", "public_validation_manifest.json"],
        "gate": "BIDS, preprocessing, ROI, split and QC assumptions must be recorded.",
        "artifact": "artifacts/demo/public_validation_protocol_template.md",
    },
    {
        "skill_id": "ROITimeSeriesExtractor",
        "stage": "Build",
        "purpose": "Convert validated imaging data into atlas-aligned ROI time series and QC tables.",
        "inputs": ["BIDS dataset", "atlas contract", "confounds table"],
        "outputs": ["ROI time series", "ROI QC table", "motion/site summary"],
        "gate": "Minimum timepoints, missing ROI threshold and motion review must pass or be marked for repair.",
        "artifact": "future public-validation workspace",
    },
    {
        "skill_id": "SurrogateTrainer",
        "stage": "Compute",
        "purpose": "Fit the surrogate brain dynamics model under fixed split and seed policy.",
        "inputs": ["ROI time series", "scenario objective", "subject split"],
        "outputs": ["BOLD prediction", "functional connectivity", "model metrics"],
        "gate": "Signal fidelity and FC reproducibility gates are updated.",
        "artifact": "artifacts/demo/demo_data.json",
    },
    {
        "skill_id": "PerturbationSimulator",
        "stage": "Compute",
        "purpose": "Run counterfactual virtual perturbations and estimate effective-connectivity response.",
        "inputs": ["trained surrogate", "candidate perturbation", "objective function"],
        "outputs": ["virtual EC map", "objective delta", "candidate policy score"],
        "gate": "Perturbation budget and objective-effect gates are updated.",
        "artifact": "artifacts/demo/brain_twin_lab.html",
    },
    {
        "skill_id": "ValidationLedgerWriter",
        "stage": "Validate",
        "purpose": "Record pass, watch, review and hold decisions for scientific readiness.",
        "inputs": ["metrics", "public validation bridge", "operator notes"],
        "outputs": ["validation_ledger.md", "review queue"],
        "gate": "Review items must become concrete validation tasks.",
        "artifact": "artifacts/demo/validation_ledger.md",
    },
    {
        "skill_id": "AcquisitionPolicyOptimizer",
        "stage": "Learn",
        "purpose": "Rank next simulations using uncertainty, FC gap, objective signal, feasibility and risk control.",
        "inputs": ["validation ledger", "negative evidence", "policy weights"],
        "outputs": ["ranked next actions", "multi-objective portfolio"],
        "gate": "Weak actions remain in negative evidence for future routing.",
        "artifact": "artifacts/demo/acquisition_policy.md",
    },
    {
        "skill_id": "NextValidationPacketBuilder",
        "stage": "Learn",
        "purpose": "Package the next executable validation step as a decision-ready object for the next loop.",
        "inputs": ["scenario state", "evidence cards", "agent skill route", "protocol template"],
        "outputs": ["next_validation_packet.json", "next_validation_packet.md"],
        "gate": "Packet must include objective, evidence, route, protocol files, required outputs and decision rule.",
        "artifact": "artifacts/demo/next_validation_packet.json",
    },
]

AGENT_LOOP_ROUTE = {
    "principle": "An AI4S agent should route one scientific question through Read, Prepare, Build, Compute, Validate and Learn, while preserving trace and decision memory.",
    "steps": [
        {
            "step": "Read",
            "agent_action": "Mine papers, standards and internal method cards into structured evidence.",
            "memory": "Evidence cards and risk notes.",
        },
        {
            "step": "Prepare",
            "agent_action": "Select a public validation tier and fill the protocol fields needed before scoring.",
            "memory": "Dataset contract, BIDS/QC state and operator assumptions.",
        },
        {
            "step": "Build",
            "agent_action": "Create ROI time series and feature context under a fixed split policy.",
            "memory": "Data card, ROI QC and split file.",
        },
        {
            "step": "Compute",
            "agent_action": "Train surrogate dynamics and run virtual perturbation experiments.",
            "memory": "Model metrics, FC/EC response and objective delta.",
        },
        {
            "step": "Validate",
            "agent_action": "Write pass, watch, review and hold decisions into a validation ledger.",
            "memory": "Review queue and escalation rule.",
        },
        {
            "step": "Learn",
            "agent_action": "Rank next actions, preserve negative evidence and emit a next validation packet.",
            "memory": "Acquisition portfolio and next-cycle packet.",
        },
    ],
}


def build_evidence_cards() -> list[dict]:
    return [
        {
            "card_id": "EC-001",
            "source_theme": "Agentic AI4S infrastructure",
            "evidence_claim": "A scientific capability should expose contracts, trace and validation gates.",
            "design_input": "Require every NeuroTwin run to declare inputs, outputs, gates and trace identifiers.",
            "surrogate_requirement": "Package the surrogate perturbation workflow as a callable tool with replayable artifacts.",
            "validation_gate": "Capability card and experiment trace must be generated for each run.",
            "risk_to_track": "Unclear interface boundaries can make the project look like an isolated demo.",
            "next_action": "Keep capability card, trace and final submission index synced with generated outputs.",
            "source_url": "https://arxiv.org/abs/2512.20469",
        },
        {
            "card_id": "EC-002",
            "source_theme": "Personalised brain simulation",
            "evidence_claim": "MRI-derived data can support individualized brain network simulation.",
            "design_input": "Represent fMRI/structural MRI as subject-specific context for future surrogate fitting.",
            "surrogate_requirement": "Leave a path from ROI surrogate dynamics to TVB-style connectome and neural mass models.",
            "validation_gate": "Record atlas, connectome, ROI extraction and subject split assumptions.",
            "risk_to_track": "Synthetic ROI data can hide connectome and preprocessing limitations.",
            "next_action": "Add public fMRI smoke test before claiming stronger phenotype simulation.",
            "source_url": "https://ebrains.eu/data-tools-services/tools/the-virtual-brain",
        },
        {
            "card_id": "EC-003",
            "source_theme": "Self-driving lab metrics",
            "evidence_claim": "Closed-loop systems need repeatability, metadata and autonomy/readiness records.",
            "design_input": "Treat each validation packet as a loop-memory object with dataset, model and operator metadata.",
            "surrogate_requirement": "Persist acquisition policy weights, negative evidence and validation readiness fields.",
            "validation_gate": "Runbook must include QC, endpoint, split and repeatability requirements.",
            "risk_to_track": "A high model score without operational metadata can be misleading.",
            "next_action": "Promote motion/site/scanner and behavior endpoint checks into public validation artifacts.",
            "source_url": "https://www.nature.com/articles/s41467-024-45569-5",
        },
        {
            "card_id": "EC-004",
            "source_theme": "Hypothesis generation agents",
            "evidence_claim": "Literature-backed hypotheses need structured debate, evolution and human objective checks.",
            "design_input": "Use literature parsing to generate evidence cards instead of free-text method notes.",
            "surrogate_requirement": "Each card must map to a scenario objective, candidate perturbation or validation gate.",
            "validation_gate": "Human review keeps hypothesis quality and translational claims bounded.",
            "risk_to_track": "Automated literature mining can overstate novelty or biological plausibility.",
            "next_action": "Use evidence-card schema as the interface between literature mining and Design.",
            "source_url": "https://arxiv.org/abs/2502.18864",
        },
        {
            "card_id": "EC-005",
            "source_theme": "Neuroimaging validation standards",
            "evidence_claim": "Public neuroimaging validation depends on BIDS compliance, QC and cohort-aware splits.",
            "design_input": "Select OpenNeuro/HCP/ABCD validation tiers based on task fit, access and governance.",
            "surrogate_requirement": "Calculate BOLD R2 and FC corr only after BIDS, ROI and motion QC are recorded.",
            "validation_gate": "Manifest must include BIDS validation, ROI QC, motion/site/scanner and endpoint fields.",
            "risk_to_track": "Scanner/site confounds can appear as model generalization.",
            "next_action": "Prepare OpenNeuro P1 smoke-test packet and keep controlled-access cohorts as later tiers.",
            "source_url": "https://docs.openneuro.org/packages/openneuro-cli.html",
        },
        {
            "card_id": "EC-006",
            "source_theme": "DBTL loop engineering",
            "evidence_claim": "Closed-loop discovery benefits when each cycle returns structured learning memory.",
            "design_input": "Map DSVL to DBTL/DMTA language for AI4S reviewers: design, virtual build/run, validate/test, learn/analyze.",
            "surrogate_requirement": "Keep negative evidence and acquisition portfolio as first-class loop outputs.",
            "validation_gate": "Next-run plan must cite what was learned from current pass/watch/review gates.",
            "risk_to_track": "A loop without persisted weak results repeats low-value experiments.",
            "next_action": "Add evidence-card JSON and schema to the submission package.",
            "source_url": "https://link.springer.com/article/10.1007/s13721-024-00455-4",
        },
        {
            "card_id": "EC-007",
            "source_theme": "Generative digital twins",
            "evidence_claim": "Digital twins become more useful when they can simulate counterfactual interventions.",
            "design_input": "Define each perturbation as a counterfactual dry experiment with a measurable objective.",
            "surrogate_requirement": "Report virtual effective connectivity and acquisition-driven next perturbation choices.",
            "validation_gate": "Counterfactual claims require external evidence review before translational interpretation.",
            "risk_to_track": "Virtual intervention response can reflect model bias instead of biology.",
            "next_action": "Keep perturbation budget, external evidence and expert review visible in the Validation Ledger.",
            "source_url": "https://academic.oup.com/cercor/article/35/1/bhae462/7930283",
        },
    ]


def build_next_validation_packets(scenarios: dict, evidence_cards: list[dict]) -> dict:
    card_lookup = {card["card_id"]: card for card in evidence_cards}
    default_card_ids = ["EC-001", "EC-002", "EC-003", "EC-005", "EC-006", "EC-007"]
    skill_route = [item["skill_id"] for item in AGENT_SKILL_REGISTRY]
    packets = {}
    for key, scenario in scenarios.items():
        ledger = scenario["validation_ledger"]
        summary = ledger["summary"]
        learning = scenario["learning_update"]
        top = learning["ranked_actions"][0]
        review_task = ledger["review_queue"][0] if ledger["review_queue"] else build_public_review_queue()[0]
        metric = scenario["metrics"]
        packets[key] = {
            "packet_id": f"NVP-{key}",
            "scenario": scenario["name"],
            "objective": scenario["objective"],
            "why_now": "External-evidence review is visible, the dry run is traceable and the next action has a ranked acquisition score.",
            "linked_evidence_cards": [
                {
                    "card_id": card_id,
                    "theme": card_lookup[card_id]["source_theme"],
                    "gate": card_lookup[card_id]["validation_gate"],
                }
                for card_id in default_card_ids
            ],
            "agent_skill_route": skill_route,
            "public_validation_candidate": {
                "priority": review_task["priority"],
                "action": review_task["action"],
                "dataset": review_task["dataset"],
                "success_gate": review_task["success_gate"],
                "url": review_task["url"],
            },
            "protocol_files": [
                "public_validation_openneuro_smoke_protocol_template.md",
                "public_validation_openneuro_smoke_protocol_template.json",
                "public_validation_openneuro_smoke_runbook.md",
                "public_validation_openneuro_smoke_manifest.json",
            ],
            "current_metric_snapshot": {
                "bold_r2": metric["bold_r2"],
                "fc_corr": metric["fc_corr"],
                "objective_delta": metric["objective_delta"],
                "readiness_score": summary["readiness_score"],
                "routing": summary["routing"],
            },
            "learn_stage_action": {
                "top_action": top["action"],
                "priority_score": top["priority_score"],
                "weighted_profile": top["multi_objective"],
                "why": top["why"],
            },
            "negative_evidence": learning["negative_evidence"],
            "required_outputs": [
                "BIDS validator JSON",
                "ROI QC table",
                "subject split file",
                "motion, site and scanner summary",
                "behavior or task endpoint note",
                "updated validation ledger",
                "updated acquisition portfolio",
            ],
            "decision_rule": "Advance only after protocol fields, QC evidence and external-data review are recorded in the ledger.",
        }
    return packets


def rounded_matrix(matrix: np.ndarray) -> list[list[float]]:
    return [[round(float(x), 4) for x in row] for row in matrix]


def rounded_series(series: np.ndarray) -> list[list[float]]:
    return [[round(float(x), 4) for x in row] for row in series]


def build_learning_update(scenario_key: str, intervention: dict[str, float], metrics: dict[str, float]) -> dict:
    """Rank next simulations using active-learning inspired signals."""
    uncertainty = max(0.0, 1.0 - metrics["bold_r2"])
    fc_gap = max(0.0, 1.0 - metrics["fc_corr"])
    objective_signal = abs(metrics["objective_delta"])
    intervention_cost = float(np.linalg.norm(list(intervention.values())))
    objective_alignment = min(1.0, objective_signal / 0.40)

    candidates = [
        {
            "action": "Perturbation scale sweep",
            "why": "Map dose-response shape and detect nonlinear response thresholds.",
            "expected_information_gain": 0.55 * uncertainty + 0.25 * objective_signal + 0.10 * fc_gap,
            "validation_cost": 0.22 + 0.08 * intervention_cost,
            "novelty": 0.72,
            "base_risk": 0.34,
        },
        {
            "action": "Atlas robustness test",
            "why": "Check whether the inferred path survives a different parcellation.",
            "expected_information_gain": 0.35 * fc_gap + 0.20 * uncertainty + 0.12,
            "validation_cost": 0.30,
            "novelty": 0.42,
            "base_risk": 0.18,
        },
        {
            "action": "Subject split generalization",
            "why": "Estimate whether the surrogate remains useful outside the current synthetic subject.",
            "expected_information_gain": 0.45 * uncertainty + 0.16,
            "validation_cost": 0.42,
            "novelty": 0.52,
            "base_risk": 0.22,
        },
        {
            "action": "Behavior endpoint alignment",
            "why": "Connect the network-level shift to a task or behavioral readout.",
            "expected_information_gain": 0.35 * objective_signal + 0.15 * uncertainty + 0.18,
            "validation_cost": 0.36,
            "novelty": 0.61,
            "base_risk": 0.24,
        },
    ]
    if scenario_key == "closed_loop":
        candidates.append(
            {
                "action": "Constrained policy search",
                "why": "Optimize objective improvement under a small-perturbation budget.",
                "expected_information_gain": 0.35 * objective_signal + 0.25 * uncertainty + 0.18,
                "validation_cost": 0.40,
                "novelty": 0.82,
                "base_risk": 0.40,
            }
        )

    for item in candidates:
        item["priority_score"] = item["expected_information_gain"] - 0.35 * item["validation_cost"]
        fidelity_gain = min(1.0, item["expected_information_gain"] / 0.38)
        feasibility = max(0.0, 1.0 - item["validation_cost"] / 0.60)
        risk = min(1.0, item["base_risk"] + 0.12 * intervention_cost)
        risk_control = max(0.0, 1.0 - risk)
        portfolio_score = (
            PORTFOLIO_WEIGHTS["fidelity"] * fidelity_gain
            + PORTFOLIO_WEIGHTS["objective_alignment"] * objective_alignment
            + PORTFOLIO_WEIGHTS["novelty"] * item["novelty"]
            + PORTFOLIO_WEIGHTS["feasibility"] * feasibility
            + PORTFOLIO_WEIGHTS["risk_control"] * risk_control
        )
        item["multi_objective"] = {
            "fidelity": round(fidelity_gain, 4),
            "objective_alignment": round(objective_alignment, 4),
            "novelty": round(item["novelty"], 4),
            "feasibility": round(feasibility, 4),
            "risk_control": round(risk_control, 4),
            "portfolio_score": round(portfolio_score, 4),
        }

    ranked = sorted(candidates, key=lambda item: item["priority_score"], reverse=True)
    negative_evidence = [
        {
            "action": item["action"],
            "reason": "Low priority in this round; keep as negative evidence for routing and acquisition-policy refinement.",
            "priority_score": round(item["priority_score"], 4),
        }
        for item in ranked[-2:]
    ]
    return {
        "uncertainty": round(uncertainty, 4),
        "fc_gap": round(fc_gap, 4),
        "objective_signal": round(objective_signal, 4),
        "intervention_cost": round(intervention_cost, 4),
        "signal_bars": [
            {"label": "BOLD uncertainty", "value": round(uncertainty, 4), "scaled": round(min(1.0, uncertainty / 0.35), 4)},
            {"label": "FC gap", "value": round(fc_gap, 4), "scaled": round(min(1.0, fc_gap / 0.20), 4)},
            {"label": "Objective signal", "value": round(objective_signal, 4), "scaled": round(min(1.0, objective_signal / 0.40), 4)},
            {"label": "Validation cost", "value": round(intervention_cost, 4), "scaled": round(min(1.0, intervention_cost / 0.70), 4)},
        ],
        "top_action": ranked[0]["action"],
        "negative_evidence": negative_evidence,
        "ranked_actions": [
            {
                "action": item["action"],
                "why": item["why"],
                "expected_information_gain": round(item["expected_information_gain"], 4),
                "validation_cost": round(item["validation_cost"], 4),
                "priority_score": round(item["priority_score"], 4),
                "multi_objective": item["multi_objective"],
            }
            for item in ranked
        ],
    }


def threshold_status(value: float, pass_at: float, watch_at: float) -> str:
    if value >= pass_at:
        return "pass"
    if value >= watch_at:
        return "watch"
    return "hold"


def build_public_review_queue() -> list[dict]:
    queue = []
    for index, tier in enumerate(PUBLIC_VALIDATION_BRIDGE["tiers"], start=1):
        queue.append(
            {
                "priority": index,
                "action": tier["name"],
                "dataset": tier["dataset"],
                "task": tier["task"],
                "success_gate": tier["success_gate"],
                "url": tier["url"],
            }
        )
    return queue


def build_validation_ledger(metrics: dict[str, float], learning: dict) -> dict:
    """Turn validation metrics into explicit gate decisions."""
    intervention_cost = learning["intervention_cost"]
    if intervention_cost <= 0.55:
        cost_status = "pass"
    elif intervention_cost <= 0.75:
        cost_status = "watch"
    else:
        cost_status = "hold"

    gates = [
        {
            "gate": "Signal fidelity",
            "status": threshold_status(metrics["bold_r2"], 0.70, 0.55),
            "evidence": f"BOLD R2 = {metrics['bold_r2']}",
            "threshold": "pass >= 0.70; watch >= 0.55",
            "next_control": "Advance to FC and perturbation audit when pass is reached.",
        },
        {
            "gate": "FC reproducibility",
            "status": threshold_status(metrics["fc_corr"], 0.75, 0.60),
            "evidence": f"FC corr = {metrics['fc_corr']}",
            "threshold": "pass >= 0.75; watch >= 0.60",
            "next_control": "Run atlas robustness or subject-split validation when uncertainty remains.",
        },
        {
            "gate": "Objective effect",
            "status": threshold_status(abs(metrics["objective_delta"]), 0.08, 0.03),
            "evidence": f"objective delta = {metrics['objective_delta']}",
            "threshold": "pass if absolute effect >= 0.08",
            "next_control": "Attach task behavior, symptom score, cell assay or stimulation readout.",
        },
        {
            "gate": "Perturbation budget",
            "status": cost_status,
            "evidence": f"intervention cost = {intervention_cost}",
            "threshold": "pass <= 0.55; watch <= 0.75",
            "next_control": "Search smaller intervention scales before downstream validation.",
        },
        {
            "gate": "External evidence",
            "status": "review",
            "evidence": "Current artifact uses synthetic ROI signals.",
            "threshold": "requires public fMRI, held-out subject split, or expert endpoint review",
            "next_control": "Route to public-data validation before translational claims.",
        },
    ]
    counts = {status: sum(1 for item in gates if item["status"] == status) for status in ["pass", "watch", "review", "hold"]}
    readiness_score = round(
        (
            counts["pass"] * 1.0
            + counts["watch"] * 0.6
            + counts["review"] * 0.4
        )
        / len(gates),
        4,
    )
    if counts["hold"]:
        routing = "Hold for model or data repair"
    elif counts["watch"] or counts["review"]:
        routing = "Advance as dry-run with explicit review gates"
    else:
        routing = "Ready for public-data validation"
    return {
        "principle": "Every virtual experiment must expose pass, watch, review or hold gates before the Learn stage selects the next run.",
        "gates": gates,
        "summary": {
            "pass": counts["pass"],
            "watch": counts["watch"],
            "review": counts["review"],
            "hold": counts["hold"],
            "readiness_score": readiness_score,
            "routing": routing,
        },
        "escalation_rule": "Only pass-gated signals can inform the next acquisition policy directly; watch and review gates create validation tasks in the next DSVL cycle.",
        "review_queue": build_public_review_queue() if counts["review"] else [],
    }


def build_payload() -> dict:
    next_experiments = {
        "emotion": {
            "hypothesis": "Visual-to-limbic over-response can be reduced by strengthening top-down control.",
            "dry_run": "Replay emotional-face task fMRI with subject-level train/test split.",
            "wet_or_human_check": "Compare simulated limbic reduction with task accuracy, reaction time and expert ROI review.",
            "success_gate": "BOLD R2 > 0.70, FC corr > 0.75, perturbation direction stable across 3 seeds.",
        },
        "control": {
            "hypothesis": "Frontoparietal reinforcement and default-mode suppression improve conflict-task stability.",
            "dry_run": "Run cognitive-control task simulation under multiple perturbation strengths.",
            "wet_or_human_check": "Validate against Stroop-like behavior labels or reaction-time shift.",
            "success_gate": "Control gain positive, default-mode intrusion reduced, no large visual-network degradation.",
        },
        "closed_loop": {
            "hypothesis": "A small network-level perturbation can move salience/subcortical dynamics toward a stable attractor.",
            "dry_run": "Search perturbation scale with objective/cost trade-off and uncertainty logging.",
            "wet_or_human_check": "Route top candidate to neurofeedback, stimulation planning, organoid readout, or clinician review.",
            "success_gate": "Objective improves under constrained perturbation and remains robust to missing ROI masking.",
        },
    }
    scenarios = {}
    for key, scenario in SCENARIOS.items():
        pre, stim, true_w = simulate(key, intervention_scale=0.0)
        post, _, _ = simulate(key, intervention_scale=1.0)
        coef = fit_surrogate(pre)
        pred = predict_surrogate(pre, coef)
        fc_true = functional_connectivity(pre)
        fc_pred = functional_connectivity(pred)
        ec = effective_connectivity_from_surrogate(pre, coef)
        candidate = summarize_candidate(pre, post)
        metrics = {
            "bold_r2": round(r2_score(pre[1:], pred[1:]), 4),
            "fc_corr": round(float(np.corrcoef(fc_true.ravel(), fc_pred.ravel())[0, 1]), 4),
            "objective_delta": round(candidate["objective_delta"], 4),
            "limbic_drop": round(candidate["limbic_drop"], 4),
            "control_gain": round(candidate["control_gain"], 4),
            "salience_drop": round(candidate["salience_drop"], 4),
        }
        learning_update = build_learning_update(key, scenario.intervention, metrics)
        scenarios[key] = {
            "name": scenario.name,
            "description": scenario.description,
            "objective": scenario.objective,
            "drives": scenario.drives,
            "intervention": scenario.intervention,
            "series": rounded_series(pre),
            "post_series": rounded_series(post),
            "prediction": rounded_series(pred),
            "stimulus": rounded_series(stim),
            "functional_connectivity": rounded_matrix(fc_true),
            "predicted_connectivity": rounded_matrix(fc_pred),
            "effective_connectivity": rounded_matrix(ec),
            "true_coupling": rounded_matrix(true_w),
            "metrics": metrics,
            "next_experiment": next_experiments[key],
            "learning_update": learning_update,
            "validation_ledger": build_validation_ledger(metrics, learning_update),
        }
    evidence_cards = build_evidence_cards()
    return {
        "project": "NeuroTwin",
        "networks": NETWORKS,
        "scenarios": scenarios,
        "public_validation_bridge": PUBLIC_VALIDATION_BRIDGE,
        "research_backbone": LITERATURE_BACKBONE,
        "evidence_cards": evidence_cards,
        "agent_skill_registry": AGENT_SKILL_REGISTRY,
        "agent_loop_route": AGENT_LOOP_ROUTE,
        "next_validation_packets": build_next_validation_packets(scenarios, evidence_cards),
        "acquisition_policy": {
            "name": "NeuroTwin Learn-stage acquisition policy",
            "formula": "priority(a) = EIG(a) - lambda * Cost(a)",
            "lambda": 0.35,
            "signals": [
                "BOLD uncertainty = 1 - BOLD_R2",
                "FC gap = 1 - FC_corr",
                "Objective signal = abs(objective_delta)",
                "Validation cost = compute + data + experiment + expert-review burden",
            ],
            "purpose": "Select the next simulation or validation action that is expected to reduce uncertainty or improve the objective under realistic cost.",
            "portfolio_axes": [
                "Fidelity gain",
                "Objective alignment",
                "Novelty",
                "Feasibility",
                "Risk control",
            ],
            "portfolio_weights": PORTFOLIO_WEIGHTS,
            "weight_profiles": [
                {
                    "name": "Fidelity-first",
                    "use_case": "Prioritize model reliability before external validation.",
                    "weights": {"fidelity": 0.42, "objective_alignment": 0.18, "novelty": 0.10, "feasibility": 0.16, "risk_control": 0.14},
                },
                {
                    "name": "Exploration-first",
                    "use_case": "Search for high-novelty mechanisms while keeping validation gates visible.",
                    "weights": {"fidelity": 0.22, "objective_alignment": 0.20, "novelty": 0.32, "feasibility": 0.12, "risk_control": 0.14},
                },
                {
                    "name": "Risk-controlled",
                    "use_case": "Prefer lower-risk candidates when downstream validation is expensive or sensitive.",
                    "weights": {"fidelity": 0.24, "objective_alignment": 0.18, "novelty": 0.12, "feasibility": 0.20, "risk_control": 0.26},
                },
            ],
        },
        "virtual_experiment_world": {
            "name": "NeuroTwin virtual experimental world",
            "principle": "Turn brain-system hypotheses into executable dry experiments with explicit evidence gates and learning memory.",
            "layers": [
                {
                    "layer": "Problem Space",
                    "role": "Represent task context, target phenotype, intervention objective and constraints.",
                    "artifact": "Hypothesis + objective function",
                },
                {
                    "layer": "Surrogate Simulator",
                    "role": "Predict brain dynamics and run controllable perturbations before costly validation.",
                    "artifact": "BOLD, FC and virtual EC response",
                },
                {
                    "layer": "Evidence Gates",
                    "role": "Score fidelity, robustness, biological plausibility and validation cost.",
                    "artifact": "Trace-backed metrics",
                },
                {
                    "layer": "Learning Memory",
                    "role": "Retain top choices, weak actions and uncertainty targets for the next DSVL cycle.",
                    "artifact": "Acquisition portfolio",
                },
            ],
        },
        "data_interface_boundary": {
            "principle": "Knowledge mining and data engineering are Design-layer inputs. They source hypotheses, improve data readiness and propose representations before the surrogate brain runs virtual experiments.",
            "interfaces": [
                {
                    "name": "Literature and method mining",
                    "role": "Surface candidate mechanisms, task paradigms, ROI choices and validation metrics.",
                    "output": "Evidence cards, method candidates and hypothesis seeds",
                    "boundary": "Feeds Design; final next-run choice is made by validation metrics and acquisition policy.",
                },
                {
                    "name": "Data extraction and cleaning",
                    "role": "Convert imaging, behavior or metadata assets into reusable model inputs.",
                    "output": "QC reports, ROI time series and dataset cards",
                    "boundary": "Feeds Simulate only after quality gates are recorded.",
                },
                {
                    "name": "Feature engineering",
                    "role": "Build candidate descriptors such as FC priors, task labels, phenotype scores and subject context.",
                    "output": "Feature schema and representation candidates",
                    "boundary": "Provides optional context; surrogate validation decides whether features help.",
                },
                {
                    "name": "Virtual experiment core",
                    "role": "Train surrogate dynamics, run perturbations, validate outputs and update the next policy.",
                    "output": "BOLD predictions, FC/EC response, reports, trace and next-run plan",
                    "boundary": "Main DSVL engine and primary project contribution.",
                },
            ],
        },
        "platform_architecture": {
            "nodes": [
                "Knowledge input layer",
                "Data readiness layer",
                "NeuroTwin virtual world",
                "Validation gates",
                "Programmable acquisition policy",
                "Next experiment",
                "Learning memory",
            ],
            "claim": "NeuroTwin fits an AI4S platform as a callable virtual experiment capability between upstream scientific evidence and downstream validation workflows.",
        },
        "scientific_loop": {
            "name": "DSVL",
            "full_name": "Design-Simulate-Validate-Learn",
            "principle": "A surrogate-driven AI4S loop where hypotheses are designed, tested in virtual brain experiments, validated against neural or behavioral evidence, and learned back into the next round.",
            "steps": [
                {
                    "stage": "Design",
                    "question": "What brain-system hypothesis or intervention objective should be tested next?",
                    "artifact": "Hypothesis, task context, candidate perturbation and objective function",
                },
                {
                    "stage": "Simulate",
                    "question": "How does the surrogate brain respond under the proposed task or perturbation?",
                    "artifact": "Predicted BOLD dynamics, FC shift and virtual EC response",
                },
                {
                    "stage": "Validate",
                    "question": "Does the simulation pass fidelity, stability and plausibility gates?",
                    "artifact": "Signal R2, FC consistency, perturbation robustness and expert-review checklist",
                },
                {
                    "stage": "Learn",
                    "question": "What should change in the next round?",
                    "artifact": "Updated hypothesis ranking, model configuration, uncertainty target and experiment plan",
                },
            ],
        },
        "capability": {
            "name": "NeuroTwin.SurrogateBrainPerturbation",
            "version": "0.2-demo",
            "input_contract": [
                "ROI time series: T x N",
                "Brain atlas and network labels",
                "Scenario objective and candidate perturbation",
                "Optional behavior or clinical endpoint",
            ],
            "output_contract": [
                "Predicted BOLD dynamics",
                "Functional and virtual effective connectivity",
                "Candidate intervention score",
                "Validation metrics and replayable trace",
                "Validation ledger and escalation rule",
            ],
            "validation_gates": [
                "Signal fidelity",
                "FC consistency",
                "Perturbation stability",
                "External-evidence review",
                "Human expert review before real-world action",
            ],
            "platform_fit": [
                "Design: evidence-grounded hypothesis and objective design",
                "Simulate: callable surrogate brain virtual experiment",
                "Validate: trace-backed metrics and plausibility gates",
                "Learn: metrics drive model, hypothesis and experiment iteration",
            ],
        },
        "trace": [
            {
                "stage": "Design",
                "artifact": "Brain-system hypothesis, task context and candidate perturbation objective",
                "status": "hypothesis-ready",
            },
            {
                "stage": "Simulate",
                "artifact": "ROI time series -> surrogate dynamics -> virtual perturbation",
                "status": "executable",
            },
            {
                "stage": "Validate",
                "artifact": "Signal fidelity, FC consistency and perturbation stability gates",
                "status": "metrics-recorded",
            },
            {
                "stage": "Learn",
                "artifact": "Next hypothesis, uncertainty target and experiment-plan update",
                "status": "next-round-ready",
            },
        ],
    }


def write_report(payload: dict) -> None:
    scenario_lines = []
    learning_lines = []
    portfolio_lines = []
    ledger_lines = []
    packet_lines = []
    bridge_lines = [
        f"| {tier['name']} | {tier['dataset']} | {tier['access']} | {tier['task']} |"
        for tier in payload["public_validation_bridge"]["tiers"]
    ]
    for key, item in payload["scenarios"].items():
        m = item["metrics"]
        scenario_lines.append(
            f"| {item['name']} | {m['bold_r2']} | {m['fc_corr']} | "
            f"{m['objective_delta']} | {item['objective']} |"
        )
        learn = item["learning_update"]
        top = learn["ranked_actions"][0]
        learning_lines.append(
            f"| {item['name']} | {learn['uncertainty']} | {learn['fc_gap']} | "
            f"{top['action']} | {top['priority_score']} |"
        )
        profile = top["multi_objective"]
        portfolio_lines.append(
            f"| {item['name']} | {top['action']} | {profile['fidelity']} | "
            f"{profile['objective_alignment']} | {profile['novelty']} | "
            f"{profile['feasibility']} | {profile['risk_control']} | "
            f"{profile['portfolio_score']} |"
        )
        summary = item["validation_ledger"]["summary"]
        ledger_lines.append(
            f"| {item['name']} | {summary['pass']} | {summary['watch']} | "
            f"{summary['review']} | {summary['hold']} | {summary['readiness_score']} | "
            f"{summary['routing']} |"
        )
        packet = payload["next_validation_packets"][key]
        packet_lines.append(
            f"| {item['name']} | {packet['learn_stage_action']['top_action']} | "
            f"{packet['public_validation_candidate']['action']} | "
            f"{packet['current_metric_snapshot']['readiness_score']} | {packet['decision_rule']} |"
        )
    report = (
        "# NeuroTwin Demo Report\n\n"
        "## Demo Purpose\n\n"
        "NeuroTwin demonstrates an agent-ready surrogate brain capability for neuro-AI4S. "
        "The demo uses synthetic ROI-level fMRI-like signals to show the executable workflow: "
        "build a brain dynamics surrogate, run virtual perturbations, score the response, and "
        "produce a trace-backed next-experiment suggestion. The core scientific loop is DSVL: "
        "Design, Simulate, Validate and Learn.\n\n"
        "## What This Proves\n\n"
        "- The proposal has been turned from concept into a callable workflow.\n"
        "- The workflow follows a surrogate-driven Design-Simulate-Validate-Learn loop.\n"
        "- The surrogate brain can be evaluated by signal fidelity, FC consistency, perturbation response, "
        "and human-readable experiment traces.\n\n"
        "## Demo Metrics\n\n"
        "| Scenario | BOLD R2 | FC Corr | Objective Delta | Objective |\n"
        "| --- | ---: | ---: | ---: | --- |\n"
        f"{chr(10).join(scenario_lines)}\n\n"
        "## Learn Stage Ranking\n\n"
        "| Scenario | Uncertainty | FC Gap | Next simulation | Priority |\n"
        "| --- | ---: | ---: | --- | ---: |\n"
        f"{chr(10).join(learning_lines)}\n\n"
        "## Multi-Objective Acquisition Portfolio\n\n"
        "| Scenario | Top action | Fidelity | Objective | Novelty | Feasibility | Risk control | Portfolio |\n"
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |\n"
        f"{chr(10).join(portfolio_lines)}\n\n"
        "Default portfolio weights: fidelity 0.32, objective 0.22, novelty 0.18, feasibility 0.16, risk control 0.12. "
        "The interactive dashboard can adjust these weights to simulate different experiment-operation policies.\n\n"
        "## Validation Ledger\n\n"
        "| Scenario | Pass | Watch | Review | Hold | Readiness | Routing |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |\n"
        f"{chr(10).join(ledger_lines)}\n\n"
        "The ledger turns validation into a visible gate before the Learn stage updates the next run. "
        "Review gates create explicit validation tasks for public data, held-out subjects or expert endpoint review.\n\n"
        "## Public Validation Bridge\n\n"
        f"{payload['public_validation_bridge']['principle']}\n\n"
        "| Tier | Dataset | Access | Task |\n"
        "| --- | --- | --- | --- |\n"
        f"{chr(10).join(bridge_lines)}\n\n"
        "## Evidence Backbone\n\n"
        "| Theme | Source | Project move |\n"
        "| --- | --- | --- |\n"
        + "\n".join(
            f"| {item['theme']} | [{item['source']}]({item['url']}) | {item['project_move']} |"
            for item in payload["research_backbone"]
        )
        + "\n\n"
        "## Agent Loop and Next Validation Packet\n\n"
        f"{payload['agent_loop_route']['principle']}\n\n"
        "| Scenario | Learn action | Validation candidate | Readiness | Decision rule |\n"
        "| --- | --- | --- | ---: | --- |\n"
        f"{chr(10).join(packet_lines)}\n\n"
        "## Interpretation\n\n"
        "Positive objective delta means the virtual intervention moved the network in the desired "
        "direction for this synthetic task. In a real project, this metric would be replaced or "
        "calibrated by domain endpoints such as task accuracy, symptom-scale shift, cell assay "
        "response, or stimulation readout.\n\n"
        "## Next Step\n\n"
        "Replace synthetic signals with a public fMRI dataset, package preprocessing as a reusable "
        "capability, and expose the surrogate model as an API with explicit input/output schemas and "
        "replayable execution traces. The next research step is to add uncertainty-aware experiment "
        "selection so the Learn stage actively chooses the most informative next simulation.\n"
    )
    (DIST / "demo_report.md").write_text(report, encoding="utf-8")


def write_data_card() -> None:
    data_card = dedent(
        """
        # Data Card

        This demo uses synthetic ROI-level fMRI-like time series generated by a stable nonlinear
        dynamical system. No personal, clinical, or medical data are included.

        ## Fields

        - `series`: simulated pre-intervention ROI signals.
        - `prediction`: one-step surrogate predictions.
        - `post_series`: simulated response after candidate perturbation.
        - `functional_connectivity`: correlation matrix from `series`.
        - `predicted_connectivity`: correlation matrix from `prediction`.
        - `effective_connectivity`: perturbation response inferred from the fitted surrogate.
        - `metrics`: signal, network, and objective metrics.
        - `learning_update`: acquisition signals, ranked next actions, multi-objective profiles and negative evidence.
        - `validation_ledger`: pass, watch, review and hold gates for scientific readiness.
        - `public_validation_bridge`: concrete public-data tasks created by review gates.
        - `research_backbone`: curated literature and infrastructure cues used by the demo design.
        - `evidence_cards`: structured literature-to-design cards for the Design stage.
        - `agent_skill_registry`: callable skill map for the Read-Prepare-Build-Compute-Validate-Learn route.
        - `agent_loop_route`: platform-style route for Agent-orchestrated scientific work.
        - `next_validation_packets`: decision-ready packets for the next public validation cycle.

        ## Intended Use

        The dataset is only for demonstrating the workflow and UI. It should not be interpreted as
        a biomedical model or used for clinical claims.
        """
    ).strip() + "\n"
    (DIST / "data_card.md").write_text(data_card, encoding="utf-8")


def write_validation_ledger_note(payload: dict) -> None:
    lines = [
        "# Validation Ledger",
        "",
        "This note makes the Validate stage explicit. Each virtual experiment is routed through pass, watch, review or hold gates before its result can update the next acquisition policy.",
        "",
        "## Scenario Summaries",
        "",
        "| Scenario | Pass | Watch | Review | Hold | Readiness | Routing |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for scenario in payload["scenarios"].values():
        summary = scenario["validation_ledger"]["summary"]
        lines.append(
            f"| {scenario['name']} | {summary['pass']} | {summary['watch']} | "
            f"{summary['review']} | {summary['hold']} | {summary['readiness_score']} | "
            f"{summary['routing']} |"
        )
    lines += [
        "",
        "## Gate Details",
        "",
    ]
    for scenario in payload["scenarios"].values():
        ledger = scenario["validation_ledger"]
        lines += [
            f"### {scenario['name']}",
            "",
            ledger["principle"],
            "",
            "| Gate | Status | Evidence | Threshold | Next control |",
            "| --- | --- | --- | --- | --- |",
        ]
        for gate in ledger["gates"]:
            lines.append(
                f"| {gate['gate']} | {gate['status']} | {gate['evidence']} | "
                f"{gate['threshold']} | {gate['next_control']} |"
            )
        lines += [
            "",
            f"Escalation rule: {ledger['escalation_rule']}",
            "",
            "Review queue:",
            "",
        ]
        for task in ledger["review_queue"]:
            lines += [
                f"- P{task['priority']} {task['action']}: {task['task']} Success gate: {task['success_gate']} ({task['url']})",
            ]
        lines += [
            "",
        ]
    lines += [
        "## Design Cues",
        "",
        "- Virtual brain simulation and digital twin work motivate explicit subject/data readiness and intervention validation: https://academic.oup.com/nsr/article/11/5/nwae079/7616087",
        "- Neural perturbational inference motivates using a trained surrogate as a virtual perturbation object: https://www.nature.com/articles/s41592-025-02654-x",
        "- Self-driving laboratory work motivates visible metrics for closed-loop experiment selection: https://www.nature.com/articles/s41467-024-45569-5",
        "",
    ]
    (DIST / "validation_ledger.md").write_text("\n".join(lines), encoding="utf-8")


def write_public_validation_bridge_note(payload: dict) -> None:
    bridge = payload["public_validation_bridge"]
    lines = [
        "# Public Validation Bridge",
        "",
        bridge["principle"],
        "",
        "## Validation Tiers",
        "",
        "| Tier | Dataset | Access | Task | Success gate | Source |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for tier in bridge["tiers"]:
        lines.append(
            f"| {tier['name']} | {tier['dataset']} | {tier['access']} | "
            f"{tier['task']} | {tier['success_gate']} | {tier['url']} |"
        )
    lines += [
        "",
        "## How Review Gates Use This Bridge",
        "",
        "When `External evidence` is marked as `review`, the next DSVL cycle should schedule the OpenNeuro smoke test first. HCP transfer and ABCD cohort stress testing follow only after data access, governance and QC are clear.",
        "",
        "## Minimum Executable Path",
        "",
        "1. Select one OpenNeuro BIDS task-fMRI dataset.",
        "2. Run ROI extraction and QC into the existing `demo_data.json` schema.",
        "3. Recompute BOLD R2, FC corr, objective effect and perturbation budget.",
        "4. Update the Validation Ledger and acquisition portfolio.",
        "5. Keep failed or weak validation runs as negative evidence for routing.",
        "",
    ]
    (DIST / "public_validation_bridge.md").write_text("\n".join(lines), encoding="utf-8")


def write_literature_research_brief(payload: dict) -> None:
    lines = [
        "# Literature Research Brief",
        "",
        "This brief records the current evidence backbone for NeuroTwin. Each item is translated into a concrete project design move.",
        "",
        "## Current Insights",
        "",
        "| Theme | Source | Insight | Project move |",
        "| --- | --- | --- | --- |",
    ]
    for item in payload["research_backbone"]:
        lines.append(
            f"| {item['theme']} | [{item['source']}]({item['url']}) | {item['insight']} | {item['project_move']} |"
        )
    lines += [
        "",
        "## Design Consequences",
        "",
        "- Treat NeuroTwin as a platform capability with input/output contracts, execution traces and validation gates.",
        "- Keep surrogate brain modeling connected to MRI-derived brain network simulation, with TVB-style multiscale modeling as a future extension.",
        "- Record autonomy level, repeatability assumptions, dataset state, QC status and operator choices for each validation packet.",
        "- Let literature and method mining generate evidence cards for Design, then require each hypothesis to pass simulation and review gates.",
        "- Use BIDS/OpenNeuro/HCP/ABCD as staged validation resources, with motion, site/scanner and behavior-endpoint checks recorded separately from model score.",
        "",
        "## Source Links",
        "",
        "- Bohrium + SciMaster: https://arxiv.org/abs/2512.20469",
        "- The Virtual Brain on EBRAINS: https://ebrains.eu/data-tools-services/tools/the-virtual-brain",
        "- Self-driving lab metrics: https://www.nature.com/articles/s41467-024-45569-5",
        "- Science acceleration with SDLs: https://www.nature.com/articles/s41467-025-59231-1",
        "- AI co-scientist: https://arxiv.org/abs/2502.18864",
        "- OpenNeuro CLI: https://docs.openneuro.org/packages/openneuro-cli.html",
        "- BIDS Validator: https://github.com/bids-standard/bids-validator",
        "- ABCD imaging data sharing: https://abcdstudy.org/scientists/data-sharing/fast-track-imaging-data-release/",
        "",
    ]
    (DIST / "literature_research_brief.md").write_text("\n".join(lines), encoding="utf-8")


def write_evidence_cards(payload: dict) -> None:
    (DIST / "evidence_cards.json").write_text(
        json.dumps(payload["evidence_cards"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    fields = [
        ("card_id", "Stable card identifier."),
        ("source_theme", "Research theme or infrastructure standard."),
        ("evidence_claim", "Condensed claim extracted from literature or standards."),
        ("design_input", "How the claim enters the DSVL Design stage."),
        ("surrogate_requirement", "What the surrogate or virtual world must support."),
        ("validation_gate", "Gate or artifact needed before stronger claims."),
        ("risk_to_track", "Failure mode that must stay visible."),
        ("next_action", "Concrete next project action."),
        ("source_url", "Source link for review."),
    ]
    lines = [
        "# Evidence Card Schema",
        "",
        "Evidence cards are the interface between literature/method mining and the DSVL Design stage. They convert external knowledge into testable inputs, surrogate requirements and validation gates.",
        "",
        "## Schema Fields",
        "",
        "| Field | Meaning |",
        "| --- | --- |",
    ]
    lines += [f"| `{name}` | {meaning} |" for name, meaning in fields]
    lines += [
        "",
        "## Current Cards",
        "",
        "| Card | Theme | Design input | Validation gate |",
        "| --- | --- | --- | --- |",
    ]
    for card in payload["evidence_cards"]:
        lines.append(
            f"| {card['card_id']} | {card['source_theme']} | {card['design_input']} | {card['validation_gate']} |"
        )
    lines += [
        "",
        "## Why This Matters",
        "",
        "This schema keeps literature parsing useful as an AI4S interface: extracted evidence must become a scenario input, surrogate requirement, validation gate, risk record or next action.",
        "",
    ]
    (DIST / "evidence_card_schema.md").write_text("\n".join(lines), encoding="utf-8")


def write_agent_skill_registry(payload: dict) -> None:
    route = payload["agent_loop_route"]
    lines = [
        "# Agent Skill Registry",
        "",
        route["principle"],
        "",
        "## Loop Route",
        "",
        "| Step | Agent action | Memory written back |",
        "| --- | --- | --- |",
    ]
    for step in route["steps"]:
        lines.append(f"| {step['step']} | {step['agent_action']} | {step['memory']} |")
    lines += [
        "",
        "## Callable Skills",
        "",
        "| Skill | Stage | Purpose | Gate | Artifact |",
        "| --- | --- | --- | --- | --- |",
    ]
    for skill in payload["agent_skill_registry"]:
        lines.append(
            f"| `{skill['skill_id']}` | {skill['stage']} | {skill['purpose']} | "
            f"{skill['gate']} | {skill['artifact']} |"
        )
    lines += [
        "",
        "## Why This Matters",
        "",
        "This registry turns the demo into a platform-style scientific capability. A master agent can inspect which tool to call, what evidence it consumes, what artifact it emits and which gate must be satisfied before the next stage.",
        "",
    ]
    (DIST / "agent_skill_registry.md").write_text("\n".join(lines), encoding="utf-8")


def write_next_validation_packets(payload: dict) -> None:
    packets = payload["next_validation_packets"]
    (DIST / "next_validation_packet.json").write_text(
        json.dumps(packets, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Next Validation Packet",
        "",
        "A next validation packet is the handoff object between one DSVL cycle and the next. It packages the scenario objective, evidence cards, Agent skill route, public validation candidate, protocol files, current metric state, next action and negative evidence.",
        "",
        "## Scenario Packets",
        "",
    ]
    for packet in packets.values():
        metrics = packet["current_metric_snapshot"]
        action = packet["learn_stage_action"]
        candidate = packet["public_validation_candidate"]
        card_list = ", ".join(item["card_id"] for item in packet["linked_evidence_cards"])
        output_list = "; ".join(packet["required_outputs"])
        protocol_list = "; ".join(packet["protocol_files"])
        negative = "; ".join(
            f"{item['action']} ({item['priority_score']})" for item in packet["negative_evidence"]
        )
        lines += [
            f"### {packet['scenario']}",
            "",
            f"- Packet ID: `{packet['packet_id']}`",
            f"- Objective: {packet['objective']}",
            f"- Why now: {packet['why_now']}",
            f"- Evidence cards: {card_list}",
            f"- Agent route: {' -> '.join(packet['agent_skill_route'])}",
            f"- Public validation candidate: P{candidate['priority']} {candidate['action']} using {candidate['dataset']}. Success gate: {candidate['success_gate']}",
            f"- Protocol files: {protocol_list}",
            f"- Current metrics: BOLD R2 {metrics['bold_r2']}, FC corr {metrics['fc_corr']}, objective {metrics['objective_delta']}, readiness {metrics['readiness_score']}, routing {metrics['routing']}",
            f"- Learn action: {action['top_action']} (priority {action['priority_score']}). {action['why']}",
            f"- Negative evidence: {negative}",
            f"- Required outputs: {output_list}",
            f"- Decision rule: {packet['decision_rule']}",
            "",
        ]
    lines += [
        "## Reviewer Reading",
        "",
        "This file is the clearest place to show AI-accelerated iteration: the previous run produces a small structured packet that can be routed to the next dry validation step, then merged back into the ledger and acquisition policy.",
        "",
    ]
    (DIST / "next_validation_packet.md").write_text("\n".join(lines), encoding="utf-8")


def write_capability_card(payload: dict) -> None:
    cap = payload["capability"]
    lines = [
        "# Capability Card",
        "",
        f"Name: `{cap['name']}`",
        f"Version: `{cap['version']}`",
        "",
        "## Input Contract",
        "",
    ]
    lines += [f"- {item}" for item in cap["input_contract"]]
    lines += ["", "## Output Contract", ""]
    lines += [f"- {item}" for item in cap["output_contract"]]
    lines += ["", "## Validation Gates", ""]
    lines += [f"- {item}" for item in cap["validation_gates"]]
    lines += ["", "## Platform Fit", ""]
    lines += [f"- {item}" for item in cap["platform_fit"]]
    lines += ["", "## Agent Skill Route", ""]
    lines += [f"- `{item['skill_id']}` ({item['stage']}): {item['purpose']}" for item in payload["agent_skill_registry"]]
    lines += [
        "",
        "## Next Validation Packet",
        "",
        "- `artifacts/demo/next_validation_packet.json`: machine-readable handoff for the next DSVL cycle.",
        "- `artifacts/demo/next_validation_packet.md`: human-readable scenario packets and decision rules.",
    ]
    lines += ["", "## Evidence Backbone", ""]
    lines += [f"- {item['theme']}: {item['project_move']} ({item['url']})" for item in payload["research_backbone"]]
    lines += [
        "",
        "## Boundary",
        "",
        "This is a research workflow capability for hypothesis generation and virtual dry-runs. "
        "It does not perform clinical diagnosis or autonomous medical decision-making.",
        "",
    ]
    (DIST / "capability_card.md").write_text("\n".join(lines), encoding="utf-8")


def write_trace_jsonl(payload: dict) -> None:
    rows = []
    for index, item in enumerate(payload["trace"], start=1):
        rows.append(
            {
                "run_id": "neurotwin-demo-0001",
                "step": index,
                "stage": item["stage"],
                "artifact": item["artifact"],
                "status": item["status"],
                "validation": "recorded",
            }
        )
    (DIST / "experiment_trace.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def write_next_experiment_plan(payload: dict) -> None:
    lines = [
        "# Next Experiment Plan",
        "",
        "This plan turns the virtual perturbation demo into an executable dry-run workflow that can later be connected to public fMRI data or laboratory feedback.",
        "",
    ]
    for item in payload["scenarios"].values():
        nxt = item["next_experiment"]
        top = item["learning_update"]["ranked_actions"][0]
        lines += [
            f"## {item['name']}",
            "",
            f"- Hypothesis: {nxt['hypothesis']}",
            f"- Dry run: {nxt['dry_run']}",
            f"- Human or experiment check: {nxt['wet_or_human_check']}",
            f"- Success gate: {nxt['success_gate']}",
            f"- Learn-stage priority: {top['action']} (score {top['priority_score']})",
        ]
        for task in item["validation_ledger"]["review_queue"][:1]:
            lines.append(f"- Review-gate validation: {task['action']} -> {task['success_gate']}")
        lines.append("")
    (DIST / "next_experiment_plan.md").write_text("\n".join(lines), encoding="utf-8")


def write_scientific_loop_note(payload: dict) -> None:
    loop = payload["scientific_loop"]
    lines = [
        "# DSVL Scientific Loop",
        "",
        f"Loop name: **{loop['full_name']}**",
        "",
        loop["principle"],
        "",
        "## Why DSVL",
        "",
        "AI4S projects become more scientific when the surrogate model participates in experiment design, simulation, validation and learning. For NeuroTwin, the main claim is the creation of a virtual experimental world for brain-system research.",
        "",
        "Knowledge extraction, literature parsing and feature engineering support the Design stage. The core scientific value comes from the surrogate-driven loop itself.",
        "",
        "## Stages",
        "",
    ]
    for item in loop["steps"]:
        lines += [
            f"### {item['stage']}",
            "",
            f"- Guiding question: {item['question']}",
            f"- Artifact: {item['artifact']}",
            "",
        ]
    lines += [
        "## Next Upgrade",
        "",
        "Add active-learning style experiment selection: the Learn stage should rank the next simulation by expected information gain, uncertainty reduction and validation cost.",
        "",
    ]
    (DIST / "scientific_loop.md").write_text("\n".join(lines), encoding="utf-8")


def write_theoretical_model_note() -> None:
    lines = [
        "# Theoretical Model",
        "",
        "NeuroTwin uses a three-layer model: dynamics, virtual perturbation and closed-loop experiment selection.",
        "",
        "## 1. Brain Dynamics Surrogate",
        "",
        "```text",
        "x_{t+1} = F_theta(x_t, u_t, c) + epsilon_t",
        "```",
        "",
        "- `x_t`: ROI or network-level brain state.",
        "- `u_t`: task stimulus, candidate intervention or context input.",
        "- `c`: subject-level context such as connectome, phenotype or session metadata.",
        "- `F_theta`: learned surrogate brain dynamics.",
        "",
        "## 2. Virtual Perturbation Response",
        "",
        "```text",
        "R_i(x_t, delta) = F_theta(x_t + delta e_i, u_t, c) - F_theta(x_t, u_t, c)",
        "EC_{i,j} = E_t [R_i(x_t, delta)_j]",
        "```",
        "",
        "This turns the trained surrogate into a virtual experimental object. Perturbing node `i` produces a response profile across target nodes.",
        "",
        "## 3. Learn-Stage Experiment Selection",
        "",
        "```text",
        "a_next = argmax_a [ I(a; F_theta, D) - lambda C(a) ]",
        "```",
        "",
        "- `I(a; F_theta, D)`: expected information gain or uncertainty reduction from the next simulation or validation action.",
        "- `C(a)`: validation cost, including compute, data, experimental burden and expert-review effort.",
        "- `lambda`: cost-sensitivity parameter.",
        "",
        "In the current demo, this is approximated by a transparent heuristic based on BOLD uncertainty, FC gap, objective signal and validation cost. A real version can replace it with Bayesian optimization, active learning or multi-objective acquisition functions.",
        "",
    ]
    (DIST / "theoretical_model.md").write_text("\n".join(lines), encoding="utf-8")


def write_acquisition_policy_note(payload: dict) -> None:
    policy = payload["acquisition_policy"]
    lines = [
        "# Learn-Stage Acquisition Policy",
        "",
        f"Policy: **{policy['name']}**",
        "",
        "The Learn stage should decide what to run next. In this demo, that decision is implemented as a transparent acquisition policy inspired by active learning and Bayesian optimization.",
        "",
        "## Formula",
        "",
        "```text",
        policy["formula"],
        "```",
        "",
        f"Current `lambda`: `{policy['lambda']}`",
        "",
        "## Signals",
        "",
    ]
    lines += [f"- {signal}" for signal in policy["signals"]]
    lines += [
        "",
        "## Multi-Objective Audit Axes",
        "",
    ]
    lines += [f"- {axis}" for axis in policy["portfolio_axes"]]
    lines += [
        "",
        "## Programmable Policy State",
        "",
        "Default portfolio weights:",
        "",
        "| Axis | Weight |",
        "| --- | ---: |",
    ]
    for axis, weight in policy["portfolio_weights"].items():
        lines.append(f"| {axis} | {weight} |")
    lines += [
        "",
        "Preset policy profiles:",
        "",
        "| Profile | Use case |",
        "| --- | --- |",
    ]
    for profile in policy["weight_profiles"]:
        lines.append(f"| {profile['name']} | {profile['use_case']} |")
    lines += [
        "",
        "## Purpose",
        "",
        policy["purpose"],
        "",
        "## Current Demo Ranking",
        "",
        "| Scenario | Top next action | Priority | Why |",
        "| --- | --- | ---: | --- |",
    ]
    for scenario in payload["scenarios"].values():
        top = scenario["learning_update"]["ranked_actions"][0]
        lines.append(f"| {scenario['name']} | {top['action']} | {top['priority_score']} | {top['why']} |")
    lines += [
        "",
        "## Portfolio Audit",
        "",
        "| Scenario | Top action | Fidelity | Objective | Novelty | Feasibility | Risk control | Portfolio |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for scenario in payload["scenarios"].values():
        top = scenario["learning_update"]["ranked_actions"][0]
        profile = top["multi_objective"]
        lines.append(
            f"| {scenario['name']} | {top['action']} | {profile['fidelity']} | "
            f"{profile['objective_alignment']} | {profile['novelty']} | "
            f"{profile['feasibility']} | {profile['risk_control']} | "
            f"{profile['portfolio_score']} |"
        )
    lines += [
        "",
        "## Negative Evidence",
        "",
        "Low-priority actions are retained as routing evidence. They can help future policies avoid repeating weak experiment choices.",
        "",
        "| Scenario | Low-priority actions |",
        "| --- | --- |",
    ]
    for scenario in payload["scenarios"].values():
        rejected = "; ".join(f"{item['action']} ({item['priority_score']})" for item in scenario["learning_update"]["negative_evidence"])
        lines.append(f"| {scenario['name']} | {rejected} |")
    lines += [
        "",
        "## Upgrade Path",
        "",
        "- Replace transparent heuristic EIG with posterior uncertainty from an ensemble, Bayesian neural network, or Gaussian process surrogate.",
        "- Add multi-objective acquisition when the project needs to balance fidelity, biological plausibility, experimental cost and novelty.",
        "- Log rejected actions as negative evidence so failed runs also improve the next round.",
        "",
    ]
    (DIST / "acquisition_policy.md").write_text("\n".join(lines), encoding="utf-8")


def write_virtual_experiment_world_note(payload: dict) -> None:
    world = payload["virtual_experiment_world"]
    lines = [
        "# Virtual Experimental World",
        "",
        f"Name: **{world['name']}**",
        "",
        world["principle"],
        "",
        "## Layers",
        "",
        "| Layer | Role | Artifact |",
        "| --- | --- | --- |",
    ]
    for item in world["layers"]:
        lines.append(f"| {item['layer']} | {item['role']} | {item['artifact']} |")
    lines += [
        "",
        "## Why It Matters",
        "",
        "The key AI4S value is the ability to run many low-cost virtual trials before selecting expensive data collection or human validation. The virtual world keeps hypotheses, simulation outputs, validation gates and learning memory in one traceable loop.",
        "",
        "## Expansion Interfaces",
        "",
        "- Public fMRI datasets for task-specific or resting-state validation.",
        "- Behavioral endpoints for objective calibration.",
        "- Molecular, protein or gene model outputs as upstream mechanism hypotheses.",
        "- Lab feedback from neurofeedback, stimulation planning, organoid readout or expert review.",
        "",
    ]
    (DIST / "virtual_experiment_world.md").write_text("\n".join(lines), encoding="utf-8")


def write_experiment_os_policy_note(payload: dict) -> None:
    policy = payload["acquisition_policy"]
    lines = [
        "# Programmable Experiment OS Policy",
        "",
        "This note explains how the Learn stage can behave like a small programmable experiment-operation policy.",
        "",
        "## Policy State",
        "",
        "```json",
        json.dumps(
            {
                "priority_formula": policy["formula"],
                "portfolio_weights": policy["portfolio_weights"],
                "decision_memory": ["ranked_actions", "negative_evidence", "next_experiment"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## Why This Matters",
        "",
        "A scientific loop becomes more useful when its next-step policy can be inspected and adjusted. In NeuroTwin, changing the acquisition weights simulates different operating modes: reliability-first, exploration-first, or risk-controlled validation.",
        "",
        "## Preset Profiles",
        "",
        "| Profile | Use case | Weights |",
        "| --- | --- | --- |",
    ]
    for profile in policy["weight_profiles"]:
        weights = ", ".join(f"{key}={value}" for key, value in profile["weights"].items())
        lines.append(f"| {profile['name']} | {profile['use_case']} | {weights} |")
    lines += [
        "",
        "## Demo Behavior",
        "",
        "- The static JSON stores default weights for reproducibility.",
        "- The HTML dashboard exposes sliders for the five acquisition axes.",
        "- Changing weights reranks the visible acquisition portfolio and updates the next-run transition.",
        "- Negative evidence remains logged even when a different weight profile changes the top action.",
        "",
    ]
    (DIST / "experiment_os_policy.md").write_text("\n".join(lines), encoding="utf-8")


def write_data_interface_boundary_note(payload: dict) -> None:
    boundary = payload["data_interface_boundary"]
    lines = [
        "# Data Interface Boundary",
        "",
        boundary["principle"],
        "",
        "## Interface Map",
        "",
        "| Interface | Role | Output | Boundary |",
        "| --- | --- | --- | --- |",
    ]
    for item in boundary["interfaces"]:
        lines.append(f"| {item['name']} | {item['role']} | {item['output']} | {item['boundary']} |")
    lines += [
        "",
        "## Positioning",
        "",
        "The data interface layer makes the project compatible with large-scale literature parsing, data extraction, data cleaning and feature engineering pipelines. Its job is to improve hypothesis quality and data readiness before a virtual experiment starts.",
        "",
        "The main NeuroTwin contribution remains the executable scientific loop: surrogate simulation, validation gates, programmable acquisition policy and learning memory.",
        "",
    ]
    (DIST / "data_interface_boundary.md").write_text("\n".join(lines), encoding="utf-8")


def write_platform_architecture_note(payload: dict) -> None:
    arch = payload["platform_architecture"]
    lines = [
        "# Platform Architecture Map",
        "",
        arch["claim"],
        "",
        "## Mermaid View",
        "",
        "```mermaid",
        "flowchart LR",
        '  A["Knowledge Input Layer<br/>literature, methods, mechanisms"] --> B["Data Readiness Layer<br/>QC, ROI signals, feature schema"]',
        '  B --> C["NeuroTwin Virtual World<br/>problem space + surrogate simulator"]',
        '  C --> D["Validation Gates<br/>fidelity, FC, robustness, plausibility"]',
        '  D --> E["Programmable Acquisition Policy<br/>weights, profiles, next-run ranking"]',
        '  E --> F["Next Experiment<br/>dry-run, human check, lab feedback"]',
        '  F --> G["Learning Memory<br/>positive signal + negative evidence"]',
        '  G --> A',
        "```",
        "",
        "## Layer Responsibilities",
        "",
        "| Layer | Responsibility |",
        "| --- | --- |",
    ]
    responsibilities = {
        "Knowledge input layer": "Collect evidence and candidate methods for Design.",
        "Data readiness layer": "Convert raw data and metadata into validated model inputs.",
        "NeuroTwin virtual world": "Run surrogate brain simulation and virtual perturbation.",
        "Validation gates": "Record fidelity, robustness, plausibility and cost signals.",
        "Programmable acquisition policy": "Rank the next action under configurable operating preferences.",
        "Next experiment": "Define dry-run, human review or downstream validation action.",
        "Learning memory": "Keep successful signals and negative evidence for the next DSVL cycle.",
    }
    for node in arch["nodes"]:
        lines.append(f"| {node} | {responsibilities[node]} |")
    lines += [
        "",
        "## Company-Fit Reading",
        "",
        "This architecture makes NeuroTwin look like an AI4S platform capability: it has inputs, executable simulation, validation gates, policy state, trace memory and a path to downstream experimental feedback.",
        "",
    ]
    (DIST / "platform_architecture.md").write_text("\n".join(lines), encoding="utf-8")


def write_dashboard(payload: dict) -> None:
    payload_json = json.dumps(payload, ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NeuroTwin Demo</title>
  <link rel="icon" href="data:,">
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --ink: #17202a;
      --muted: #64707d;
      --line: #dce2e8;
      --blue: #2563eb;
      --green: #0f8b6f;
      --red: #c24132;
      --amber: #b45309;
      --violet: #6d5bd0;
      --shadow: 0 12px 28px rgba(18, 32, 46, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      letter-spacing: 0;
    }}
    header {{
      padding: 22px 28px 16px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
      position: sticky;
      top: 0;
      z-index: 5;
    }}
    .title-row {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      max-width: 1240px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0;
      font-size: 24px;
      line-height: 1.2;
      font-weight: 750;
    }}
    .subtitle {{
      margin-top: 6px;
      color: var(--muted);
      font-size: 14px;
      max-width: 760px;
    }}
    .status-pill {{
      border: 1px solid #b8d5cc;
      color: #0f6b55;
      background: #eaf7f2;
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 13px;
      white-space: nowrap;
    }}
    main {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 20px 28px 36px;
    }}
    .core-intro {{
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .intro-card {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 16px;
    }}
    .intro-title {{
      font-size: 14px;
      font-weight: 780;
      margin-bottom: 6px;
    }}
    .intro-text {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.55;
    }}
    .workflow-mini {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
      margin-top: 10px;
    }}
    .workflow-mini-step {{
      border: 1px solid #d7e2ef;
      border-radius: 8px;
      background: #f8fbff;
      padding: 9px 10px;
      min-height: 76px;
      font-size: 12px;
      line-height: 1.4;
    }}
    .workflow-mini-step strong {{
      display: block;
      color: var(--blue);
      margin-bottom: 4px;
    }}
    .folded-stack {{
      display: grid;
      gap: 10px;
      margin-top: 16px;
    }}
    details.collapsible {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}
    details.collapsible > summary {{
      list-style: none;
      cursor: pointer;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      font-size: 14px;
      font-weight: 780;
      background: #fbfcfd;
    }}
    details.collapsible > summary::-webkit-details-marker {{ display: none; }}
    details.collapsible > summary::after {{
      content: "+";
      color: var(--muted);
      font-size: 18px;
      line-height: 1;
      font-weight: 600;
    }}
    details.collapsible[open] > summary::after {{ content: "–"; }}
    .summary-note {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 500;
      line-height: 1.45;
      margin-left: auto;
      max-width: 760px;
    }}
    .collapsible-body {{
      padding: 13px 16px 16px;
      border-top: 1px solid var(--line);
    }}
    .toolbar {{
      display: grid;
      grid-template-columns: minmax(320px, 1fr) auto;
      gap: 14px;
      align-items: center;
      margin-bottom: 16px;
    }}
    .tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    button {{
      border: 1px solid var(--line);
      background: #fff;
      color: var(--ink);
      border-radius: 8px;
      padding: 9px 12px;
      cursor: pointer;
      font-weight: 650;
      font-size: 13px;
    }}
    button.active {{
      background: var(--ink);
      color: #fff;
      border-color: var(--ink);
    }}
    select {{
      min-width: 210px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 9px 10px;
      font-size: 13px;
      color: var(--ink);
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 16px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      min-width: 0;
    }}
    .panel-head {{
      padding: 14px 16px 8px;
      border-bottom: 1px solid var(--line);
    }}
    h2 {{
      margin: 0;
      font-size: 15px;
      line-height: 1.3;
      font-weight: 750;
    }}
    .panel-note {{
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }}
    .panel-body {{ padding: 14px 16px 16px; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }}
    .world-strip {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 16px;
      margin-bottom: 16px;
    }}
    .validation-strip {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 16px;
      margin-bottom: 16px;
    }}
    .artifact-strip {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 16px;
      margin-bottom: 16px;
    }}
    .artifact-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 10px;
    }}
    .artifact-title {{
      font-size: 14px;
      font-weight: 760;
    }}
    .artifact-note {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      max-width: 760px;
    }}
    .artifact-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
    }}
    .artifact-card {{
      display: block;
      min-height: 90px;
      border: 1px solid #d7e2ef;
      border-radius: 8px;
      background: #f8fbff;
      padding: 10px;
      color: var(--ink);
      text-decoration: none;
    }}
    .artifact-card:hover {{
      border-color: var(--blue);
    }}
    .artifact-card strong {{
      display: block;
      font-size: 12px;
      line-height: 1.35;
    }}
    .artifact-card span {{
      display: block;
      margin-top: 6px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.4;
    }}
    .agent-strip {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 16px;
      margin-bottom: 16px;
    }}
    .agent-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 10px;
    }}
    .agent-title {{
      font-size: 14px;
      font-weight: 760;
    }}
    .agent-note {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      max-width: 780px;
    }}
    .agent-route {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: stretch;
      margin-bottom: 10px;
    }}
    .agent-step {{
      min-width: 118px;
      flex: 1 1 118px;
      border: 1px solid #cbdced;
      border-radius: 8px;
      background: #f8fbff;
      padding: 9px 10px;
      font-size: 12px;
      line-height: 1.35;
    }}
    .agent-step strong {{
      display: block;
      color: var(--blue);
      margin-bottom: 4px;
    }}
    .agent-skills {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
    }}
    .agent-skill {{
      border: 1px solid var(--line);
      border-left: 3px solid var(--green);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 10px;
      min-height: 122px;
    }}
    .agent-skill:nth-child(2n) {{ border-left-color: var(--blue); }}
    .agent-skill:nth-child(3n) {{ border-left-color: var(--amber); }}
    .agent-skill-id {{
      font-size: 12px;
      font-weight: 760;
      line-height: 1.35;
    }}
    .agent-skill-stage {{
      margin-top: 4px;
      color: var(--green);
      font-size: 11px;
      font-weight: 760;
    }}
    .agent-skill-purpose {{
      margin-top: 6px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.4;
    }}
    .packet-box {{
      margin-top: 10px;
      border: 1px solid #d9c7ee;
      border-radius: 8px;
      background: #fbf8ff;
      padding: 10px;
      font-size: 12px;
      line-height: 1.5;
    }}
    .packet-title {{
      color: var(--violet);
      font-weight: 800;
      margin-bottom: 6px;
    }}
    .packet-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
    }}
    .packet-cell {{
      background: #ffffff;
      border: 1px solid #e2d7f0;
      border-radius: 8px;
      padding: 8px;
      min-height: 82px;
    }}
    .packet-label {{
      color: var(--muted);
      font-size: 11px;
      font-weight: 760;
      margin-bottom: 4px;
    }}
    .research-strip {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 16px;
      margin-bottom: 16px;
    }}
    .research-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 10px;
    }}
    .research-title {{
      font-size: 14px;
      font-weight: 760;
    }}
    .research-note {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      max-width: 760px;
    }}
    .research-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
    }}
    .research-card {{
      border: 1px solid var(--line);
      border-top: 3px solid var(--blue);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 10px;
      min-height: 142px;
    }}
    .research-card:nth-child(2) {{ border-top-color: var(--green); }}
    .research-card:nth-child(3) {{ border-top-color: var(--amber); }}
    .research-card:nth-child(4) {{ border-top-color: var(--violet); }}
    .research-card:nth-child(5) {{ border-top-color: var(--red); }}
    .research-theme {{
      font-size: 12px;
      font-weight: 760;
      line-height: 1.35;
    }}
    .research-source {{
      margin-top: 4px;
      color: var(--blue);
      font-size: 11px;
      font-weight: 750;
    }}
    .research-move {{
      margin-top: 6px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.4;
    }}
    .validation-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 10px;
    }}
    .validation-title {{
      font-size: 14px;
      font-weight: 760;
    }}
    .validation-summary {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      max-width: 760px;
    }}
    .ledger-grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 10px;
    }}
    .ledger-card {{
      border: 1px solid var(--line);
      border-top: 3px solid var(--muted);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 10px;
      min-height: 132px;
    }}
    .ledger-card.pass {{ border-top-color: var(--green); }}
    .ledger-card.watch {{ border-top-color: var(--amber); }}
    .ledger-card.review {{ border-top-color: var(--violet); }}
    .ledger-card.hold {{ border-top-color: var(--red); }}
    .ledger-status {{
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--muted);
    }}
    .ledger-card.pass .ledger-status {{ color: var(--green); }}
    .ledger-card.watch .ledger-status {{ color: var(--amber); }}
    .ledger-card.review .ledger-status {{ color: var(--violet); }}
    .ledger-card.hold .ledger-status {{ color: var(--red); }}
    .ledger-title {{
      margin-top: 5px;
      font-size: 12px;
      font-weight: 760;
    }}
    .ledger-evidence {{
      margin-top: 6px;
      color: var(--ink);
      font-size: 12px;
      line-height: 1.4;
    }}
    .ledger-action {{
      margin-top: 7px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.4;
    }}
    .review-queue {{
      margin-top: 10px;
      border: 1px solid #d9c7ee;
      border-radius: 8px;
      background: #fbf8ff;
      padding: 10px;
    }}
    .review-title {{
      color: var(--violet);
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 7px;
    }}
    .review-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}
    .review-card {{
      background: #ffffff;
      border: 1px solid #e2d7f0;
      border-radius: 8px;
      padding: 9px;
      min-height: 112px;
    }}
    .review-card-name {{
      font-size: 12px;
      font-weight: 760;
      color: var(--ink);
    }}
    .review-card-meta {{
      margin-top: 4px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.4;
    }}
    .review-card-gate {{
      margin-top: 6px;
      color: var(--green);
      font-size: 11px;
      font-weight: 750;
      line-height: 1.4;
    }}
    .world-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 10px;
    }}
    .world-title {{
      font-size: 14px;
      font-weight: 760;
    }}
    .world-principle {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      max-width: 760px;
    }}
    .world-layers {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }}
    .world-layer {{
      border-top: 3px solid var(--blue);
      background: #fbfcfd;
      padding: 10px;
      min-height: 112px;
    }}
    .world-layer:nth-child(2) {{ border-top-color: var(--green); }}
    .world-layer:nth-child(3) {{ border-top-color: var(--amber); }}
    .world-layer:nth-child(4) {{ border-top-color: var(--violet); }}
    .world-layer-title {{
      font-size: 12px;
      font-weight: 760;
      margin-bottom: 5px;
    }}
    .world-layer-role {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }}
    .world-layer-artifact {{
      margin-top: 7px;
      font-size: 11px;
      color: var(--green);
      font-weight: 750;
    }}
    .platform-strip {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 16px;
      margin-bottom: 16px;
    }}
    .platform-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 10px;
    }}
    .platform-title {{
      font-size: 14px;
      font-weight: 760;
    }}
    .platform-claim {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      max-width: 780px;
    }}
    .platform-flow {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: stretch;
    }}
    .platform-node {{
      min-width: 128px;
      flex: 1 1 128px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 9px 10px;
      font-size: 12px;
      font-weight: 740;
      line-height: 1.35;
    }}
    .platform-node.core {{
      border-color: #b8d5cc;
      background: #eefaf5;
      color: #0f6b55;
    }}
    .platform-arrow {{
      display: grid;
      place-items: center;
      color: var(--green);
      font-size: 16px;
      font-weight: 800;
    }}
    .platform-boundary {{
      margin-top: 10px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }}
    .metric {{
      background: #f8fafc;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 11px 12px;
    }}
    .metric-label {{
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .metric-value {{
      margin-top: 5px;
      font-size: 20px;
      font-weight: 760;
    }}
    canvas {{
      display: block;
      width: 100%;
      background: #fbfcfd;
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    #networkCanvas {{ height: 360px; }}
    #seriesCanvas {{ height: 260px; }}
    .small-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 16px;
    }}
    .trace-list {{
      display: grid;
      gap: 10px;
    }}
    .trace-item {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #fbfcfd;
    }}
    .trace-stage {{
      font-size: 12px;
      color: var(--blue);
      font-weight: 760;
    }}
    .trace-artifact {{
      margin-top: 4px;
      font-size: 13px;
      line-height: 1.45;
    }}
    .trace-status {{
      margin-top: 5px;
      color: var(--muted);
      font-size: 12px;
    }}
    .bars {{
      display: grid;
      gap: 12px;
    }}
    .bar-row {{
      display: grid;
      grid-template-columns: 120px 1fr 54px;
      gap: 10px;
      align-items: center;
      font-size: 13px;
    }}
    .bar-track {{
      background: #edf1f5;
      border-radius: 999px;
      height: 10px;
      overflow: hidden;
    }}
    .bar {{
      height: 100%;
      border-radius: inherit;
      background: var(--green);
      width: 50%;
    }}
    .footer-note {{
      margin-top: 16px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.55;
    }}
    .wide-grid {{
      display: grid;
      grid-template-columns: 0.9fr 1.1fr;
      gap: 16px;
      margin-top: 16px;
    }}
    .contract-list, .next-list {{
      display: grid;
      gap: 10px;
    }}
    .contract-item {{
      display: grid;
      grid-template-columns: 108px 1fr;
      gap: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 11px 12px;
    }}
    .contract-label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 750;
    }}
    .contract-value {{
      color: var(--ink);
      font-size: 13px;
      line-height: 1.45;
    }}
    .next-item {{
      border-left: 3px solid var(--green);
      background: #fbfcfd;
      padding: 8px 10px;
      border-radius: 0 8px 8px 0;
      font-size: 13px;
      line-height: 1.45;
    }}
    .next-key {{
      color: var(--muted);
      font-weight: 750;
      margin-right: 4px;
    }}
    .rank-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 12px;
    }}
    .rank-table th,
    .rank-table td {{
      border-bottom: 1px solid var(--line);
      padding: 7px 5px;
      text-align: left;
      vertical-align: top;
    }}
    .rank-table th {{
      color: var(--muted);
      font-weight: 750;
      background: #f8fafc;
    }}
    .learning-summary {{
      margin-top: 12px;
      padding: 10px;
      background: #f8fafc;
      border: 1px solid var(--line);
      border-radius: 8px;
      font-size: 12px;
      line-height: 1.5;
      color: var(--muted);
    }}
    .signal-bars {{
      display: grid;
      gap: 9px;
      margin-top: 12px;
    }}
    .signal-row {{
      display: grid;
      grid-template-columns: 118px 1fr 48px;
      gap: 8px;
      align-items: center;
      font-size: 12px;
    }}
    .signal-track {{
      height: 8px;
      background: #edf1f5;
      border-radius: 999px;
      overflow: hidden;
    }}
    .signal-fill {{
      height: 100%;
      background: var(--blue);
      border-radius: inherit;
    }}
    .negative-evidence {{
      margin-top: 12px;
      border: 1px dashed #d5a495;
      border-radius: 8px;
      padding: 10px;
      background: #fff9f6;
      color: #7c3a2f;
      font-size: 12px;
      line-height: 1.5;
    }}
    .policy-controls {{
      margin-top: 12px;
      border: 1px solid #d7e2ef;
      border-radius: 8px;
      background: #f8fbff;
      padding: 10px;
    }}
    .policy-title {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      font-size: 12px;
      font-weight: 760;
      margin-bottom: 8px;
    }}
    .policy-note {{
      color: var(--muted);
      font-size: 11px;
      line-height: 1.45;
      margin-bottom: 8px;
    }}
    .weight-row {{
      display: grid;
      grid-template-columns: 104px 1fr 42px;
      gap: 8px;
      align-items: center;
      font-size: 11px;
      margin-top: 6px;
    }}
    input[type="range"] {{
      width: 100%;
      accent-color: var(--blue);
    }}
    .policy-summary {{
      margin-top: 8px;
      color: var(--green);
      font-size: 11px;
      font-weight: 750;
    }}
    .portfolio-map {{
      display: grid;
      gap: 10px;
      margin-top: 12px;
    }}
    .portfolio-action {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #fbfcfd;
    }}
    .portfolio-action-title {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      font-size: 12px;
      font-weight: 760;
      margin-bottom: 8px;
    }}
    .axis-row {{
      display: grid;
      grid-template-columns: 92px 1fr 38px;
      gap: 8px;
      align-items: center;
      font-size: 11px;
      margin-top: 5px;
    }}
    .axis-track {{
      height: 7px;
      border-radius: 999px;
      background: #edf1f5;
      overflow: hidden;
    }}
    .axis-fill {{
      height: 100%;
      border-radius: inherit;
      background: var(--green);
    }}
    .state-transition {{
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 10px;
      align-items: center;
      margin-top: 12px;
      font-size: 12px;
    }}
    .state-box {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 9px;
      background: #fbfcfd;
      min-height: 74px;
    }}
    .state-title {{
      color: var(--muted);
      font-weight: 750;
      margin-bottom: 5px;
    }}
    .state-arrow {{
      color: var(--green);
      font-weight: 800;
      font-size: 18px;
    }}
    @media (max-width: 960px) {{
      .core-intro, .workflow-mini, .grid, .toolbar, .small-grid, .wide-grid, .metrics, .world-layers, .ledger-grid, .review-grid, .artifact-grid, .agent-skills, .packet-grid, .research-grid {{
        grid-template-columns: 1fr;
      }}
      .title-row {{
        display: block;
      }}
      .status-pill {{
        display: inline-block;
        margin-top: 12px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="title-row">
      <div>
        <h1>NeuroTwin</h1>
        <div class="subtitle">Surrogate-driven AI4S demo for brain-system research: Design, Simulate, Validate, Learn.</div>
      </div>
      <div class="status-pill">DSVL virtual experiment</div>
    </div>
  </header>
  <main>
    <section class="core-intro">
      <div class="intro-card">
        <div class="intro-title">Core idea</div>
        <div class="intro-text">
          NeuroTwin packages a brain-system question as an AI4S workflow: evidence and task context enter Design, a surrogate brain runs virtual perturbations in Simulate, validation gates decide whether the result can advance, and Learn emits the next validation packet.
        </div>
      </div>
      <div class="intro-card">
        <div class="intro-title">What this Demo proves</div>
        <div class="intro-text">
          The page is a dry-run prototype. It uses synthetic ROI-level fMRI-like signals to show feasibility, workflow contracts, validation logic and cycle-to-cycle handoff without clinical or personal data.
        </div>
      </div>
    </section>

    <section class="toolbar">
      <div class="tabs" id="tabs"></div>
      <label>
        <select id="nodeSelect" aria-label="Perturbation source"></select>
      </label>
    </section>

    <section class="metrics" id="metrics"></section>

    <section class="platform-strip">
      <div class="platform-head">
        <div class="platform-title">AI4S Platform Route</div>
        <div class="platform-claim" id="platformClaim"></div>
      </div>
      <div class="platform-flow" id="platformFlow"></div>
      <div class="platform-boundary" id="platformBoundary"></div>
      <div class="workflow-mini">
        <div class="workflow-mini-step"><strong>Design</strong>Evidence cards, task objective, candidate perturbation.</div>
        <div class="workflow-mini-step"><strong>Simulate</strong>Surrogate dynamics, virtual perturbation, FC/EC response.</div>
        <div class="workflow-mini-step"><strong>Validate</strong>Signal fidelity, FC reproducibility, review gates.</div>
        <div class="workflow-mini-step"><strong>Learn</strong>Acquisition policy, negative evidence, next packet.</div>
      </div>
    </section>

    <section class="grid">
      <div class="panel">
        <div class="panel-head">
          <h2>Virtual Perturbation Map</h2>
          <div class="panel-note" id="scenarioText"></div>
        </div>
        <div class="panel-body">
          <canvas id="networkCanvas"></canvas>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head">
          <h2>DSVL Trace</h2>
          <div class="panel-note">Each run records how the hypothesis is designed, simulated, validated and learned into the next round.</div>
        </div>
        <div class="panel-body">
          <div class="trace-list" id="traceList"></div>
        </div>
      </div>
    </section>

    <section class="small-grid">
      <div class="panel">
        <div class="panel-head">
          <h2>Signal Simulation</h2>
          <div class="panel-note">Pre-intervention signal, surrogate prediction and post-intervention response.</div>
        </div>
        <div class="panel-body">
          <canvas id="seriesCanvas"></canvas>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head">
          <h2>Candidate Policy</h2>
          <div class="panel-note" id="objectiveText"></div>
        </div>
        <div class="panel-body">
          <div class="bars" id="bars"></div>
          <div class="footer-note">This synthetic demo does not make clinical claims. In a real deployment, each action would be tied to a dataset, model version, validation gate and human review record.</div>
        </div>
      </div>
    </section>

    <div class="folded-stack">
      <details class="collapsible">
        <summary>Validation gates and next-cycle handoff <span class="summary-note">Open for review ledger, review queue and learning packet details.</span></summary>
        <div class="collapsible-body">
          <section class="validation-strip">
            <div class="validation-head">
              <div class="validation-title">Validation Ledger</div>
              <div class="validation-summary" id="validationSummary"></div>
            </div>
            <div class="ledger-grid" id="validationLedger"></div>
            <div class="review-queue">
              <div class="review-title">Review Gate Queue</div>
              <div class="review-grid" id="reviewQueue"></div>
            </div>
          </section>
          <section class="wide-grid">
            <div class="panel">
              <div class="panel-head">
                <h2>Agent-Ready Capability</h2>
                <div class="panel-note">The workflow is specified as a callable scientific capability with contracts and validation gates.</div>
              </div>
              <div class="panel-body">
                <div class="contract-list" id="contractList"></div>
              </div>
            </div>

            <div class="panel">
              <div class="panel-head">
                <h2>Learn: Next Experiment Plan</h2>
                <div class="panel-note">Each virtual result updates the next hypothesis, uncertainty target and validation gate.</div>
              </div>
              <div class="panel-body">
                <div class="next-list" id="nextExperiment"></div>
                <div class="learning-summary" id="learningSummary"></div>
                <div class="signal-bars" id="signalBars"></div>
                <div class="policy-controls">
                  <div class="policy-title"><span>Programmable Acquisition Policy</span><span id="policyWeightTotal"></span></div>
                  <div class="policy-note">Adjust the operating preference and watch the acquisition portfolio rerank candidate virtual experiments.</div>
                  <div id="weightControls"></div>
                  <div class="policy-summary" id="policySummary"></div>
                </div>
                <div class="portfolio-map" id="portfolioMap"></div>
                <div class="state-transition" id="stateTransition"></div>
                <div class="negative-evidence" id="negativeEvidence"></div>
                <table class="rank-table" id="learningRank"></table>
              </div>
            </div>
          </section>
        </div>
      </details>

      <details class="collapsible">
        <summary>Workflow / Agent implementation details <span class="summary-note">Agent route, skill registry and active validation packet.</span></summary>
        <div class="collapsible-body">
          <section class="agent-strip">
            <div class="agent-head">
              <div class="agent-title">Agent Loop Route</div>
              <div class="agent-note">A platform Agent can route one scientific question from evidence reading to public validation and learning memory. The active scenario below emits a decision-ready packet for the next cycle.</div>
            </div>
            <div class="agent-route" id="agentRoute"></div>
            <div class="agent-skills" id="agentSkills"></div>
            <div class="packet-box">
              <div class="packet-title">Active Next Validation Packet</div>
              <div class="packet-grid" id="packetSummary"></div>
            </div>
          </section>
        </div>
      </details>

      <details class="collapsible">
        <summary>Evidence, virtual world and submission artifacts <span class="summary-note">Supporting materials are folded to keep the main demo focused.</span></summary>
        <div class="collapsible-body">
          <section class="research-strip">
            <div class="research-head">
              <div class="research-title">Evidence Backbone</div>
              <div class="research-note">Literature and infrastructure cues translated into concrete design moves. Full notes are in <a href="literature_research_brief.md">literature_research_brief.md</a>; structured cards are in <a href="evidence_cards.json">evidence_cards.json</a>.</div>
            </div>
            <div class="research-grid" id="researchBackbone"></div>
          </section>

          <section class="world-strip">
            <div class="world-head">
              <div class="world-title">Virtual Experimental World</div>
              <div class="world-principle" id="worldPrinciple"></div>
            </div>
            <div class="world-layers" id="worldLayers"></div>
          </section>

          <section class="artifact-strip">
            <div class="artifact-head">
              <div class="artifact-title">Public Validation Artifacts</div>
              <div class="artifact-note">Generated by <code>scripts/prepare_public_validation.py</code>. The focused smoke-test files show how one review gate becomes an executable validation preparation packet.</div>
            </div>
            <div class="artifact-grid">
              <a class="artifact-card" href="public_validation_runbook.md"><strong>Full Runbook</strong><span>All scenarios and all public-data validation tiers.</span></a>
              <a class="artifact-card" href="public_validation_manifest.json"><strong>Full Manifest</strong><span>Machine-readable input, tool and artifact contract.</span></a>
              <a class="artifact-card" href="public_validation_openneuro_smoke_runbook.md"><strong>OpenNeuro Smoke Runbook</strong><span>One scenario, P1 review gate and minimum BIDS path.</span></a>
              <a class="artifact-card" href="public_validation_openneuro_smoke_manifest.json"><strong>OpenNeuro Smoke Manifest</strong><span>Focused manifest for the first public validation step.</span></a>
              <a class="artifact-card" href="public_validation_protocol_template.md"><strong>Validation Protocol</strong><span>BIDS, preprocessing, atlas, split and QC template.</span></a>
              <a class="artifact-card" href="public_validation_openneuro_smoke_protocol_template.md"><strong>OpenNeuro Smoke Protocol</strong><span>Focused P1 protocol template for the first dry validation.</span></a>
              <a class="artifact-card" href="evidence_cards.json"><strong>Evidence Cards</strong><span>Structured literature-to-Design cards for DSVL inputs.</span></a>
              <a class="artifact-card" href="evidence_card_schema.md"><strong>Evidence Card Schema</strong><span>Interface contract for literature mining outputs.</span></a>
              <a class="artifact-card" href="agent_skill_registry.md"><strong>Agent Skill Registry</strong><span>Tool route for Read, Prepare, Build, Compute, Validate and Learn.</span></a>
              <a class="artifact-card" href="next_validation_packet.md"><strong>Next Validation Packet</strong><span>Human-readable handoff object for the next AI4S loop.</span></a>
              <a class="artifact-card" href="next_validation_packet.json"><strong>Packet JSON</strong><span>Machine-readable scenario packets for Agent routing.</span></a>
            </div>
          </section>
        </div>
      </details>
    </div>
  </main>

  <script>
    const payload = {payload_json};
    const colors = ["#2563eb", "#0f8b6f", "#b45309", "#6d5bd0", "#c24132", "#0891b2", "#4b5563", "#be6a15"];
    const shortLabels = ["Visual", "Attention", "FPN", "DMN", "Limbic", "Salience", "Motor", "Subcort."];
    const axisLabels = {{
      fidelity: "Fidelity",
      objective_alignment: "Objective",
      novelty: "Novelty",
      feasibility: "Feasible",
      risk_control: "Risk ctrl",
    }};
    let activeKey = Object.keys(payload.scenarios)[0];
    let activeNode = 0;
    let policyWeights = {{ ...payload.acquisition_policy.portfolio_weights }};

    const tabs = document.getElementById("tabs");
    const nodeSelect = document.getElementById("nodeSelect");
    const metricsEl = document.getElementById("metrics");
    const traceList = document.getElementById("traceList");
    const scenarioText = document.getElementById("scenarioText");
    const objectiveText = document.getElementById("objectiveText");
    const bars = document.getElementById("bars");
    const validationSummary = document.getElementById("validationSummary");
    const validationLedger = document.getElementById("validationLedger");
    const reviewQueue = document.getElementById("reviewQueue");
    const worldPrinciple = document.getElementById("worldPrinciple");
    const worldLayers = document.getElementById("worldLayers");
    const platformClaim = document.getElementById("platformClaim");
    const platformFlow = document.getElementById("platformFlow");
    const platformBoundary = document.getElementById("platformBoundary");
    const researchBackbone = document.getElementById("researchBackbone");
    const agentRoute = document.getElementById("agentRoute");
    const agentSkills = document.getElementById("agentSkills");
    const packetSummary = document.getElementById("packetSummary");
    const contractList = document.getElementById("contractList");
    const nextExperiment = document.getElementById("nextExperiment");
    const learningSummary = document.getElementById("learningSummary");
    const signalBars = document.getElementById("signalBars");
    const weightControls = document.getElementById("weightControls");
    const policyWeightTotal = document.getElementById("policyWeightTotal");
    const policySummary = document.getElementById("policySummary");
    const portfolioMap = document.getElementById("portfolioMap");
    const learningRank = document.getElementById("learningRank");
    const stateTransition = document.getElementById("stateTransition");
    const negativeEvidence = document.getElementById("negativeEvidence");
    const networkCanvas = document.getElementById("networkCanvas");
    const seriesCanvas = document.getElementById("seriesCanvas");

    function setup() {{
      Object.entries(payload.scenarios).forEach(([key, scenario]) => {{
        const button = document.createElement("button");
        button.textContent = scenario.name;
        button.addEventListener("click", () => {{
          activeKey = key;
          render();
        }});
        tabs.appendChild(button);
      }});
      payload.networks.forEach((name, index) => {{
        const option = document.createElement("option");
        option.value = String(index);
        option.textContent = `Perturb: ${{name}}`;
        nodeSelect.appendChild(option);
      }});
      nodeSelect.addEventListener("change", () => {{
        activeNode = Number(nodeSelect.value);
        render();
      }});
      renderWorldLayers();
      renderPlatformArchitecture();
      renderAgentLoop();
      renderResearchBackbone();
      renderPolicyControls();
      renderTrace();
      render();
    }}

    function fitCanvas(canvas) {{
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.round(rect.width * dpr);
      canvas.height = Math.round(rect.height * dpr);
      const ctx = canvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return {{ ctx, width: rect.width, height: rect.height }};
    }}

    function render() {{
      [...tabs.children].forEach((button, index) => {{
        button.classList.toggle("active", Object.keys(payload.scenarios)[index] === activeKey);
      }});
      nodeSelect.value = String(activeNode);
      const scenario = payload.scenarios[activeKey];
      scenarioText.textContent = scenario.description;
      objectiveText.textContent = scenario.objective;
      renderMetrics(scenario);
      renderValidationLedger(scenario);
      renderNetwork(scenario);
      renderSeries(scenario);
      renderBars(scenario);
      renderContract();
      renderNextExperiment(scenario);
      renderNextValidationPacket();
      renderLearningRank(scenario);
      renderSignalBars(scenario);
      renderPortfolioMap(scenario);
      renderStateTransition(scenario);
    }}

    function normalizedWeights() {{
      const total = Object.values(policyWeights).reduce((sum, value) => sum + value, 0) || 1;
      const normalized = {{}};
      Object.entries(policyWeights).forEach(([key, value]) => {{
        normalized[key] = value / total;
      }});
      return {{ total, normalized }};
    }}

    function scoreWithWeights(profile) {{
      const {{ normalized }} = normalizedWeights();
      return Object.entries(normalized).reduce((sum, [key, weight]) => sum + weight * profile[key], 0);
    }}

    function portfolioRanking(scenario) {{
      return scenario.learning_update.ranked_actions
        .map(item => ({{ ...item, weighted_score: scoreWithWeights(item.multi_objective) }}))
        .sort((a, b) => b.weighted_score - a.weighted_score);
    }}

    function renderPolicyControls() {{
      weightControls.innerHTML = "";
      Object.entries(policyWeights).forEach(([key, value]) => {{
        const row = document.createElement("div");
        row.className = "weight-row";
        row.innerHTML = `<div>${{axisLabels[key]}}</div><input type="range" min="0" max="60" step="1" value="${{Math.round(value * 100)}}" aria-label="${{axisLabels[key]}} weight"><div>${{value.toFixed(2)}}</div>`;
        const input = row.querySelector("input");
        const label = row.querySelector("div:last-child");
        input.addEventListener("input", () => {{
          policyWeights[key] = Number(input.value) / 100;
          label.textContent = policyWeights[key].toFixed(2);
          render();
        }});
        weightControls.appendChild(row);
      }});
    }}

    function renderPlatformArchitecture() {{
      const architecture = payload.platform_architecture;
      platformClaim.textContent = architecture.claim;
      platformFlow.innerHTML = "";
      architecture.nodes.forEach((node, index) => {{
        const block = document.createElement("div");
        const isCore = node === "NeuroTwin virtual world" || node === "Programmable acquisition policy";
        block.className = `platform-node${{isCore ? " core" : ""}}`;
        block.textContent = node;
        platformFlow.appendChild(block);
        if (index < architecture.nodes.length - 1) {{
          const arrow = document.createElement("div");
          arrow.className = "platform-arrow";
          arrow.textContent = "→";
          platformFlow.appendChild(arrow);
        }}
      }});
      platformBoundary.textContent = payload.data_interface_boundary.principle;
    }}

    function renderResearchBackbone() {{
      researchBackbone.innerHTML = "";
      payload.research_backbone.forEach(item => {{
        const block = document.createElement("div");
        block.className = "research-card";
        block.innerHTML = `<div class="research-theme">${{item.theme}}</div><div class="research-source">${{item.source}}</div><div class="research-move">${{item.project_move}}</div>`;
        researchBackbone.appendChild(block);
      }});
    }}

    function renderAgentLoop() {{
      agentRoute.innerHTML = "";
      payload.agent_loop_route.steps.forEach(step => {{
        const block = document.createElement("div");
        block.className = "agent-step";
        block.innerHTML = `<strong>${{step.step}}</strong>${{step.agent_action}}`;
        agentRoute.appendChild(block);
      }});
      agentSkills.innerHTML = "";
      payload.agent_skill_registry.forEach(skill => {{
        const block = document.createElement("div");
        block.className = "agent-skill";
        block.innerHTML = `<div class="agent-skill-id">${{skill.skill_id}}</div><div class="agent-skill-stage">${{skill.stage}}</div><div class="agent-skill-purpose">${{skill.purpose}}</div>`;
        agentSkills.appendChild(block);
      }});
    }}

    function renderNextValidationPacket() {{
      const packet = payload.next_validation_packets[activeKey];
      const cards = packet.linked_evidence_cards.map(item => item.card_id).join(", ");
      const action = packet.learn_stage_action;
      const candidate = packet.public_validation_candidate;
      const metrics = packet.current_metric_snapshot;
      const rows = [
        ["Packet", packet.packet_id],
        ["Evidence", cards],
        ["Agent route", packet.agent_skill_route.slice(0, 4).join(" -> ") + " -> ..."],
        ["Validation", `P${{candidate.priority}} ${{candidate.action}}`],
        ["Readiness", `${{metrics.readiness_score}} · ${{metrics.routing}}`],
        ["Learn action", `${{action.top_action}} · ${{action.priority_score}}`],
        ["Required outputs", packet.required_outputs.slice(0, 3).join("; ") + "; ..."],
        ["Decision rule", packet.decision_rule],
      ];
      packetSummary.innerHTML = rows.map(([label, value]) => `
        <div class="packet-cell">
          <div class="packet-label">${{label}}</div>
          <div>${{value}}</div>
        </div>
      `).join("");
    }}

    function renderWorldLayers() {{
      const world = payload.virtual_experiment_world;
      worldPrinciple.textContent = world.principle;
      worldLayers.innerHTML = "";
      world.layers.forEach(item => {{
        const block = document.createElement("div");
        block.className = "world-layer";
        block.innerHTML = `<div class="world-layer-title">${{item.layer}}</div><div class="world-layer-role">${{item.role}}</div><div class="world-layer-artifact">${{item.artifact}}</div>`;
        worldLayers.appendChild(block);
      }});
    }}

    function renderTrace() {{
      traceList.innerHTML = "";
      payload.trace.forEach(item => {{
        const row = document.createElement("div");
        row.className = "trace-item";
        row.innerHTML = `<div class="trace-stage">${{item.stage}}</div><div class="trace-artifact">${{item.artifact}}</div><div class="trace-status">${{item.status}}</div>`;
        traceList.appendChild(row);
      }});
    }}

    function renderMetrics(scenario) {{
      const items = [
        ["BOLD R2", scenario.metrics.bold_r2],
        ["FC Corr", scenario.metrics.fc_corr],
        ["Objective", scenario.metrics.objective_delta],
        ["Trace Steps", payload.trace.length],
      ];
      metricsEl.innerHTML = "";
      items.forEach(([label, value]) => {{
        const card = document.createElement("div");
        card.className = "metric";
        card.innerHTML = `<div class="metric-label">${{label}}</div><div class="metric-value">${{value}}</div>`;
        metricsEl.appendChild(card);
      }});
    }}

    function renderValidationLedger(scenario) {{
      const ledger = scenario.validation_ledger;
      const summary = ledger.summary;
      validationSummary.textContent = `${{summary.routing}} | readiness ${{summary.readiness_score}} | pass ${{summary.pass}}, watch ${{summary.watch}}, review ${{summary.review}}, hold ${{summary.hold}}.`;
      validationLedger.innerHTML = "";
      ledger.gates.forEach(item => {{
        const card = document.createElement("div");
        card.className = `ledger-card ${{item.status}}`;
        card.innerHTML = `<div class="ledger-status">${{item.status}}</div><div class="ledger-title">${{item.gate}}</div><div class="ledger-evidence">${{item.evidence}}</div><div class="ledger-action">${{item.next_control}}</div>`;
        validationLedger.appendChild(card);
      }});
      reviewQueue.innerHTML = "";
      ledger.review_queue.forEach(task => {{
        const card = document.createElement("div");
        card.className = "review-card";
        card.innerHTML = `<div class="review-card-name">P${{task.priority}}. ${{task.action}}</div><div class="review-card-meta">${{task.dataset}} · ${{task.task}}</div><div class="review-card-gate">${{task.success_gate}}</div>`;
        reviewQueue.appendChild(card);
      }});
    }}

    function renderContract() {{
      const cap = payload.capability;
      const items = [
        ["Capability", `${{cap.name}} / ${{cap.version}}`],
        ["Inputs", cap.input_contract.join("; ")],
        ["Outputs", cap.output_contract.join("; ")],
        ["Gates", cap.validation_gates.join("; ")],
        ["Platform", cap.platform_fit.join("; ")],
      ];
      contractList.innerHTML = "";
      items.forEach(([label, value]) => {{
        const row = document.createElement("div");
        row.className = "contract-item";
        row.innerHTML = `<div class="contract-label">${{label}}</div><div class="contract-value">${{value}}</div>`;
        contractList.appendChild(row);
      }});
    }}

    function renderNextExperiment(scenario) {{
      const next = scenario.next_experiment;
      const rows = [
        ["Hypothesis", next.hypothesis],
        ["Dry run", next.dry_run],
        ["Human check", next.wet_or_human_check],
        ["Success gate", next.success_gate],
      ];
      nextExperiment.innerHTML = "";
      rows.forEach(([label, value]) => {{
        const row = document.createElement("div");
        row.className = "next-item";
        row.innerHTML = `<span class="next-key">${{label}}:</span>${{value}}`;
        nextExperiment.appendChild(row);
      }});
    }}

    function renderLearningRank(scenario) {{
      const learning = scenario.learning_update;
      const portfolioTop = portfolioRanking(scenario)[0];
      const {{ total }} = normalizedWeights();
      policyWeightTotal.textContent = `weight sum ${{total.toFixed(2)}}`;
      policySummary.textContent = `Current portfolio route: ${{portfolioTop.action}} (weighted score ${{portfolioTop.weighted_score.toFixed(4)}}).`;
      learningSummary.textContent = `Learn signals: uncertainty ${{learning.uncertainty}}, FC gap ${{learning.fc_gap}}, perturbation cost ${{learning.intervention_cost}}. Top priority action: ${{learning.top_action}}.`;
      learningRank.innerHTML = "<thead><tr><th>Rank</th><th>Next simulation</th><th>Info</th><th>Cost</th><th>Priority</th><th>Weighted</th></tr></thead>";
      const body = document.createElement("tbody");
      portfolioRanking(scenario).slice(0, 3).forEach((item, index) => {{
        const row = document.createElement("tr");
        row.innerHTML = `<td>${{index + 1}}</td><td>${{item.action}}<br><span style="color:#64707d">${{item.why}}</span></td><td>${{item.expected_information_gain}}</td><td>${{item.validation_cost}}</td><td>${{item.priority_score}}</td><td>${{item.weighted_score.toFixed(4)}}</td>`;
        body.appendChild(row);
      }});
      learningRank.appendChild(body);
    }}

    function renderSignalBars(scenario) {{
      const colors = ["#2563eb", "#0891b2", "#0f8b6f", "#b45309"];
      signalBars.innerHTML = "";
      scenario.learning_update.signal_bars.forEach((item, index) => {{
        const row = document.createElement("div");
        row.className = "signal-row";
        const width = Math.max(4, Math.round(item.scaled * 100));
        row.innerHTML = `<div>${{item.label}}</div><div class="signal-track"><div class="signal-fill" style="width:${{width}}%; background:${{colors[index % colors.length]}}"></div></div><div>${{item.value}}</div>`;
        signalBars.appendChild(row);
      }});
    }}

    function renderPortfolioMap(scenario) {{
      const axes = [
        ["fidelity", "Fidelity"],
        ["objective_alignment", "Objective"],
        ["novelty", "Novelty"],
        ["feasibility", "Feasible"],
        ["risk_control", "Risk ctrl"],
      ];
      const axisColors = ["#2563eb", "#0f8b6f", "#6d5bd0", "#b45309", "#0891b2"];
      portfolioMap.innerHTML = "";
      portfolioRanking(scenario).slice(0, 2).forEach((item, index) => {{
        const profile = item.multi_objective;
        const block = document.createElement("div");
        block.className = "portfolio-action";
        const axisRows = axes.map(([key, label], axisIndex) => {{
          const value = profile[key];
          const width = Math.max(4, Math.round(value * 100));
          return `<div class="axis-row"><div>${{label}}</div><div class="axis-track"><div class="axis-fill" style="width:${{width}}%; background:${{axisColors[axisIndex]}}"></div></div><div>${{value}}</div></div>`;
        }}).join("");
        block.innerHTML = `<div class="portfolio-action-title"><span>${{index + 1}}. ${{item.action}}</span><span>weighted ${{item.weighted_score.toFixed(4)}} / base ${{profile.portfolio_score}}</span></div>${{axisRows}}`;
        portfolioMap.appendChild(block);
      }});
    }}

    function renderStateTransition(scenario) {{
      const learning = scenario.learning_update;
      const top = portfolioRanking(scenario)[0];
      const currentState = `R2 ${{scenario.metrics.bold_r2}}, FC ${{scenario.metrics.fc_corr}}, objective ${{scenario.metrics.objective_delta}}`;
      const nextState = `${{top.action}}; weighted ${{top.weighted_score.toFixed(4)}}, cost ${{top.validation_cost}}`;
      stateTransition.innerHTML = `<div class="state-box"><div class="state-title">Current evidence</div>${{currentState}}</div><div class="state-arrow">→</div><div class="state-box"><div class="state-title">Next run</div>${{nextState}}</div>`;
      const rejected = learning.negative_evidence.map(item => `${{item.action}} (${{item.priority_score}})`).join("; ");
      negativeEvidence.innerHTML = `<strong>Negative evidence:</strong> lower-priority actions logged for routing update: ${{rejected}}.`;
    }}

    function renderNetwork(scenario) {{
      const {{ ctx, width, height }} = fitCanvas(networkCanvas);
      ctx.clearRect(0, 0, width, height);
      const cx = width / 2;
      const cy = height / 2;
      const radius = Math.min(width, height) * 0.34;
      const nodes = payload.networks.map((name, i) => {{
        const angle = -Math.PI / 2 + i * 2 * Math.PI / payload.networks.length;
        return {{ name, x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle), color: colors[i % colors.length] }};
      }});

      ctx.lineCap = "round";
      const ec = scenario.effective_connectivity[activeNode];
      ec.forEach((value, target) => {{
        if (target === activeNode || Math.abs(value) < 0.015) return;
        const from = nodes[activeNode];
        const to = nodes[target];
        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.lineTo(to.x, to.y);
        ctx.strokeStyle = value >= 0 ? "rgba(15, 139, 111, 0.72)" : "rgba(194, 65, 50, 0.72)";
        ctx.lineWidth = 1.5 + Math.min(7, Math.abs(value) * 38);
        ctx.stroke();
        const midX = from.x * 0.35 + to.x * 0.65;
        const midY = from.y * 0.35 + to.y * 0.65;
        ctx.beginPath();
        ctx.arc(midX, midY, 4, 0, Math.PI * 2);
        ctx.fillStyle = ctx.strokeStyle;
        ctx.fill();
      }});

      nodes.forEach((node, i) => {{
        ctx.beginPath();
        ctx.arc(node.x, node.y, i === activeNode ? 19 : 15, 0, Math.PI * 2);
        ctx.fillStyle = i === activeNode ? "#17202a" : node.color;
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();
        ctx.fillStyle = "#17202a";
        ctx.font = "12px Inter, sans-serif";
        ctx.textAlign = "center";
        const labelY = node.y > cy ? node.y + 32 : node.y - 24;
        const labelX = Math.max(38, Math.min(width - 38, node.x));
        ctx.fillText(shortLabels[i], labelX, labelY);
      }});

      ctx.fillStyle = "#64707d";
      ctx.font = "12px Inter, sans-serif";
      ctx.textAlign = "left";
      ctx.fillText("Green: excitatory virtual response", 14, height - 28);
      ctx.fillText("Red: inhibitory virtual response", 14, height - 12);
    }}

    function renderSeries(scenario) {{
      const {{ ctx, width, height }} = fitCanvas(seriesCanvas);
      ctx.clearRect(0, 0, width, height);
      const pad = 28;
      const source = activeNode;
      const raw = scenario.series.map(row => row[source]);
      const pred = scenario.prediction.map(row => row[source]);
      const post = scenario.post_series.map(row => row[source]);
      const all = raw.concat(pred).concat(post);
      const min = Math.min(...all) - 0.08;
      const max = Math.max(...all) + 0.08;

      function xy(i, value) {{
        return [
          pad + (i / (raw.length - 1)) * (width - pad * 2),
          height - pad - ((value - min) / (max - min)) * (height - pad * 2)
        ];
      }}
      function drawLine(values, color, widthLine) {{
        ctx.beginPath();
        values.forEach((value, i) => {{
          const [x, y] = xy(i, value);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }});
        ctx.strokeStyle = color;
        ctx.lineWidth = widthLine;
        ctx.stroke();
      }}

      ctx.strokeStyle = "#dce2e8";
      ctx.lineWidth = 1;
      for (let i = 0; i < 5; i++) {{
        const y = pad + i * (height - pad * 2) / 4;
        ctx.beginPath();
        ctx.moveTo(pad, y);
        ctx.lineTo(width - pad, y);
        ctx.stroke();
      }}
      drawLine(raw, "#2563eb", 2.2);
      drawLine(pred, "#0f8b6f", 1.8);
      drawLine(post, "#c24132", 1.8);

      ctx.fillStyle = "#17202a";
      ctx.font = "12px Inter, sans-serif";
      ctx.fillText(payload.networks[source], pad, 17);
      [["signal", "#2563eb"], ["surrogate", "#0f8b6f"], ["post", "#c24132"]].forEach(([label, color], i) => {{
        ctx.fillStyle = color;
        ctx.fillRect(width - 180 + i * 58, 10, 12, 12);
        ctx.fillStyle = "#64707d";
        ctx.fillText(label, width - 164 + i * 58, 20);
      }});
    }}

    function renderBars(scenario) {{
      const rows = [
        ["Limbic drop", scenario.metrics.limbic_drop, "#c24132"],
        ["Control gain", scenario.metrics.control_gain, "#2563eb"],
        ["Salience drop", scenario.metrics.salience_drop, "#0f8b6f"],
        ["Objective delta", scenario.metrics.objective_delta, "#b45309"],
      ];
      const maxAbs = Math.max(...rows.map(row => Math.abs(row[1])), 0.01);
      bars.innerHTML = "";
      rows.forEach(([label, value, color]) => {{
        const width = 50 + (value / maxAbs) * 45;
        const row = document.createElement("div");
        row.className = "bar-row";
        row.innerHTML = `<div>${{label}}</div><div class="bar-track"><div class="bar" style="width:${{Math.max(4, Math.min(96, width))}}%; background:${{color}}"></div></div><div>${{Number(value).toFixed(3)}}</div>`;
        bars.appendChild(row);
      }});
    }}

    window.addEventListener("resize", render);
    setup();
  </script>
</body>
</html>
"""
    (DIST / "brain_twin_lab.html").write_text(html, encoding="utf-8")


def write_favicon() -> None:
    """Write a tiny transparent ICO so static preview servers avoid favicon 404 noise."""
    icon_hex = (
        "00000100010001010000010020003000000016000000"
        "280000000100000002000000010020000000000004000000"
        "000000000000000000000000000000000000000000000000"
        "00000000"
    )
    (DIST / "favicon.ico").write_bytes(bytes.fromhex(icon_hex))


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    (DIST / "demo_data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_dashboard(payload)
    write_report(payload)
    write_data_card()
    write_validation_ledger_note(payload)
    write_public_validation_bridge_note(payload)
    write_literature_research_brief(payload)
    write_evidence_cards(payload)
    write_agent_skill_registry(payload)
    write_next_validation_packets(payload)
    write_capability_card(payload)
    write_trace_jsonl(payload)
    write_next_experiment_plan(payload)
    write_scientific_loop_note(payload)
    write_theoretical_model_note()
    write_acquisition_policy_note(payload)
    write_virtual_experiment_world_note(payload)
    write_experiment_os_policy_note(payload)
    write_data_interface_boundary_note(payload)
    write_platform_architecture_note(payload)
    write_favicon()
    print(f"Wrote demo artifacts to {DIST}")


if __name__ == "__main__":
    main()
