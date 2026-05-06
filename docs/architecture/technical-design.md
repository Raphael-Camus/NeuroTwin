# Technical Design

## 1. Capability Contract

NeuroTwin is designed as an agent-ready scientific capability built around a DSVL loop: Design, Simulate, Validate and Learn.

### Input

- ROI-level fMRI time series: `T x N`
- Brain atlas metadata: network names and ROI groups
- Scenario definition: task stimulus, candidate intervention, objective
- Optional subject metadata: cohort, session, behavioral score

### Output

- Predicted BOLD dynamics
- Functional connectivity matrix
- Virtual effective connectivity matrix
- Candidate perturbation score
- Validation metrics
- Replayable experiment trace
- Learn-stage next simulation ranking
- Multi-objective acquisition portfolio

## 2. Minimal Demo Model

The Demo uses a lightweight ridge one-step surrogate:

```text
x(t + 1) = f_theta(x(t))
```

For a real version, this can be replaced by:

- GRU/LSTM for low-data task fMRI;
- graph temporal network for explicit brain topology;
- hypernetwork + main network for subject personalization;
- transformer/Mamba sequence model for larger datasets.

## 3. Virtual Perturbation

After fitting the surrogate, each brain network is perturbed in model state space:

```text
EC[i, j] = mean_t f(x_t + delta * e_i)[j] - f(x_t)[j]
```

This follows the NPI-style idea: use a trained surrogate brain as a virtual experimental object.

## 4. Closed-Loop Upgrade Path

### Phase 1: Synthetic DSVL Demo

- Synthetic ROI time series
- Static web dashboard
- Automatically generated report

### Phase 2: Public fMRI Dataset

- Replace synthetic signal with public task or resting-state fMRI
- Add preprocessing notebook
- Evaluate model fidelity and FC consistency

### Phase 3: Agentic Workflow

- Package preprocessing, training, perturbation and report generation as callable tools
- Add schemas, logging and replayable traces
- Expose the capability to a scientific agent
- Add active-learning criteria for selecting the next simulation

### Phase 4: Dry-Wet Learning Feedback

- Connect candidate perturbation to behavioral task, neurofeedback, cell assay, organoid signal, or neuromodulation experiment
- Feed validation results back into model selection and objective design

## 5. Why This Fits AI for Science

The proposal extends AI4S from molecular and material design toward system-level biological phenotype simulation. It gives molecular/protein/gene models a downstream phenotype sandbox: if a candidate mechanism is proposed, NeuroTwin can ask what network-level brain phenotype it may shift, what uncertainty remains, and what experiment should be run next.

## 6. Learn-Stage Selection

The current demo approximates active experiment selection with a transparent ranking:

```text
priority = expected_information_gain - lambda * validation_cost
```

The score uses four interpretable signals:

- BOLD uncertainty: how much prediction fidelity remains to be improved;
- FC gap: how much generated functional connectivity differs from the simulated reference;
- objective signal: whether the candidate perturbation changes the target in a useful direction;
- validation cost: compute, data, experiment and expert-review burden.

This makes the Learn stage operational: the system can recommend the next simulation instead of only reporting the current result.

The dashboard now renders the loop as:

```text
current evidence -> next run
```

This small UI element is important because it makes the feedback mechanism visible: every validation result becomes a decision signal for the next simulation.

Low-priority candidate actions are stored as negative evidence. This mirrors real closed-loop scientific work: failed or weak options still carry information and should improve future routing, acquisition scoring and experiment design.

## 7. Virtual Experimental World

The demo now exposes the surrogate loop as a small virtual experimental world:

- Problem Space: task context, target phenotype, objective and constraints;
- Surrogate Simulator: BOLD dynamics, FC shift and virtual EC response;
- Evidence Gates: fidelity, robustness, plausibility and validation cost;
- Learning Memory: acquisition portfolio, top choices, weak actions and uncertainty targets.

This framing makes the project closer to an AI4S platform capability. The value is a repeatable environment for selecting, running and learning from virtual experiments.

## 8. Multi-Objective Acquisition Portfolio

The priority score remains transparent:

```text
priority(a) = EIG(a) - lambda * Cost(a)
```

Each candidate is also audited through five axes:

- fidelity gain;
- objective alignment;
- novelty;
- feasibility;
- risk control.

This helps explain why one next experiment is useful, whether it is feasible, and how much uncertainty or risk it carries before any costly validation is triggered.

## 9. Programmable Experiment Policy

The dashboard now exposes acquisition weights as an inspectable policy state. The default weights are stored in `demo_data.json` for reproducibility, and the HTML page provides sliders for:

- fidelity;
- objective alignment;
- novelty;
- feasibility;
- risk control.

Changing the weights reranks the acquisition portfolio and updates the visible next-run transition. This turns the Learn stage into a small experiment-operation policy: different teams can choose reliability-first, exploration-first or risk-controlled modes while preserving the same validation trace.

## 10. Data Interface Boundary

Literature parsing, data extraction, data cleaning and feature engineering are positioned as Design-layer inputs. They improve hypothesis sourcing, data readiness and representation choices before the surrogate experiment runs.

The boundary is:

- literature and method mining produce evidence cards and hypothesis seeds;
- data extraction and cleaning produce QC reports, ROI time series and dataset cards;
- feature engineering produces optional context such as FC priors, task labels and phenotype scores;
- the virtual experiment core trains the surrogate, runs perturbations, validates outputs and updates the acquisition policy.

This keeps the project scientifically focused: knowledge and data interfaces provide input quality, while the DSVL engine provides executable simulation and learning feedback.

## 11. Platform Architecture

The submission now includes `artifacts/demo/platform_architecture.md` with a Mermaid architecture map:

```text
Knowledge Input -> Data Readiness -> NeuroTwin Virtual World
-> Validation Gates -> Programmable Acquisition Policy
-> Next Experiment -> Learning Memory -> Knowledge Input
```

This makes the enterprise fit explicit: NeuroTwin can be presented as a platform capability with clear inputs, execution, validation, policy state and trace memory.

The web demo now mirrors the same architecture in the first screen as **AI4S Platform Route**, so reviewers can see the full route from knowledge inputs and data readiness to surrogate simulation, validation, policy selection and learning memory without opening extra files.

## 12. Scientific Validation Ledger

The demo now adds `artifacts/demo/validation_ledger.md` and a visible web panel. Each scenario is checked through:

- signal fidelity;
- FC reproducibility;
- objective effect;
- perturbation budget;
- external evidence.

Each gate returns `pass`, `watch`, `review` or `hold`. The Learn stage can only treat pass-gated signals as direct acquisition evidence. Watch and review gates become explicit validation tasks for the next DSVL cycle. This makes the project easier to defend scientifically because uncertainty, synthetic-data limits and expert-review requirements are shown in the same place as model scores.

## 13. Public Validation Bridge

The review gate now creates a staged validation queue:

- OpenNeuro BIDS smoke test for the first public-data run;
- HCP task-fMRI transfer check for high-quality task validation;
- ABCD cohort stress test when controlled access and governance are clear.

This connects the synthetic Demo to a realistic data path. It also makes the AI4S loop more credible: external evidence becomes an executable next-cycle task with a concrete success gate.

## 14. Public Validation Scaffold

The demo now includes `scripts/prepare_public_validation.py`, a dry scaffold that turns the review queue into a concrete public-data validation preparation step. The script performs no dataset download and makes no clinical claim. It reads `artifacts/demo/demo_data.json`, then emits:

- `artifacts/demo/public_validation_manifest.json`: dataset input contract, official tool templates, validation bridge, scenario review summary and minimum artifact list;
- `artifacts/demo/public_validation_runbook.md`: operator-facing steps for OpenNeuro dataset selection, BIDS validation, ROI extraction, surrogate rerun and metric backfill.

This makes the external-evidence gate more operational. A reviewer can see which accession must be chosen, which BIDS checks must pass, which metrics must be updated, and which artifacts are expected before a synthetic result is promoted into stronger evidence.

The script also supports focused preparation:

```bash
python scripts/prepare_public_validation.py --scenario emotion --tier 1 --output-prefix public_validation_openneuro_smoke
```

This emits `artifacts/demo/public_validation_openneuro_smoke_manifest.json` and `artifacts/demo/public_validation_openneuro_smoke_runbook.md`. The focused files show a narrower path: one scenario, the P1 OpenNeuro BIDS smoke test, and the exact artifacts needed to update the validation ledger.

## 15. Literature-Backed Evidence Backbone

The demo now records an evidence backbone in `artifacts/demo/literature_research_brief.md` and `demo_data.json`. The current design moves are:

- Bohrium + SciMaster: package NeuroTwin as an agent-ready capability with contracts, trace memory and validation gates.
- The Virtual Brain on EBRAINS: keep a future path toward MRI-derived personalised brain network modeling and multiscale simulation.
- Self-driving lab metrics: record autonomy/readiness, repeatability, metadata and operator assumptions in every validation packet.
- AI co-scientist: let literature mining generate evidence cards for Design, then route hypotheses through simulation and review gates.
- OpenNeuro/BIDS/HCP/ABCD: require BIDS checks, ROI QC, motion/site/scanner summaries, behavior endpoints and cohort-stress constraints before stronger claims.

This makes the project easier to defend as AI4S: the literature interface supplies evidence-grounded hypotheses, the surrogate world executes virtual experiments, and the validation scaffold records the standards needed to move from synthetic demo to public fMRI.

## 16. Evidence-Card Interface

The literature/mining interface now has an explicit output contract:

- `artifacts/demo/evidence_cards.json`: machine-readable cards from literature or standards to Design-stage inputs;
- `artifacts/demo/evidence_card_schema.md`: field definitions and current cards.

Each card records a source theme, evidence claim, Design input, surrogate requirement, validation gate, risk and next action. This is useful because literature parsing can feed the project without dominating it: every extracted claim must become a testable scenario input, a simulator requirement, a validation gate or a learning-memory update.

The schema also bridges DSVL with DBTL/DMTA language. Design maps to evidence cards and objectives; Simulate maps to virtual build/run; Validate maps to test/review packets; Learn maps to analysis, negative evidence and next acquisition policy.

## 17. Public Validation Protocol Template

`scripts/prepare_public_validation.py` now emits protocol templates:

- `artifacts/demo/public_validation_protocol_template.md` and `.json` for the full review queue;
- `artifacts/demo/public_validation_openneuro_smoke_protocol_template.md` and `.json` for the P1 OpenNeuro smoke-test packet.

The template records:

- BIDS contract: `dataset_description.json`, `participants.tsv`, task events and validator JSON;
- preprocessing contract: fMRIPrep-style confounds, framewise displacement, DVARS, motion outliers, site/scanner labels;
- atlas contract: space, atlas name, ROI labels, extraction tool, minimum timepoints and missing-ROI threshold;
- split policy: subject-level split, stratification fields, fixed seed and leakage rule;
- QC thresholds: proposed motion review defaults, BOLD R2 and FC corr pass gates;
- required outputs: BIDS report, ROI QC, split file, motion/site summary, endpoint note, updated ledger and acquisition portfolio.

This gives the public-data route a concrete operating protocol before model scores are interpreted.

## 18. Agent Skill Registry and Next Validation Packet

To better match a Deep Potential style AI4S platform, the demo now exposes two additional operating artifacts:

- `artifacts/demo/agent_skill_registry.md`: a route of callable skills across Read, Prepare, Build, Compute, Validate and Learn.
- `artifacts/demo/next_validation_packet.md` and `.json`: the handoff object that carries one cycle into the next.

The skill registry describes what each platform tool consumes, emits and gates. The current route is:

```text
EvidenceCardBuilder -> BIDSValidationPlanner -> ROITimeSeriesExtractor
-> SurrogateTrainer -> PerturbationSimulator -> ValidationLedgerWriter
-> AcquisitionPolicyOptimizer -> NextValidationPacketBuilder
```

The next validation packet records:

- scenario objective and current metric snapshot;
- linked evidence cards and their validation gates;
- public validation candidate and protocol files;
- Learn-stage top action and multi-objective profile;
- negative evidence retained for routing;
- required outputs before the ledger can be updated.

This makes the AI acceleration loop concrete. Each run creates a small decision object, the Agent can route it to the next validation task, and the result can return to the validation ledger and acquisition policy.
