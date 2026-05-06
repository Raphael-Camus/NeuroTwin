# Public Validation Protocol Template

This is a dry template for turning a selected public fMRI dataset into a NeuroTwin validation run. It records the expected data contract, QC fields and split policy before any model score is interpreted.

## OpenNeuro Dry Example

- Accession: `<openneuro_accession>`
- Dataset root: `<local_bids_root>`

```bash
openneuro download <openneuro_accession> <local_bids_root>
```

Replace placeholders with a selected public dataset. The script records the command template only.

## BIDS Contract

- Validator: `bids-validator-deno <dataset root> --json`
- Source: https://bids-specification.readthedocs.io/

Required files:

- dataset_description.json
- participants.tsv
- task events.tsv for each selected BOLD run

## Preprocessing Contract

- Recommended derivative: fMRIPrep outputs when available
- Source: https://fmriprep.org/en/stable/outputs.html

Confounds to record:

- framewise_displacement
- dvars
- motion_outliers or censoring columns when available
- scanner/site/session labels when available

## Atlas Contract

| Field | Value |
| --- | --- |
| space | MNI152NLin2009cAsym or dataset-native space with explicit transform record |
| atlas_name | <atlas_name> |
| roi_labels | <roi_labels.tsv> |
| extraction_tool | Nilearn NiftiLabelsMasker or equivalent audited extractor |
| aggregation | mean signal per ROI after mask and confound handling |
| minimum_timepoints | 120 |
| max_missing_roi_fraction | 0.05 |
| source | https://nilearn.github.io/stable/modules/generated/nilearn.maskers.NiftiLabelsMasker.html |

## Split Policy

| Field | Value |
| --- | --- |
| primary_split | subject-level train/validation/test split |
| fallback_split | session-level split only when subject count is insufficient and leakage is documented |
| stratify_by | ['task', 'site/scanner when available', 'age/sex or cohort label when available'] |
| fixed_seed | 20260501 |
| leakage_rule | No subject can appear in both train and test. |

## QC Thresholds

| Field | Value |
| --- | ---: |
| mean_fd_watch_mm | 0.2 |
| mean_fd_review_mm | 0.3 |
| max_high_motion_fraction | 0.25 |
| min_bold_r2_for_pass | 0.7 |
| min_fc_corr_for_pass | 0.75 |
| threshold_note | Motion thresholds are proposed review defaults for this demo and should be adapted per dataset. |

## Required Outputs

- BIDS validator JSON
- ROI extraction QC table
- subject split file
- motion/site/scanner summary
- behavior endpoint alignment note
- updated Validation Ledger
- updated acquisition portfolio
