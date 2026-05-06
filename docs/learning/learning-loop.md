# Learning Loop

The Learn stage is where I turn the current result into the next experiment.

## Acquisition Policy

The current policy is transparent by design:

```text
priority = expected_information_gain - lambda * validation_cost
```

I rank next actions using:

- model uncertainty;
- FC gap;
- objective signal;
- feasibility;
- risk control;
- negative evidence.

This is not yet Bayesian optimization. It is a readable policy scaffold that I can later replace with BO while keeping the same artifact contract.

## Next Validation Packet

A next validation packet is my handoff object between DSVL cycles. It contains:

- scenario objective;
- current metric snapshot;
- linked evidence cards;
- top Learn-stage action;
- negative evidence;
- public validation candidate;
- required outputs;
- decision rule.

The packet makes the loop concrete: the previous run does not just produce a report; it produces the next executable validation step.
