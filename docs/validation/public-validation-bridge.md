# Public Validation Bridge

Review gates should create concrete public-data validation tasks before downstream claims are made.

## Validation Tiers

| Tier | Dataset | Access | Task | Success gate | Source |
| --- | --- | --- | --- | --- | --- |
| OpenNeuro BIDS smoke test | OpenNeuro | public BIDS datasets with validation tooling | Run the same ROI extraction, surrogate fit and Validation Ledger on one small task-fMRI dataset. | Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated. | https://docs.openneuro.org/ |
| HCP task-fMRI transfer check | Human Connectome Project | registered access for high-quality task and resting fMRI resources | Check whether the surrogate and acquisition policy remain stable on HCP task contrasts. | Subject-split metrics and behavior-alignment signals are reproducible across tasks. | https://icb.humanconnectome.org/hcp-protocols-ya-task-fmri |
| ABCD cohort stress test | ABCD Study | controlled access; availability must be checked before use | Use large-cohort developmental MRI only when approved access and governance are clear. | Generalization, site effects and QC gates are reported separately from model score. | https://abcdstudy.org/scientists/data-sharing/ |

## How Review Gates Use This Bridge

When `External evidence` is marked as `review`, the next DSVL cycle should schedule the OpenNeuro smoke test first. HCP transfer and ABCD cohort stress testing follow only after data access, governance and QC are clear.

## Minimum Executable Path

1. Select one OpenNeuro BIDS task-fMRI dataset.
2. Run ROI extraction and QC into the existing `demo_data.json` schema.
3. Recompute BOLD R2, FC corr, objective effect and perturbation budget.
4. Update the Validation Ledger and acquisition portfolio.
5. Keep failed or weak validation runs as negative evidence for routing.
