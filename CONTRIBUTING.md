# Contributing

I maintain NeuroTwin as a personal research and engineering portfolio project. I welcome improvements when they preserve the project boundary: reusable AI4S workflow code belongs in the repo; generated artifacts, private pitch material, and real neuroimaging data do not.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

## Checks

Before I commit changes, I run:

```bash
make compile
make lint
make test
make demo
make validate
```

## Repository Boundaries

I do not commit:

- real subject MRI, DICOM, NIfTI, clinical records, or personally identifying data;
- generated files under `artifacts/demo/`;
- private pitch or application materials under `application_materials/`;
- local paper PDFs under `references/papers/`;
- virtual environments, caches, screenshots, or temporary render outputs.

If a contribution needs one of those assets, it should describe how to reproduce or obtain it locally instead of adding it to Git.
