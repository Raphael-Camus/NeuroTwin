# Programmable Experiment OS Policy

This note explains how the Learn stage can behave like a small programmable experiment-operation policy.

## Policy State

```json
{
  "priority_formula": "priority(a) = EIG(a) - lambda * Cost(a)",
  "portfolio_weights": {
    "fidelity": 0.32,
    "objective_alignment": 0.22,
    "novelty": 0.18,
    "feasibility": 0.16,
    "risk_control": 0.12
  },
  "decision_memory": [
    "ranked_actions",
    "negative_evidence",
    "next_experiment"
  ]
}
```

## Why This Matters

A scientific loop becomes more useful when its next-step policy can be inspected and adjusted. In NeuroTwin, changing the acquisition weights simulates different operating modes: reliability-first, exploration-first, or risk-controlled validation.

## Preset Profiles

| Profile | Use case | Weights |
| --- | --- | --- |
| Fidelity-first | Prioritize model reliability before external validation. | fidelity=0.42, objective_alignment=0.18, novelty=0.1, feasibility=0.16, risk_control=0.14 |
| Exploration-first | Search for high-novelty mechanisms while keeping validation gates visible. | fidelity=0.22, objective_alignment=0.2, novelty=0.32, feasibility=0.12, risk_control=0.14 |
| Risk-controlled | Prefer lower-risk candidates when downstream validation is expensive or sensitive. | fidelity=0.24, objective_alignment=0.18, novelty=0.12, feasibility=0.2, risk_control=0.26 |

## Demo Behavior

- The static JSON stores default weights for reproducibility.
- The HTML dashboard exposes sliders for the five acquisition axes.
- Changing weights reranks the visible acquisition portfolio and updates the next-run transition.
- Negative evidence remains logged even when a different weight profile changes the top action.
