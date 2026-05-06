# Demo Overview

The NeuroTwin demo is a no-backend static dashboard generated from a synthetic ROI-level surrogate-brain run. It demonstrates the full DSVL contract without committing generated artifacts to Git.

## Run

```bash
python scripts/run_demo.py
python scripts/prepare_public_validation.py
python scripts/prepare_public_validation.py --scenario emotion --tier 1 --output-prefix public_validation_openneuro_smoke
python -m http.server 8769 --directory artifacts/demo
```

Open:

```text
http://127.0.0.1:8769/brain_twin_lab.html
```

## Generated Files

The scripts write to `artifacts/demo/`, which is ignored by Git:

- `brain_twin_lab.html`: interactive static dashboard;
- `demo_data.json`: synthetic ROI signals, model outputs, validation ledger, and learning packet state;
- `evidence_cards.json`: structured Design-stage evidence objects;
- `next_validation_packet.json`: scenario-to-next-cycle handoff;
- `public_validation_manifest.json`: public-data validation scaffold;
- `public_validation_openneuro_smoke_manifest.json`: focused P1 OpenNeuro smoke-test scaffold;
- `experiment_trace.jsonl`: replayable execution trace.

## Demo Scenarios

- **Emotional faces**: visual input recruits limbic and salience circuits.
- **Cognitive control**: attention and frontoparietal networks coordinate control.
- **Closed-loop neuro experiment**: candidate perturbation is reranked through validation and learning gates.

## What To Show

1. AI4S Platform Route: how the virtual experiment layer fits a larger scientific workflow.
2. Virtual Perturbation Map: how the surrogate responds to counterfactual network perturbations.
3. Validation Ledger: how pass/watch/review/hold gates prevent overclaiming.
4. Agent Loop Route: how Read, Prepare, Build, Compute, Validate, and Learn become callable steps.
5. Next Validation Packet: how one DSVL cycle hands off to the next public-data validation step.
6. Programmable Acquisition Policy: how fidelity, objective alignment, novelty, feasibility, and risk control rerank next experiments.
