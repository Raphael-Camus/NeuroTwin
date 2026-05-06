# Evidence Card Schema

Evidence cards are the interface between literature/method mining and the DSVL Design stage. They convert external knowledge into testable inputs, surrogate requirements and validation gates.

## Schema Fields

| Field | Meaning |
| --- | --- |
| `card_id` | Stable card identifier. |
| `source_theme` | Research theme or infrastructure standard. |
| `evidence_claim` | Condensed claim extracted from literature or standards. |
| `design_input` | How the claim enters the DSVL Design stage. |
| `surrogate_requirement` | What the surrogate or virtual world must support. |
| `validation_gate` | Gate or artifact needed before stronger claims. |
| `risk_to_track` | Failure mode that must stay visible. |
| `next_action` | Concrete next project action. |
| `source_url` | Source link for review. |

## Current Cards

| Card | Theme | Design input | Validation gate |
| --- | --- | --- | --- |
| EC-001 | Agentic AI4S infrastructure | Require every NeuroTwin run to declare inputs, outputs, gates and trace identifiers. | Capability card and experiment trace must be generated for each run. |
| EC-002 | Personalised brain simulation | Represent fMRI/structural MRI as subject-specific context for future surrogate fitting. | Record atlas, connectome, ROI extraction and subject split assumptions. |
| EC-003 | Self-driving lab metrics | Treat each validation packet as a loop-memory object with dataset, model and operator metadata. | Runbook must include QC, endpoint, split and repeatability requirements. |
| EC-004 | Hypothesis generation agents | Use literature parsing to generate evidence cards instead of free-text method notes. | Human review keeps hypothesis quality and translational claims bounded. |
| EC-005 | Neuroimaging validation standards | Select OpenNeuro/HCP/ABCD validation tiers based on task fit, access and governance. | Manifest must include BIDS validation, ROI QC, motion/site/scanner and endpoint fields. |
| EC-006 | DBTL loop engineering | Map DSVL to DBTL/DMTA language for AI4S reviewers: design, virtual build/run, validate/test, learn/analyze. | Next-run plan must cite what was learned from current pass/watch/review gates. |
| EC-007 | Generative digital twins | Define each perturbation as a counterfactual dry experiment with a measurable objective. | Counterfactual claims require external evidence review before translational interpretation. |

## Why This Matters

This schema keeps literature parsing useful as an AI4S interface: extracted evidence must become a scenario input, surrogate requirement, validation gate, risk record or next action.
