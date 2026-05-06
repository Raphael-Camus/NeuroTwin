# Public Validation Runbook

This runbook turns the review gate into a concrete public-data validation path. It is a dry scaffold; no dataset download was performed by this script.

## Current Dataset Input

- OpenNeuro accession: `<openneuro_accession>`
- Dataset root: `<local_bids_root>`
- Dataset state: `placeholder`
- `dataset_description.json`: `not checked`

## Filter Scope

- Scenario filter: `emotion`
- Tier filter: `1`
- Matched scenarios: `1`
- Matched review tasks: `1`

## Official Tool Templates

### OpenNeuro CLI

Download public OpenNeuro datasets after selecting an accession.

```bash
openneuro download <accession number> <destination directory>
```

Source: https://docs.openneuro.org/packages/openneuro-cli.html

### BIDS Validator

Check BIDS compliance before ROI extraction.

```bash
bids-validator-deno <dataset root> --json
```

Source: https://github.com/bids-standard/bids-validator

## Review-Gate Queue

| Priority | Action | Dataset | Task | Success gate |
| ---: | --- | --- | --- | --- |
| 1 | OpenNeuro BIDS smoke test | OpenNeuro | Run the same ROI extraction, surrogate fit and Validation Ledger on one small task-fMRI dataset. | Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated. |

## Scenario Routing

| Scenario | Readiness | Routing | First review task |
| --- | ---: | --- | --- |
| Emotional faces | 0.88 | Advance as dry-run with explicit review gates | OpenNeuro BIDS smoke test |

## Validation Readiness Requirements

| Area | Check | Reason |
| --- | --- | --- |
| BIDS compliance | Run validator JSON output and record dataset_description, participants.tsv and task event files. | Public fMRI validation must start from a reusable data contract. |
| ROI extraction QC | Record atlas version, missing ROI rate, temporal length, nuisance regression choices and failed subjects. | Surrogate metrics are only interpretable when representation quality is visible. |
| Motion and site effects | Record framewise displacement summary, censoring rule, scanner/site labels and split strategy. | Large neuroimaging cohorts can reward confounds if QC is mixed with model score. |
| Behavior endpoint | Attach task accuracy, reaction time, clinical scale or human-review endpoint when available. | Network-level shifts need an external objective for scientific interpretation. |
| Repeatability | Save seeds, model version, feature schema, validation split and negative evidence. | Self-driving lab style loops require replayable decisions and failed-run memory. |

## Evidence Backbone Used

| Theme | Project move |
| --- | --- |
| Agentic AI4S infrastructure | Frame NeuroTwin as an agent-ready virtual experiment capability with contracts, trace memory and validation gates. |
| Personalised brain simulation | Position the demo as a lightweight surrogate layer that can later interoperate with TVB-style connectome and neural mass modeling. |
| Self-driving lab metrics | Add autonomy/readiness scoring and require each validation packet to record data, model, metrics and operator assumptions. |
| Hypothesis generation agents | Keep literature mining as Design-layer evidence cards, then route hypotheses through surrogate simulation and review gates. |
| Neuroimaging validation standards | Extend public validation runbooks with BIDS checks, ROI QC, subject split metrics, behavior endpoints and cohort-stress constraints. |
| DBTL loop engineering | Map NeuroTwin's DSVL stages to evidence cards, virtual runs, validation packets and learning-memory updates. |
| Generative digital twins | Treat effective-connectivity perturbation and next-run acquisition as counterfactual dry experiments under explicit validation gates. |

## Minimum Executable Path

1. Select the target public dataset and prepare access outside this demo package.
2. Validate the BIDS root and save the validator JSON report.
3. Extract ROI time series using the same atlas contract used by NeuroTwin.
4. Re-run surrogate fitting and update BOLD R2, FC corr and perturbation budget.
5. Complete `public_validation_openneuro_smoke_protocol_template.md` before interpreting model scores.
6. Update `validation_ledger`, `public_validation_openneuro_smoke_manifest.json` and the acquisition portfolio.

## Expected Artifacts

- BIDS validation report
- ROI extraction QC report
- Motion/site/scanner QC summary
- Behavior or endpoint alignment note
- Updated BOLD R2 and FC corr
- Updated Validation Ledger
- Updated acquisition portfolio and negative evidence
