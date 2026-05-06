# Capability Card

Name: `NeuroTwin.SurrogateBrainPerturbation`
Version: `0.2-demo`

## Input Contract

- ROI time series: T x N
- Brain atlas and network labels
- Scenario objective and candidate perturbation
- Optional behavior or clinical endpoint

## Output Contract

- Predicted BOLD dynamics
- Functional and virtual effective connectivity
- Candidate intervention score
- Validation metrics and replayable trace
- Validation ledger and escalation rule

## Validation Gates

- Signal fidelity
- FC consistency
- Perturbation stability
- External-evidence review
- Human expert review before real-world action

## Platform Fit

- Design: evidence-grounded hypothesis and objective design
- Simulate: callable surrogate brain virtual experiment
- Validate: trace-backed metrics and plausibility gates
- Learn: metrics drive model, hypothesis and experiment iteration

## Agent Skill Route

- `EvidenceCardBuilder` (Read): Convert literature, method notes and platform standards into structured Design inputs.
- `BIDSValidationPlanner` (Prepare): Turn review gates into public fMRI validation protocol fields before model scores are interpreted.
- `ROITimeSeriesExtractor` (Build): Convert validated imaging data into atlas-aligned ROI time series and QC tables.
- `SurrogateTrainer` (Compute): Fit the surrogate brain dynamics model under fixed split and seed policy.
- `PerturbationSimulator` (Compute): Run counterfactual virtual perturbations and estimate effective-connectivity response.
- `ValidationLedgerWriter` (Validate): Record pass, watch, review and hold decisions for scientific readiness.
- `AcquisitionPolicyOptimizer` (Learn): Rank next simulations using uncertainty, FC gap, objective signal, feasibility and risk control.
- `NextValidationPacketBuilder` (Learn): Package the next executable validation step as a decision-ready object for the next loop.

## Next Validation Packet

- `artifacts/demo/next_validation_packet.json`: machine-readable handoff for the next DSVL cycle.
- `artifacts/demo/next_validation_packet.md`: human-readable scenario packets and decision rules.

## Evidence Backbone

- Agentic AI4S infrastructure: Frame NeuroTwin as an agent-ready virtual experiment capability with contracts, trace memory and validation gates. (https://arxiv.org/abs/2512.20469)
- Personalised brain simulation: Position the demo as a lightweight surrogate layer that can later interoperate with TVB-style connectome and neural mass modeling. (https://ebrains.eu/data-tools-services/tools/the-virtual-brain)
- Self-driving lab metrics: Add autonomy/readiness scoring and require each validation packet to record data, model, metrics and operator assumptions. (https://www.nature.com/articles/s41467-024-45569-5)
- Hypothesis generation agents: Keep literature mining as Design-layer evidence cards, then route hypotheses through surrogate simulation and review gates. (https://arxiv.org/abs/2502.18864)
- Neuroimaging validation standards: Extend public validation runbooks with BIDS checks, ROI QC, subject split metrics, behavior endpoints and cohort-stress constraints. (https://docs.openneuro.org/packages/openneuro-cli.html)
- DBTL loop engineering: Map NeuroTwin's DSVL stages to evidence cards, virtual runs, validation packets and learning-memory updates. (https://link.springer.com/article/10.1007/s13721-024-00455-4)
- Generative digital twins: Treat effective-connectivity perturbation and next-run acquisition as counterfactual dry experiments under explicit validation gates. (https://academic.oup.com/cercor/article/35/1/bhae462/7930283)

## Boundary

This is a research workflow capability for hypothesis generation and virtual dry-runs. It does not perform clinical diagnosis or autonomous medical decision-making.
