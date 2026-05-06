# Next Validation Packet

A next validation packet is the handoff object between one DSVL cycle and the next. It packages the scenario objective, evidence cards, Agent skill route, public validation candidate, protocol files, current metric state, next action and negative evidence.

## Scenario Packets

### Emotional faces

- Packet ID: `NVP-emotion`
- Objective: Lower limbic over-response while preserving visual processing.
- Why now: External-evidence review is visible, the dry run is traceable and the next action has a ranked acquisition score.
- Evidence cards: EC-001, EC-002, EC-003, EC-005, EC-006, EC-007
- Agent route: EvidenceCardBuilder -> BIDSValidationPlanner -> ROITimeSeriesExtractor -> SurrogateTrainer -> PerturbationSimulator -> ValidationLedgerWriter -> AcquisitionPolicyOptimizer -> NextValidationPacketBuilder
- Public validation candidate: P1 OpenNeuro BIDS smoke test using OpenNeuro. Success gate: Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated.
- Protocol files: public_validation_openneuro_smoke_protocol_template.md; public_validation_openneuro_smoke_protocol_template.json; public_validation_openneuro_smoke_runbook.md; public_validation_openneuro_smoke_manifest.json
- Current metrics: BOLD R2 0.8387, FC corr 0.898, objective 0.3587, readiness 0.88, routing Advance as dry-run with explicit review gates
- Learn action: Behavior endpoint alignment (priority 0.2037). Connect the network-level shift to a task or behavioral readout.
- Negative evidence: Subject split generalization (0.0856); Atlas robustness test (0.083)
- Required outputs: BIDS validator JSON; ROI QC table; subject split file; motion, site and scanner summary; behavior or task endpoint note; updated validation ledger; updated acquisition portfolio
- Decision rule: Advance only after protocol fields, QC evidence and external-data review are recorded in the ledger.

### Cognitive control

- Packet ID: `NVP-control`
- Objective: Increase control-network stability and reduce default-mode intrusion.
- Why now: External-evidence review is visible, the dry run is traceable and the next action has a ranked acquisition score.
- Evidence cards: EC-001, EC-002, EC-003, EC-005, EC-006, EC-007
- Agent route: EvidenceCardBuilder -> BIDSValidationPlanner -> ROITimeSeriesExtractor -> SurrogateTrainer -> PerturbationSimulator -> ValidationLedgerWriter -> AcquisitionPolicyOptimizer -> NextValidationPacketBuilder
- Public validation candidate: P1 OpenNeuro BIDS smoke test using OpenNeuro. Success gate: Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated.
- Protocol files: public_validation_openneuro_smoke_protocol_template.md; public_validation_openneuro_smoke_protocol_template.json; public_validation_openneuro_smoke_runbook.md; public_validation_openneuro_smoke_manifest.json
- Current metrics: BOLD R2 0.8593, FC corr 0.9416, objective 0.1031, readiness 0.88, routing Advance as dry-run with explicit review gates
- Learn action: Behavior endpoint alignment (priority 0.1112). Connect the network-level shift to a task or behavioral readout.
- Negative evidence: Atlas robustness test (0.0636); Perturbation scale sweep (0.0183)
- Required outputs: BIDS validator JSON; ROI QC table; subject split file; motion, site and scanner summary; behavior or task endpoint note; updated validation ledger; updated acquisition portfolio
- Decision rule: Advance only after protocol fields, QC evidence and external-data review are recorded in the ledger.

### Closed-loop neuro experiment

- Packet ID: `NVP-closed_loop`
- Objective: Select the smallest perturbation that shifts the network toward a healthier attractor.
- Why now: External-evidence review is visible, the dry run is traceable and the next action has a ranked acquisition score.
- Evidence cards: EC-001, EC-002, EC-003, EC-005, EC-006, EC-007
- Agent route: EvidenceCardBuilder -> BIDSValidationPlanner -> ROITimeSeriesExtractor -> SurrogateTrainer -> PerturbationSimulator -> ValidationLedgerWriter -> AcquisitionPolicyOptimizer -> NextValidationPacketBuilder
- Public validation candidate: P1 OpenNeuro BIDS smoke test using OpenNeuro. Success gate: Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated.
- Protocol files: public_validation_openneuro_smoke_protocol_template.md; public_validation_openneuro_smoke_protocol_template.json; public_validation_openneuro_smoke_runbook.md; public_validation_openneuro_smoke_manifest.json
- Current metrics: BOLD R2 0.7382, FC corr 0.9396, objective 0.1762, readiness 0.88, routing Advance as dry-run with explicit review gates
- Learn action: Constrained policy search (priority 0.1671). Optimize objective improvement under a small-perturbation budget.
- Negative evidence: Perturbation scale sweep (0.1055); Atlas robustness test (0.0885)
- Required outputs: BIDS validator JSON; ROI QC table; subject split file; motion, site and scanner summary; behavior or task endpoint note; updated validation ledger; updated acquisition portfolio
- Decision rule: Advance only after protocol fields, QC evidence and external-data review are recorded in the ledger.

## Reviewer Reading

This file is the clearest place to show AI-accelerated iteration: the previous run produces a small structured packet that can be routed to the next dry validation step, then merged back into the ledger and acquisition policy.
