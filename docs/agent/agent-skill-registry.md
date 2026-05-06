# Agent Skill Registry

An AI4S agent should route one scientific question through Read, Prepare, Build, Compute, Validate and Learn, while preserving trace and decision memory.

## Loop Route

| Step | Agent action | Memory written back |
| --- | --- | --- |
| Read | Mine papers, standards and internal method cards into structured evidence. | Evidence cards and risk notes. |
| Prepare | Select a public validation tier and fill the protocol fields needed before scoring. | Dataset contract, BIDS/QC state and operator assumptions. |
| Build | Create ROI time series and feature context under a fixed split policy. | Data card, ROI QC and split file. |
| Compute | Train surrogate dynamics and run virtual perturbation experiments. | Model metrics, FC/EC response and objective delta. |
| Validate | Write pass, watch, review and hold decisions into a validation ledger. | Review queue and escalation rule. |
| Learn | Rank next actions, preserve negative evidence and emit a next validation packet. | Acquisition portfolio and next-cycle packet. |

## Callable Skills

| Skill | Stage | Purpose | Gate | Artifact |
| --- | --- | --- | --- | --- |
| `EvidenceCardBuilder` | Read | Convert literature, method notes and platform standards into structured Design inputs. | Every claim must map to a scenario input, surrogate requirement, validation gate, risk or next action. | artifacts/demo/evidence_cards.json |
| `BIDSValidationPlanner` | Prepare | Turn review gates into public fMRI validation protocol fields before model scores are interpreted. | BIDS, preprocessing, ROI, split and QC assumptions must be recorded. | artifacts/demo/public_validation_protocol_template.md |
| `ROITimeSeriesExtractor` | Build | Convert validated imaging data into atlas-aligned ROI time series and QC tables. | Minimum timepoints, missing ROI threshold and motion review must pass or be marked for repair. | future public-validation workspace |
| `SurrogateTrainer` | Compute | Fit the surrogate brain dynamics model under fixed split and seed policy. | Signal fidelity and FC reproducibility gates are updated. | artifacts/demo/demo_data.json |
| `PerturbationSimulator` | Compute | Run counterfactual virtual perturbations and estimate effective-connectivity response. | Perturbation budget and objective-effect gates are updated. | artifacts/demo/brain_twin_lab.html |
| `ValidationLedgerWriter` | Validate | Record pass, watch, review and hold decisions for scientific readiness. | Review items must become concrete validation tasks. | artifacts/demo/validation_ledger.md |
| `AcquisitionPolicyOptimizer` | Learn | Rank next simulations using uncertainty, FC gap, objective signal, feasibility and risk control. | Weak actions remain in negative evidence for future routing. | artifacts/demo/acquisition_policy.md |
| `NextValidationPacketBuilder` | Learn | Package the next executable validation step as a decision-ready object for the next loop. | Packet must include objective, evidence, route, protocol files, required outputs and decision rule. | artifacts/demo/next_validation_packet.json |

## Why This Matters

This registry turns the demo into a platform-style scientific capability. A master agent can inspect which tool to call, what evidence it consumes, what artifact it emits and which gate must be satisfied before the next stage.
