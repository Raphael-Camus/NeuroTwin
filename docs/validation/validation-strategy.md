# Validation Strategy

I do not want NeuroTwin to overclaim. The validation layer exists to make the boundary between demo evidence and real evidence visible.

## My Ledger Gates

For every run, I check:

- **Signal fidelity**: does the surrogate reproduce BOLD-like dynamics well enough for a dry-run?
- **FC reproducibility**: does the generated signal preserve functional-connectivity structure?
- **Objective effect**: did the virtual perturbation move the target metric?
- **Perturbation budget**: is the candidate intervention small enough to remain plausible?
- **External evidence**: has this been tested on public or held-out data?

Only pass-gated signals should directly inform the next acquisition policy. Watch and review gates become next-cycle tasks.

## Public Data Path

The first real validation step I would run is an OpenNeuro BIDS smoke test:

```bash
python scripts/prepare_public_validation.py --scenario emotion --tier 1 \
  --output-prefix public_validation_openneuro_smoke
```

That scaffold does not download data. It defines the contract I need before I can claim more than a synthetic dry-run:

- BIDS validator output;
- ROI extraction QC;
- subject split file;
- motion/site/scanner summary;
- behavior or task endpoint note;
- updated validation ledger.
