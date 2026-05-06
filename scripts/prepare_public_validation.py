"""Prepare the public-data validation scaffold for NeuroTwin.

Run:
    python scripts/prepare_public_validation.py

Optional:
    python scripts/prepare_public_validation.py --accession ds000001 --dataset-root data/openneuro/ds000001
    python scripts/prepare_public_validation.py --scenario emotion --tier 1 --output-prefix public_validation_openneuro_smoke

This script does not download data. It converts the review-gate queue in
`artifacts/demo/demo_data.json` into an executable manifest and a runbook.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "artifacts" / "demo"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a public validation manifest from the NeuroTwin review queue.")
    parser.add_argument("--payload", default=str(DIST / "demo_data.json"), help="Path to generated demo_data.json.")
    parser.add_argument(
        "--accession", default="<openneuro_accession>", help="OpenNeuro accession placeholder, e.g. ds000001."
    )
    parser.add_argument("--dataset-root", default="<local_bids_root>", help="Local BIDS dataset root or placeholder.")
    parser.add_argument("--output-dir", default=str(DIST), help="Directory for manifest and runbook outputs.")
    parser.add_argument("--output-prefix", default="public_validation", help="Output filename prefix.")
    parser.add_argument("--scenario", default="all", help="Scenario key or name to include, or all.")
    parser.add_argument("--tier", default="all", help="Review tier priority or action name to include, or all.")
    return parser.parse_args()


def load_payload(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing payload: {path}. Run `python scripts/run_demo.py` first.")
    return json.loads(path.read_text(encoding="utf-8"))


def dataset_status(dataset_root: str) -> dict:
    if dataset_root.startswith("<") and dataset_root.endswith(">"):
        return {
            "state": "placeholder",
            "dataset_root": dataset_root,
            "dataset_description": "not checked",
        }
    root = Path(dataset_root).expanduser()
    description = root / "dataset_description.json"
    return {
        "state": "present" if root.exists() else "missing",
        "dataset_root": str(root),
        "dataset_description": "present" if description.exists() else "missing",
    }


def normalize_token(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def is_all(value: str) -> bool:
    return normalize_token(value) in {"all", "*", ""}


def scenario_matches(key: str, scenario: dict, scenario_filter: str) -> bool:
    if is_all(scenario_filter):
        return True
    selected = normalize_token(scenario_filter)
    candidates = {
        normalize_token(key),
        normalize_token(scenario["name"]),
    }
    return selected in candidates


def task_matches_tier(task: dict, tier_filter: str) -> bool:
    if is_all(tier_filter):
        return True
    selected = normalize_token(tier_filter)
    candidates = {
        normalize_token(task["priority"]),
        normalize_token(task["action"]),
    }
    return selected in candidates


def scenario_review_summary(payload: dict, scenario_filter: str, tier_filter: str) -> list[dict]:
    rows = []
    for key, scenario in payload["scenarios"].items():
        if not scenario_matches(key, scenario, scenario_filter):
            continue
        ledger = scenario["validation_ledger"]
        review_tasks = [task for task in ledger["review_queue"] if task_matches_tier(task, tier_filter)]
        if not review_tasks:
            continue
        rows.append(
            {
                "scenario_key": key,
                "scenario": scenario["name"],
                "routing": ledger["summary"]["routing"],
                "readiness_score": ledger["summary"]["readiness_score"],
                "review_tasks": review_tasks,
            }
        )
    return rows


def filter_bridge(payload: dict, rows: list[dict]) -> dict:
    bridge = payload["public_validation_bridge"]
    selected_actions = {task["action"] for row in rows for task in row["review_tasks"]}
    return {
        **bridge,
        "tiers": [tier for tier in bridge["tiers"] if tier["name"] in selected_actions],
    }


def validation_readiness_requirements() -> list[dict]:
    return [
        {
            "area": "BIDS compliance",
            "check": "Run validator JSON output and record dataset_description, participants.tsv and task event files.",
            "reason": "Public fMRI validation must start from a reusable data contract.",
        },
        {
            "area": "ROI extraction QC",
            "check": "Record atlas version, missing ROI rate, temporal length, nuisance regression choices and failed subjects.",
            "reason": "Surrogate metrics are only interpretable when representation quality is visible.",
        },
        {
            "area": "Motion and site effects",
            "check": "Record framewise displacement summary, censoring rule, scanner/site labels and split strategy.",
            "reason": "Large neuroimaging cohorts can reward confounds if QC is mixed with model score.",
        },
        {
            "area": "Behavior endpoint",
            "check": "Attach task accuracy, reaction time, clinical scale or human-review endpoint when available.",
            "reason": "Network-level shifts need an external objective for scientific interpretation.",
        },
        {
            "area": "Repeatability",
            "check": "Save seeds, model version, feature schema, validation split and negative evidence.",
            "reason": "Self-driving lab style loops require replayable decisions and failed-run memory.",
        },
    ]


def validation_protocol_template(accession: str, dataset_root: str, scenario_filter: str, tier_filter: str) -> dict:
    return {
        "protocol_name": "NeuroTwin public fMRI validation protocol template",
        "mode": "dry-template",
        "no_download_performed": True,
        "openneuro_dry_example": {
            "accession": accession,
            "dataset_root": dataset_root,
            "download_command": f"openneuro download {accession} {dataset_root}",
            "note": "Replace placeholders with a selected public dataset. The script records the command template only.",
        },
        "scope": {
            "scenario_filter": scenario_filter,
            "tier_filter": tier_filter,
        },
        "bids_contract": {
            "required_files": [
                "dataset_description.json",
                "participants.tsv",
                "task events.tsv for each selected BOLD run",
            ],
            "validator_command": "bids-validator-deno <dataset root> --json",
            "source": "https://bids-specification.readthedocs.io/",
        },
        "preprocessing_contract": {
            "recommended_derivative": "fMRIPrep outputs when available",
            "confounds_to_record": [
                "framewise_displacement",
                "dvars",
                "motion_outliers or censoring columns when available",
                "scanner/site/session labels when available",
            ],
            "source": "https://fmriprep.org/en/stable/outputs.html",
        },
        "atlas_contract": {
            "space": "MNI152NLin2009cAsym or dataset-native space with explicit transform record",
            "atlas_name": "<atlas_name>",
            "roi_labels": "<roi_labels.tsv>",
            "extraction_tool": "Nilearn NiftiLabelsMasker or equivalent audited extractor",
            "aggregation": "mean signal per ROI after mask and confound handling",
            "minimum_timepoints": 120,
            "max_missing_roi_fraction": 0.05,
            "source": "https://nilearn.github.io/stable/modules/generated/nilearn.maskers.NiftiLabelsMasker.html",
        },
        "split_policy": {
            "primary_split": "subject-level train/validation/test split",
            "fallback_split": "session-level split only when subject count is insufficient and leakage is documented",
            "stratify_by": ["task", "site/scanner when available", "age/sex or cohort label when available"],
            "fixed_seed": 20260501,
            "leakage_rule": "No subject can appear in both train and test.",
        },
        "qc_thresholds": {
            "mean_fd_watch_mm": 0.20,
            "mean_fd_review_mm": 0.30,
            "max_high_motion_fraction": 0.25,
            "min_bold_r2_for_pass": 0.70,
            "min_fc_corr_for_pass": 0.75,
            "threshold_note": "Motion thresholds are proposed review defaults for this demo and should be adapted per dataset.",
        },
        "required_outputs": [
            "BIDS validator JSON",
            "ROI extraction QC table",
            "subject split file",
            "motion/site/scanner summary",
            "behavior endpoint alignment note",
            "updated Validation Ledger",
            "updated acquisition portfolio",
        ],
    }


def build_manifest(payload: dict, accession: str, dataset_root: str, scenario_filter: str, tier_filter: str) -> dict:
    rows = scenario_review_summary(payload, scenario_filter, tier_filter)
    if not rows:
        raise ValueError(f"No review tasks matched scenario={scenario_filter!r}, tier={tier_filter!r}.")
    bridge = filter_bridge(payload, rows)
    return {
        "project": payload["project"],
        "mode": "public-validation-scaffold",
        "no_download_performed": True,
        "source_payload": "artifacts/demo/demo_data.json",
        "filters": {
            "scenario": scenario_filter,
            "tier": tier_filter,
            "matched_scenarios": len(rows),
            "matched_review_tasks": sum(len(row["review_tasks"]) for row in rows),
        },
        "dataset_input": {
            "openneuro_accession": accession,
            **dataset_status(dataset_root),
        },
        "official_tool_notes": [
            {
                "tool": "OpenNeuro CLI",
                "purpose": "Download public OpenNeuro datasets after selecting an accession.",
                "template": "openneuro download <accession number> <destination directory>",
                "source": "https://docs.openneuro.org/packages/openneuro-cli.html",
            },
            {
                "tool": "BIDS Validator",
                "purpose": "Check BIDS compliance before ROI extraction.",
                "template": "bids-validator-deno <dataset root> --json",
                "source": "https://github.com/bids-standard/bids-validator",
            },
        ],
        "evidence_backbone": payload.get("research_backbone", []),
        "validation_bridge": bridge,
        "scenario_review_summary": rows,
        "validation_readiness_requirements": validation_readiness_requirements(),
        "validation_protocol_template": validation_protocol_template(
            accession, dataset_root, scenario_filter, tier_filter
        ),
        "minimum_artifacts": [
            "BIDS validation report",
            "ROI extraction QC report",
            "Motion/site/scanner QC summary",
            "Behavior or endpoint alignment note",
            "Updated BOLD R2 and FC corr",
            "Updated Validation Ledger",
            "Updated acquisition portfolio and negative evidence",
        ],
    }


def write_manifest(manifest: dict, output_dir: Path, output_prefix: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{output_prefix}_manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_protocol_template(manifest: dict, output_dir: Path, output_prefix: str) -> tuple[Path, Path]:
    protocol = manifest["validation_protocol_template"]
    json_path = output_dir / f"{output_prefix}_protocol_template.json"
    json_path.write_text(json.dumps(protocol, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Public Validation Protocol Template",
        "",
        "This is a dry template for turning a selected public fMRI dataset into a NeuroTwin validation run. It records the expected data contract, QC fields and split policy before any model score is interpreted.",
        "",
        "## OpenNeuro Dry Example",
        "",
        f"- Accession: `{protocol['openneuro_dry_example']['accession']}`",
        f"- Dataset root: `{protocol['openneuro_dry_example']['dataset_root']}`",
        "",
        "```bash",
        protocol["openneuro_dry_example"]["download_command"],
        "```",
        "",
        protocol["openneuro_dry_example"]["note"],
        "",
        "## BIDS Contract",
        "",
        f"- Validator: `{protocol['bids_contract']['validator_command']}`",
        f"- Source: {protocol['bids_contract']['source']}",
        "",
        "Required files:",
        "",
    ]
    lines += [f"- {item}" for item in protocol["bids_contract"]["required_files"]]
    lines += [
        "",
        "## Preprocessing Contract",
        "",
        f"- Recommended derivative: {protocol['preprocessing_contract']['recommended_derivative']}",
        f"- Source: {protocol['preprocessing_contract']['source']}",
        "",
        "Confounds to record:",
        "",
    ]
    lines += [f"- {item}" for item in protocol["preprocessing_contract"]["confounds_to_record"]]
    lines += [
        "",
        "## Atlas Contract",
        "",
        "| Field | Value |",
        "| --- | --- |",
    ]
    for key, value in protocol["atlas_contract"].items():
        lines.append(f"| {key} | {value} |")
    lines += [
        "",
        "## Split Policy",
        "",
        "| Field | Value |",
        "| --- | --- |",
    ]
    for key, value in protocol["split_policy"].items():
        lines.append(f"| {key} | {value} |")
    lines += [
        "",
        "## QC Thresholds",
        "",
        "| Field | Value |",
        "| --- | ---: |",
    ]
    for key, value in protocol["qc_thresholds"].items():
        lines.append(f"| {key} | {value} |")
    lines += [
        "",
        "## Required Outputs",
        "",
    ]
    lines += [f"- {item}" for item in protocol["required_outputs"]]
    lines.append("")
    md_path = output_dir / f"{output_prefix}_protocol_template.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def write_runbook(manifest: dict, output_dir: Path, output_prefix: str) -> Path:
    lines = [
        "# Public Validation Runbook",
        "",
        "This runbook turns the review gate into a concrete public-data validation path. It is a dry scaffold; no dataset download was performed by this script.",
        "",
        "## Current Dataset Input",
        "",
        f"- OpenNeuro accession: `{manifest['dataset_input']['openneuro_accession']}`",
        f"- Dataset root: `{manifest['dataset_input']['dataset_root']}`",
        f"- Dataset state: `{manifest['dataset_input']['state']}`",
        f"- `dataset_description.json`: `{manifest['dataset_input']['dataset_description']}`",
        "",
        "## Filter Scope",
        "",
        f"- Scenario filter: `{manifest['filters']['scenario']}`",
        f"- Tier filter: `{manifest['filters']['tier']}`",
        f"- Matched scenarios: `{manifest['filters']['matched_scenarios']}`",
        f"- Matched review tasks: `{manifest['filters']['matched_review_tasks']}`",
        "",
        "## Official Tool Templates",
        "",
    ]
    for note in manifest["official_tool_notes"]:
        lines += [
            f"### {note['tool']}",
            "",
            note["purpose"],
            "",
            "```bash",
            note["template"],
            "```",
            "",
            f"Source: {note['source']}",
            "",
        ]
    lines += [
        "## Review-Gate Queue",
        "",
        "| Priority | Action | Dataset | Task | Success gate |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for tier in manifest["validation_bridge"]["tiers"]:
        priority = next(
            (
                task["priority"]
                for row in manifest["scenario_review_summary"]
                for task in row["review_tasks"]
                if task["action"] == tier["name"]
            ),
            "-",
        )
        lines.append(f"| {priority} | {tier['name']} | {tier['dataset']} | {tier['task']} | {tier['success_gate']} |")
    lines += [
        "",
        "## Scenario Routing",
        "",
        "| Scenario | Readiness | Routing | First review task |",
        "| --- | ---: | --- | --- |",
    ]
    for row in manifest["scenario_review_summary"]:
        first_task = row["review_tasks"][0]["action"] if row["review_tasks"] else "none"
        lines.append(f"| {row['scenario']} | {row['readiness_score']} | {row['routing']} | {first_task} |")
    lines += [
        "",
        "## Validation Readiness Requirements",
        "",
        "| Area | Check | Reason |",
        "| --- | --- | --- |",
    ]
    for item in manifest["validation_readiness_requirements"]:
        lines.append(f"| {item['area']} | {item['check']} | {item['reason']} |")
    lines += [
        "",
        "## Evidence Backbone Used",
        "",
        "| Theme | Project move |",
        "| --- | --- |",
    ]
    for item in manifest["evidence_backbone"]:
        lines.append(f"| {item['theme']} | {item['project_move']} |")
    lines += [
        "",
        "## Minimum Executable Path",
        "",
        "1. Select the target public dataset and prepare access outside this demo package.",
        "2. Validate the BIDS root and save the validator JSON report.",
        "3. Extract ROI time series using the same atlas contract used by NeuroTwin.",
        "4. Re-run surrogate fitting and update BOLD R2, FC corr and perturbation budget.",
        f"5. Complete `{output_prefix}_protocol_template.md` before interpreting model scores.",
        f"6. Update `validation_ledger`, `{output_prefix}_manifest.json` and the acquisition portfolio.",
        "",
        "## Expected Artifacts",
        "",
    ]
    lines += [f"- {artifact}" for artifact in manifest["minimum_artifacts"]]
    lines.append("")
    path = output_dir / f"{output_prefix}_runbook.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    args = parse_args()
    payload = load_payload(Path(args.payload))
    output_dir = Path(args.output_dir)
    try:
        manifest = build_manifest(payload, args.accession, args.dataset_root, args.scenario, args.tier)
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from None
    manifest_path = write_manifest(manifest, output_dir, args.output_prefix)
    protocol_json_path, protocol_md_path = write_protocol_template(manifest, output_dir, args.output_prefix)
    runbook_path = write_runbook(manifest, output_dir, args.output_prefix)
    print(f"Wrote {manifest_path}")
    print(f"Wrote {protocol_json_path}")
    print(f"Wrote {protocol_md_path}")
    print(f"Wrote {runbook_path}")


if __name__ == "__main__":
    main()
