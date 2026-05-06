# NeuroTwin Demo Report

## Demo Purpose

NeuroTwin demonstrates an agent-ready surrogate brain capability for neuro-AI4S. The demo uses synthetic ROI-level fMRI-like signals to show the executable workflow: build a brain dynamics surrogate, run virtual perturbations, score the response, and produce a trace-backed next-experiment suggestion. The core scientific loop is DSVL: Design, Simulate, Validate and Learn.

## What This Proves

- The proposal has been turned from concept into a callable workflow.
- The workflow follows a surrogate-driven Design-Simulate-Validate-Learn loop.
- The surrogate brain can be evaluated by signal fidelity, FC consistency, perturbation response, and human-readable experiment traces.

## Demo Metrics

| Scenario | BOLD R2 | FC Corr | Objective Delta | Objective |
| --- | ---: | ---: | ---: | --- |
| Emotional faces | 0.8387 | 0.898 | 0.3587 | Lower limbic over-response while preserving visual processing. |
| Cognitive control | 0.8593 | 0.9416 | 0.1031 | Increase control-network stability and reduce default-mode intrusion. |
| Closed-loop neuro experiment | 0.7382 | 0.9396 | 0.1762 | Select the smallest perturbation that shifts the network toward a healthier attractor. |

## Learn Stage Ranking

| Scenario | Uncertainty | FC Gap | Next simulation | Priority |
| --- | ---: | ---: | --- | ---: |
| Emotional faces | 0.1613 | 0.102 | Behavior endpoint alignment | 0.2037 |
| Cognitive control | 0.1407 | 0.0584 | Behavior endpoint alignment | 0.1112 |
| Closed-loop neuro experiment | 0.2618 | 0.0604 | Constrained policy search | 0.1671 |

## Multi-Objective Acquisition Portfolio

| Scenario | Top action | Fidelity | Objective | Novelty | Feasibility | Risk control | Portfolio |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Emotional faces | Behavior endpoint alignment | 0.8677 | 0.8968 | 0.61 | 0.4 | 0.7024 | 0.733 |
| Cognitive control | Behavior endpoint alignment | 0.6242 | 0.2577 | 0.61 | 0.4 | 0.7014 | 0.5144 |
| Closed-loop neuro experiment | Constrained policy search | 0.8082 | 0.4405 | 0.82 | 0.3333 | 0.5504 | 0.6225 |

Default portfolio weights: fidelity 0.32, objective 0.22, novelty 0.18, feasibility 0.16, risk control 0.12. The interactive dashboard can adjust these weights to simulate different experiment-operation policies.

## Validation Ledger

| Scenario | Pass | Watch | Review | Hold | Readiness | Routing |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Emotional faces | 4 | 0 | 1 | 0 | 0.88 | Advance as dry-run with explicit review gates |
| Cognitive control | 4 | 0 | 1 | 0 | 0.88 | Advance as dry-run with explicit review gates |
| Closed-loop neuro experiment | 4 | 0 | 1 | 0 | 0.88 | Advance as dry-run with explicit review gates |

The ledger turns validation into a visible gate before the Learn stage updates the next run. Review gates create explicit validation tasks for public data, held-out subjects or expert endpoint review.

## Public Validation Bridge

Review gates should create concrete public-data validation tasks before downstream claims are made.

| Tier | Dataset | Access | Task |
| --- | --- | --- | --- |
| OpenNeuro BIDS smoke test | OpenNeuro | public BIDS datasets with validation tooling | Run the same ROI extraction, surrogate fit and Validation Ledger on one small task-fMRI dataset. |
| HCP task-fMRI transfer check | Human Connectome Project | registered access for high-quality task and resting fMRI resources | Check whether the surrogate and acquisition policy remain stable on HCP task contrasts. |
| ABCD cohort stress test | ABCD Study | controlled access; availability must be checked before use | Use large-cohort developmental MRI only when approved access and governance are clear. |

## Evidence Backbone

| Theme | Source | Project move |
| --- | --- | --- |
| Agentic AI4S infrastructure | [Bohrium + SciMaster](https://arxiv.org/abs/2512.20469) | Frame NeuroTwin as an agent-ready virtual experiment capability with contracts, trace memory and validation gates. |
| Personalised brain simulation | [The Virtual Brain on EBRAINS](https://ebrains.eu/data-tools-services/tools/the-virtual-brain) | Position the demo as a lightweight surrogate layer that can later interoperate with TVB-style connectome and neural mass modeling. |
| Self-driving lab metrics | [Nature Communications SDL metrics and accessibility papers](https://www.nature.com/articles/s41467-024-45569-5) | Add autonomy/readiness scoring and require each validation packet to record data, model, metrics and operator assumptions. |
| Hypothesis generation agents | [AI co-scientist](https://arxiv.org/abs/2502.18864) | Keep literature mining as Design-layer evidence cards, then route hypotheses through surrogate simulation and review gates. |
| Neuroimaging validation standards | [OpenNeuro, BIDS Validator, HCP and ABCD](https://docs.openneuro.org/packages/openneuro-cli.html) | Extend public validation runbooks with BIDS checks, ROI QC, subject split metrics, behavior endpoints and cohort-stress constraints. |
| DBTL loop engineering | [DBTL cycle reviews](https://link.springer.com/article/10.1007/s13721-024-00455-4) | Map NeuroTwin's DSVL stages to evidence cards, virtual runs, validation packets and learning-memory updates. |
| Generative digital twins | [Neuroimaging digital twin reviews](https://academic.oup.com/cercor/article/35/1/bhae462/7930283) | Treat effective-connectivity perturbation and next-run acquisition as counterfactual dry experiments under explicit validation gates. |

## Agent Loop and Next Validation Packet

An AI4S agent should route one scientific question through Read, Prepare, Build, Compute, Validate and Learn, while preserving trace and decision memory.

| Scenario | Learn action | Validation candidate | Readiness | Decision rule |
| --- | --- | --- | ---: | --- |
| Emotional faces | Behavior endpoint alignment | OpenNeuro BIDS smoke test | 0.88 | Advance only after protocol fields, QC evidence and external-data review are recorded in the ledger. |
| Cognitive control | Behavior endpoint alignment | OpenNeuro BIDS smoke test | 0.88 | Advance only after protocol fields, QC evidence and external-data review are recorded in the ledger. |
| Closed-loop neuro experiment | Constrained policy search | OpenNeuro BIDS smoke test | 0.88 | Advance only after protocol fields, QC evidence and external-data review are recorded in the ledger. |

## Interpretation

Positive objective delta means the virtual intervention moved the network in the desired direction for this synthetic task. In a real project, this metric would be replaced or calibrated by domain endpoints such as task accuracy, symptom-scale shift, cell assay response, or stimulation readout.

## Next Step

Replace synthetic signals with a public fMRI dataset, package preprocessing as a reusable capability, and expose the surrogate model as an API with explicit input/output schemas and replayable execution traces. The next research step is to add uncertainty-aware experiment selection so the Learn stage actively chooses the most informative next simulation.
