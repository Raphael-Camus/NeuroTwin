.PHONY: install install-dev test lint compile demo validate clean

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

compile:
	$(PYTHON) -m py_compile src/neurotwin/core.py \
		scripts/run_demo.py \
		scripts/prepare_public_validation.py \
		scripts/build_demo_submission_pdf.py \
		scripts/build_project_proposal_pdf.py

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest

demo:
	$(PYTHON) scripts/run_demo.py
	$(PYTHON) scripts/prepare_public_validation.py
	$(PYTHON) scripts/prepare_public_validation.py --scenario emotion --tier 1 --output-prefix public_validation_openneuro_smoke

validate:
	$(PYTHON) -m json.tool artifacts/demo/demo_data.json >/dev/null
	$(PYTHON) -m json.tool artifacts/demo/evidence_cards.json >/dev/null
	$(PYTHON) -m json.tool artifacts/demo/next_validation_packet.json >/dev/null
	$(PYTHON) -m json.tool artifacts/demo/public_validation_manifest.json >/dev/null
	$(PYTHON) -m json.tool artifacts/demo/public_validation_openneuro_smoke_manifest.json >/dev/null

clean:
	rm -rf artifacts/demo .pytest_cache .ruff_cache
