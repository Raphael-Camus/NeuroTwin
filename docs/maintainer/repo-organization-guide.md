# NeuroTwin Repo Organization Guide

This guide records the cleanup decisions used to convert the original working folder into a GitHub-ready repository. The structure follows common patterns from mature Python and data-science repositories: `src/` layout for importable code, `scripts/` for reproducible entry points, `docs/` for curated documentation, and ignored artifact/data folders for generated or local files.

References used for the layout:

- PyOpenSci Python packaging guide: https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html
- Cookiecutter Data Science: https://github.com/drivendataorg/cookiecutter-data-science
- Real Python project layout guide: https://realpython.com/ref/best-practices/project-layout/

## 1. Recommended GitHub Directory Tree

```text
NeuroTwin/
  README.md                               <- rewritten public project entry
  LICENSE                                 <- MIT license
  pyproject.toml                          <- Python package metadata
  requirements.txt                        <- runtime dependencies
  requirements-dev.txt                    <- tests/report generation dependencies
  .github/workflows/ci.yml                <- GitHub Actions smoke test
  src/
    neurotwin/
      __init__.py
      core.py                             <- from demo/brain_twin_core.py
  scripts/
    run_demo.py                           <- from demo/run_demo.py
    prepare_public_validation.py          <- from demo/prepare_public_validation.py
    build_demo_submission_pdf.py          <- from demo/build_demo_submission_pdf.py
    build_project_proposal_pdf.py         <- from demo/build_project_proposal_pdf.py
  docs/
    architecture/
      technical-design.md                 <- from demo/technical_design.md
      dsvl-loop.md                        <- from demo/dist/scientific_loop.md
      theoretical-model.md                <- from demo/dist/theoretical_model.md
      platform-architecture.md            <- from demo/dist/platform_architecture.md
      virtual-experiment-world.md         <- from demo/dist/virtual_experiment_world.md
      data-interface-boundary.md          <- from demo/dist/data_interface_boundary.md
      experiment-os-policy.md             <- from demo/dist/experiment_os_policy.md
      capability-card.md                  <- from demo/dist/capability_card.md
    validation/
      validation-ledger.md                <- from demo/dist/validation_ledger.md
      public-validation-bridge.md         <- from demo/dist/public_validation_bridge.md
      public-validation-runbook.md        <- from demo/dist/public_validation_runbook.md
      public-validation-protocol-template.md
      openneuro-smoke-runbook.md
      openneuro-smoke-protocol-template.md
    evidence/
      evidence-card-schema.md             <- from demo/dist/evidence_card_schema.md
      literature-research-brief.md        <- from demo/dist/literature_research_brief.md
    agent/
      agent-skill-registry.md             <- from demo/dist/agent_skill_registry.md
    learning/
      acquisition-policy.md               <- from demo/dist/acquisition_policy.md
      next-experiment-plan.md             <- from demo/dist/next_experiment_plan.md
      next-validation-packet.md           <- from demo/dist/next_validation_packet.md
    research/
      research-plan.md                    <- from docs/RESEARCH_PLAN.md
      literature-review.md                <- from docs/LITERATURE_REVIEW.md
      ai-surrogate-brain-review-summary.md
      three-paper-synthesis-and-directions.md
      project-log.md
    demo/
      demo-overview.md                    <- from demo/README.md
      demo-report.md                      <- from demo/dist/demo_report.md
    maintainer/
      repo-organization-guide.md          <- this file
  data/
    README.md
    raw/                                  <- ignored; local BIDS/OpenNeuro inputs
    processed/                            <- ignored except .gitkeep
  artifacts/
    README.md
    demo/                                 <- ignored generated HTML/JSON/PDF
  references/
    README.md
    papers/                               <- ignored local PDFs
  application_materials/
    README.md                             <- tracked marker only
    pitch_narrative.md                    <- ignored local file
    proposal_500.md                       <- ignored local file
    product_strategy_note.md              <- ignored local file
    output/                               <- ignored exports and submission zips
  tests/
    test_core.py
```

Ignored or local-only folders:

- `artifacts/`: generated HTML, JSON, JSONL, PDF, and favicon outputs.
- `application_materials/`: pitch scripts, proposal copies, exported submission packages.
- `references/papers/`: local paper PDFs.
- `tmp/`, `.playwright-cli/`, `.swift-module-cache/`: tool caches and rendering scratch space.
- `data/raw/`, `data/processed/`: local neuroimaging data and derived ROI files.

## 2. File Cleanup and Classification

### Core Source Area

Place only reusable Python logic and package code in `src/`:

- `src/neurotwin/core.py`: scenario definitions, synthetic ROI dynamics, surrogate fitting, FC/EC metrics, intervention summaries.
- `src/neurotwin/__init__.py`: minimal public package exports.

Keep executable workflow scripts in `scripts/`:

- `scripts/run_demo.py`
- `scripts/prepare_public_validation.py`
- `scripts/build_demo_submission_pdf.py`
- `scripts/build_project_proposal_pdf.py`

### Technical Documentation Area

Use `docs/architecture/` for system design:

- `technical-design.md`
- `dsvl-loop.md`
- `theoretical-model.md`
- `platform-architecture.md`
- `virtual-experiment-world.md`
- `data-interface-boundary.md`
- `experiment-os-policy.md`
- `capability-card.md`

Use `docs/validation/` for scientific credibility and public-data route:

- `validation-ledger.md`
- `public-validation-bridge.md`
- `public-validation-runbook.md`
- `public-validation-protocol-template.md`
- `openneuro-smoke-runbook.md`
- `openneuro-smoke-protocol-template.md`

Use `docs/evidence/`, `docs/agent/`, and `docs/learning/` for DSVL support layers:

- `evidence-card-schema.md`
- `literature-research-brief.md`
- `agent-skill-registry.md`
- `acquisition-policy.md`
- `next-validation-packet.md`
- `next-experiment-plan.md`

Use `docs/research/` for long-form research notes and literature synthesis.

### Application_Materials

Keep application-specific materials out of the public technical surface:

- `pitch_narrative.md`
- `proposal_500.md`
- `demo_submission.md`
- `product_strategy_note.md`
- `submission_checklist.md`
- `submission_materials_and_desensitization.md`
- exported PDFs, zips, and mirrored submission folders

They are placed under `application_materials/` and ignored by `.gitignore`. Only `application_materials/README.md` is tracked to explain the boundary.

### Ignored or Generated Files

Do not commit generated files unless there is a deliberate release reason:

- `artifacts/demo/brain_twin_lab.html`
- `artifacts/demo/demo_data.json`
- `artifacts/demo/evidence_cards.json`
- `artifacts/demo/next_validation_packet.json`
- `artifacts/demo/experiment_trace.jsonl`
- `artifacts/demo/*.pdf`
- `artifacts/demo/*manifest.json`
- `artifacts/demo/*protocol_template.json`

Regenerate them with:

```bash
python scripts/run_demo.py
python scripts/prepare_public_validation.py
python scripts/prepare_public_validation.py --scenario emotion --tier 1 --output-prefix public_validation_openneuro_smoke
```

## 3. Main README Outline

The public `README.md` should contain:

- **Badges**: Python version, license, status, and later CI.
- **Project Overview**: one sentence describing NeuroTwin as an AI4S surrogate-brain DSVL workflow.
- **DSVL Loop & Architecture**: Mermaid diagram and short explanation of Design, Simulate, Validate, Learn.
- **Quick Start**: environment setup, `python scripts/run_demo.py`, validation scaffold generation, and static HTML serving.
- **Repository Structure**: short tree explaining `src/`, `scripts/`, `docs/`, `data/`, `artifacts/`, `application_materials/`.
- **Baseline Scope**: honest list of implemented vs not implemented capabilities.
- **Roadmap**: public OpenNeuro smoke test, subject-aware surrogate, Bayesian optimization, human-in-the-loop gates, agent-ready API.
- **License**: MIT or the user's preferred open-source license.

## 4. Engineering Configuration

Recommended `.gitignore` policy:

```gitignore
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.ruff_cache/
.DS_Store
tmp/
.playwright-cli/
.swift-module-cache/
artifacts/**
!artifacts/README.md
application_materials/**
!application_materials/README.md
references/papers/**
data/raw/
data/processed/*
```

Dependency policy:

- Keep `requirements.txt` curated and minimal. For this baseline, `numpy>=1.26` is enough for core demo generation.
- Keep PDF/report/testing tools in `requirements-dev.txt`.
- Avoid committing `pip freeze` output from a large local environment.

If you want to regenerate a lock-style requirements file from a clean virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip freeze > requirements-lock.txt
```

Only commit `requirements-lock.txt` if reproducible deployment matters more than readability.

## GitHub Upload Guide

Before pushing, confirm that the target account is the user's account:

```bash
git remote -v
gh auth status
```

Proceed only if the remote points to `Raphael-Camus/NeuroTwin` and GitHub CLI reports the intended account. Do not push to a connector account such as `sunaedros`.

After creating an empty repository named `NeuroTwin` under `Raphael-Camus`, run:

```bash
git add README.md LICENSE pyproject.toml requirements.txt requirements-dev.txt .gitignore .github src scripts docs data results artifacts references application_materials tests
git commit -m "Initial clean NeuroTwin repository"
git branch -M main
git remote add origin https://github.com/Raphael-Camus/NeuroTwin.git
git push -u origin main
```

If you use GitHub CLI:

```bash
brew install gh
gh auth login
gh repo create Raphael-Camus/NeuroTwin --public --source=. --remote=origin --push
```
