# Research Notes

These are the research conclusions I want to keep in the public repo.

## My Reading of the Field

I do not treat digital twin brain as a single model. I treat it as a modeling objective: build a surrogate that can reproduce relevant brain dynamics, be perturbed under controlled assumptions, and be validated before interpretation.

The literature pushed me toward three decisions:

1. **Start at the ROI/network scale.** It matches fMRI resolution and keeps the prototype tractable.
2. **Separate surrogate fitting from validation.** A model can predict well and still be scientifically unsafe to interpret.
3. **Make perturbation explicit.** A digital twin is more useful when it can support counterfactual dry-runs, not just reconstruct observed signals.

## What I Am Not Claiming

I am not claiming clinical validity, personalized therapy, or causal ground truth. The current baseline is a workflow prototype that shows how those claims would have to be gated before they become credible.

## Next Research Step

The next research step is to replace synthetic ROI signals with a public BIDS dataset and preserve the same DSVL contract:

```text
BIDS data -> ROI time series -> surrogate dynamics -> virtual perturbation -> validation ledger -> next packet
```
