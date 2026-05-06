# Learn-Stage Acquisition Policy

Policy: **NeuroTwin Learn-stage acquisition policy**

The Learn stage should decide what to run next. In this demo, that decision is implemented as a transparent acquisition policy inspired by active learning and Bayesian optimization.

## Formula

```text
priority(a) = EIG(a) - lambda * Cost(a)
```

Current `lambda`: `0.35`

## Signals

- BOLD uncertainty = 1 - BOLD_R2
- FC gap = 1 - FC_corr
- Objective signal = abs(objective_delta)
- Validation cost = compute + data + experiment + expert-review burden

## Multi-Objective Audit Axes

- Fidelity gain
- Objective alignment
- Novelty
- Feasibility
- Risk control

## Programmable Policy State

Default portfolio weights:

| Axis | Weight |
| --- | ---: |
| fidelity | 0.32 |
| objective_alignment | 0.22 |
| novelty | 0.18 |
| feasibility | 0.16 |
| risk_control | 0.12 |

Preset policy profiles:

| Profile | Use case |
| --- | --- |
| Fidelity-first | Prioritize model reliability before external validation. |
| Exploration-first | Search for high-novelty mechanisms while keeping validation gates visible. |
| Risk-controlled | Prefer lower-risk candidates when downstream validation is expensive or sensitive. |

## Purpose

Select the next simulation or validation action that is expected to reduce uncertainty or improve the objective under realistic cost.

## Current Demo Ranking

| Scenario | Top next action | Priority | Why |
| --- | --- | ---: | --- |
| Emotional faces | Behavior endpoint alignment | 0.2037 | Connect the network-level shift to a task or behavioral readout. |
| Cognitive control | Behavior endpoint alignment | 0.1112 | Connect the network-level shift to a task or behavioral readout. |
| Closed-loop neuro experiment | Constrained policy search | 0.1671 | Optimize objective improvement under a small-perturbation budget. |

## Portfolio Audit

| Scenario | Top action | Fidelity | Objective | Novelty | Feasibility | Risk control | Portfolio |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Emotional faces | Behavior endpoint alignment | 0.8677 | 0.8968 | 0.61 | 0.4 | 0.7024 | 0.733 |
| Cognitive control | Behavior endpoint alignment | 0.6242 | 0.2577 | 0.61 | 0.4 | 0.7014 | 0.5144 |
| Closed-loop neuro experiment | Constrained policy search | 0.8082 | 0.4405 | 0.82 | 0.3333 | 0.5504 | 0.6225 |

## Negative Evidence

Low-priority actions are retained as routing evidence. They can help future policies avoid repeating weak experiment choices.

| Scenario | Low-priority actions |
| --- | --- |
| Emotional faces | Subject split generalization (0.0856); Atlas robustness test (0.083) |
| Cognitive control | Atlas robustness test (0.0636); Perturbation scale sweep (0.0183) |
| Closed-loop neuro experiment | Perturbation scale sweep (0.1055); Atlas robustness test (0.0885) |

## Upgrade Path

- Replace transparent heuristic EIG with posterior uncertainty from an ensemble, Bayesian neural network, or Gaussian process surrogate.
- Add multi-objective acquisition when the project needs to balance fidelity, biological plausibility, experimental cost and novelty.
- Log rejected actions as negative evidence so failed runs also improve the next round.
