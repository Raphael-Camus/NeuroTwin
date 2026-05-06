# Validation Ledger

This note makes the Validate stage explicit. Each virtual experiment is routed through pass, watch, review or hold gates before its result can update the next acquisition policy.

## Scenario Summaries

| Scenario | Pass | Watch | Review | Hold | Readiness | Routing |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Emotional faces | 4 | 0 | 1 | 0 | 0.88 | Advance as dry-run with explicit review gates |
| Cognitive control | 4 | 0 | 1 | 0 | 0.88 | Advance as dry-run with explicit review gates |
| Closed-loop neuro experiment | 4 | 0 | 1 | 0 | 0.88 | Advance as dry-run with explicit review gates |

## Gate Details

### Emotional faces

Every virtual experiment must expose pass, watch, review or hold gates before the Learn stage selects the next run.

| Gate | Status | Evidence | Threshold | Next control |
| --- | --- | --- | --- | --- |
| Signal fidelity | pass | BOLD R2 = 0.8387 | pass >= 0.70; watch >= 0.55 | Advance to FC and perturbation audit when pass is reached. |
| FC reproducibility | pass | FC corr = 0.898 | pass >= 0.75; watch >= 0.60 | Run atlas robustness or subject-split validation when uncertainty remains. |
| Objective effect | pass | objective delta = 0.3587 | pass if absolute effect >= 0.08 | Attach task behavior, symptom score, cell assay or stimulation readout. |
| Perturbation budget | pass | intervention cost = 0.4804 | pass <= 0.55; watch <= 0.75 | Search smaller intervention scales before downstream validation. |
| External evidence | review | Current artifact uses synthetic ROI signals. | requires public fMRI, held-out subject split, or expert endpoint review | Route to public-data validation before translational claims. |

Escalation rule: Only pass-gated signals can inform the next acquisition policy directly; watch and review gates create validation tasks in the next DSVL cycle.

Review queue:

- P1 OpenNeuro BIDS smoke test: Run the same ROI extraction, surrogate fit and Validation Ledger on one small task-fMRI dataset. Success gate: Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated. (https://docs.openneuro.org/)
- P2 HCP task-fMRI transfer check: Check whether the surrogate and acquisition policy remain stable on HCP task contrasts. Success gate: Subject-split metrics and behavior-alignment signals are reproducible across tasks. (https://icb.humanconnectome.org/hcp-protocols-ya-task-fmri)
- P3 ABCD cohort stress test: Use large-cohort developmental MRI only when approved access and governance are clear. Success gate: Generalization, site effects and QC gates are reported separately from model score. (https://abcdstudy.org/scientists/data-sharing/)

### Cognitive control

Every virtual experiment must expose pass, watch, review or hold gates before the Learn stage selects the next run.

| Gate | Status | Evidence | Threshold | Next control |
| --- | --- | --- | --- | --- |
| Signal fidelity | pass | BOLD R2 = 0.8593 | pass >= 0.70; watch >= 0.55 | Advance to FC and perturbation audit when pass is reached. |
| FC reproducibility | pass | FC corr = 0.9416 | pass >= 0.75; watch >= 0.60 | Run atlas robustness or subject-split validation when uncertainty remains. |
| Objective effect | pass | objective delta = 0.1031 | pass if absolute effect >= 0.08 | Attach task behavior, symptom score, cell assay or stimulation readout. |
| Perturbation budget | pass | intervention cost = 0.4883 | pass <= 0.55; watch <= 0.75 | Search smaller intervention scales before downstream validation. |
| External evidence | review | Current artifact uses synthetic ROI signals. | requires public fMRI, held-out subject split, or expert endpoint review | Route to public-data validation before translational claims. |

Escalation rule: Only pass-gated signals can inform the next acquisition policy directly; watch and review gates create validation tasks in the next DSVL cycle.

Review queue:

- P1 OpenNeuro BIDS smoke test: Run the same ROI extraction, surrogate fit and Validation Ledger on one small task-fMRI dataset. Success gate: Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated. (https://docs.openneuro.org/)
- P2 HCP task-fMRI transfer check: Check whether the surrogate and acquisition policy remain stable on HCP task contrasts. Success gate: Subject-split metrics and behavior-alignment signals are reproducible across tasks. (https://icb.humanconnectome.org/hcp-protocols-ya-task-fmri)
- P3 ABCD cohort stress test: Use large-cohort developmental MRI only when approved access and governance are clear. Success gate: Generalization, site effects and QC gates are reported separately from model score. (https://abcdstudy.org/scientists/data-sharing/)

### Closed-loop neuro experiment

Every virtual experiment must expose pass, watch, review or hold gates before the Learn stage selects the next run.

| Gate | Status | Evidence | Threshold | Next control |
| --- | --- | --- | --- | --- |
| Signal fidelity | pass | BOLD R2 = 0.7382 | pass >= 0.70; watch >= 0.55 | Advance to FC and perturbation audit when pass is reached. |
| FC reproducibility | pass | FC corr = 0.9396 | pass >= 0.75; watch >= 0.60 | Run atlas robustness or subject-split validation when uncertainty remains. |
| Objective effect | pass | objective delta = 0.1762 | pass if absolute effect >= 0.08 | Attach task behavior, symptom score, cell assay or stimulation readout. |
| Perturbation budget | pass | intervention cost = 0.4133 | pass <= 0.55; watch <= 0.75 | Search smaller intervention scales before downstream validation. |
| External evidence | review | Current artifact uses synthetic ROI signals. | requires public fMRI, held-out subject split, or expert endpoint review | Route to public-data validation before translational claims. |

Escalation rule: Only pass-gated signals can inform the next acquisition policy directly; watch and review gates create validation tasks in the next DSVL cycle.

Review queue:

- P1 OpenNeuro BIDS smoke test: Run the same ROI extraction, surrogate fit and Validation Ledger on one small task-fMRI dataset. Success gate: Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated. (https://docs.openneuro.org/)
- P2 HCP task-fMRI transfer check: Check whether the surrogate and acquisition policy remain stable on HCP task contrasts. Success gate: Subject-split metrics and behavior-alignment signals are reproducible across tasks. (https://icb.humanconnectome.org/hcp-protocols-ya-task-fmri)
- P3 ABCD cohort stress test: Use large-cohort developmental MRI only when approved access and governance are clear. Success gate: Generalization, site effects and QC gates are reported separately from model score. (https://abcdstudy.org/scientists/data-sharing/)

## Design Cues

- Virtual brain simulation and digital twin work motivate explicit subject/data readiness and intervention validation: https://academic.oup.com/nsr/article/11/5/nwae079/7616087
- Neural perturbational inference motivates using a trained surrogate as a virtual perturbation object: https://www.nature.com/articles/s41592-025-02654-x
- Self-driving laboratory work motivates visible metrics for closed-loop experiment selection: https://www.nature.com/articles/s41467-024-45569-5
