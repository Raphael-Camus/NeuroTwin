# Literature Research Brief

This brief records the current evidence backbone for NeuroTwin. Each item is translated into a concrete project design move.

## Current Insights

| Theme | Source | Insight | Project move |
| --- | --- | --- | --- |
| Agentic AI4S infrastructure | [Bohrium + SciMaster](https://arxiv.org/abs/2512.20469) | Scientific agents need stable tool interfaces, recorded execution traces, reusable capabilities and governance hooks. | Frame NeuroTwin as an agent-ready virtual experiment capability with contracts, trace memory and validation gates. |
| Personalised brain simulation | [The Virtual Brain on EBRAINS](https://ebrains.eu/data-tools-services/tools/the-virtual-brain) | MRI-derived structural and functional data can support personalised brain network model creation and multiscale simulation. | Position the demo as a lightweight surrogate layer that can later interoperate with TVB-style connectome and neural mass modeling. |
| Self-driving lab metrics | [Nature Communications SDL metrics and accessibility papers](https://www.nature.com/articles/s41467-024-45569-5) | Closed-loop scientific systems need explicit autonomy level, operational lifetime, repeatability, metadata and reproducibility metrics. | Add autonomy/readiness scoring and require each validation packet to record data, model, metrics and operator assumptions. |
| Hypothesis generation agents | [AI co-scientist](https://arxiv.org/abs/2502.18864) | Generate-debate-evolve workflows can turn literature-backed evidence into testable scientific hypotheses under human objectives. | Keep literature mining as Design-layer evidence cards, then route hypotheses through surrogate simulation and review gates. |
| Neuroimaging validation standards | [OpenNeuro, BIDS Validator, HCP and ABCD](https://docs.openneuro.org/packages/openneuro-cli.html) | Public neuroimaging validation requires BIDS-compatible data access, task/behavior context, QC, motion and site/scanner checks. | Extend public validation runbooks with BIDS checks, ROI QC, subject split metrics, behavior endpoints and cohort-stress constraints. |
| DBTL loop engineering | [DBTL cycle reviews](https://link.springer.com/article/10.1007/s13721-024-00455-4) | Design-Build-Test-Learn systems become useful when each cycle preserves decisions, measurements and model updates as reusable loop memory. | Map NeuroTwin's DSVL stages to evidence cards, virtual runs, validation packets and learning-memory updates. |
| Generative digital twins | [Neuroimaging digital twin reviews](https://academic.oup.com/cercor/article/35/1/bhae462/7930283) | Brain digital twins are stronger when they move from descriptive maps toward generative models that can test counterfactual interventions. | Treat effective-connectivity perturbation and next-run acquisition as counterfactual dry experiments under explicit validation gates. |

## Design Consequences

- Treat NeuroTwin as a platform capability with input/output contracts, execution traces and validation gates.
- Keep surrogate brain modeling connected to MRI-derived brain network simulation, with TVB-style multiscale modeling as a future extension.
- Record autonomy level, repeatability assumptions, dataset state, QC status and operator choices for each validation packet.
- Let literature and method mining generate evidence cards for Design, then require each hypothesis to pass simulation and review gates.
- Use BIDS/OpenNeuro/HCP/ABCD as staged validation resources, with motion, site/scanner and behavior-endpoint checks recorded separately from model score.

## Source Links

- Bohrium + SciMaster: https://arxiv.org/abs/2512.20469
- The Virtual Brain on EBRAINS: https://ebrains.eu/data-tools-services/tools/the-virtual-brain
- Self-driving lab metrics: https://www.nature.com/articles/s41467-024-45569-5
- Science acceleration with SDLs: https://www.nature.com/articles/s41467-025-59231-1
- AI co-scientist: https://arxiv.org/abs/2502.18864
- OpenNeuro CLI: https://docs.openneuro.org/packages/openneuro-cli.html
- BIDS Validator: https://github.com/bids-standard/bids-validator
- ABCD imaging data sharing: https://abcdstudy.org/scientists/data-sharing/fast-track-imaging-data-release/
