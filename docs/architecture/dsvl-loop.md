# DSVL Scientific Loop

Loop name: **Design-Simulate-Validate-Learn**

A surrogate-driven AI4S loop where hypotheses are designed, tested in virtual brain experiments, validated against neural or behavioral evidence, and learned back into the next round.

## Why DSVL

AI4S projects become more scientific when the surrogate model participates in experiment design, simulation, validation and learning. For NeuroTwin, the main claim is the creation of a virtual experimental world for brain-system research.

Knowledge extraction, literature parsing and feature engineering support the Design stage. The core scientific value comes from the surrogate-driven loop itself.

## Stages

### Design

- Guiding question: What brain-system hypothesis or intervention objective should be tested next?
- Artifact: Hypothesis, task context, candidate perturbation and objective function

### Simulate

- Guiding question: How does the surrogate brain respond under the proposed task or perturbation?
- Artifact: Predicted BOLD dynamics, FC shift and virtual EC response

### Validate

- Guiding question: Does the simulation pass fidelity, stability and plausibility gates?
- Artifact: Signal R2, FC consistency, perturbation robustness and expert-review checklist

### Learn

- Guiding question: What should change in the next round?
- Artifact: Updated hypothesis ranking, model configuration, uncertainty target and experiment plan

## Next Upgrade

Add active-learning style experiment selection: the Learn stage should rank the next simulation by expected information gain, uncertainty reduction and validation cost.
