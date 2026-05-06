# Repo Organization Guide

I organized NeuroTwin to read like a serious open-source research prototype rather than a submission folder.

## My Rules

1. Root files should explain how to run, test, and trust the project.
2. `src/` contains reusable code.
3. `scripts/` contains reproducible entry points.
4. `docs/` contains only documents I can defend in my own voice.
5. `artifacts/` contains generated outputs and stays ignored.
6. `application_materials/` contains private pitch/submission material and stays ignored.
7. `references/papers/` contains local PDFs and stays ignored.

## What I Removed From Public Docs

I removed old generated reports, duplicated Markdown exports, checklist-style submission notes, and process logs because they did not sound like a project designer explaining the system. If I need one of those details later, I will rewrite it as a short design note first.

## Upload Check

Before pushing, I check:

```bash
git remote -v
git status --short
make PYTHON=.venv/bin/python compile
make PYTHON=.venv/bin/python lint
make PYTHON=.venv/bin/python test
```

The remote must point to:

```text
git@github.com:Raphael-Camus/NeuroTwin.git
```
