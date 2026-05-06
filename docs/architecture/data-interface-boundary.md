# Data Interface Boundary

Knowledge mining and data engineering are Design-layer inputs. They source hypotheses, improve data readiness and propose representations before the surrogate brain runs virtual experiments.

## Interface Map

| Interface | Role | Output | Boundary |
| --- | --- | --- | --- |
| Literature and method mining | Surface candidate mechanisms, task paradigms, ROI choices and validation metrics. | Evidence cards, method candidates and hypothesis seeds | Feeds Design; final next-run choice is made by validation metrics and acquisition policy. |
| Data extraction and cleaning | Convert imaging, behavior or metadata assets into reusable model inputs. | QC reports, ROI time series and dataset cards | Feeds Simulate only after quality gates are recorded. |
| Feature engineering | Build candidate descriptors such as FC priors, task labels, phenotype scores and subject context. | Feature schema and representation candidates | Provides optional context; surrogate validation decides whether features help. |
| Virtual experiment core | Train surrogate dynamics, run perturbations, validate outputs and update the next policy. | BOLD predictions, FC/EC response, reports, trace and next-run plan | Main DSVL engine and primary project contribution. |

## Positioning

The data interface layer makes the project compatible with large-scale literature parsing, data extraction, data cleaning and feature engineering pipelines. Its job is to improve hypothesis quality and data readiness before a virtual experiment starts.

The main NeuroTwin contribution remains the executable scientific loop: surrogate simulation, validation gates, programmable acquisition policy and learning memory.
