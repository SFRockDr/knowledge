# ----- KaC convenience commands -----
PY?=python
ROOT?=./knowledge
SCHEMA?=./schema.json

.PHONY: validate graph hooks

validate:
	$(PY) validate_notes_v2.py --root $(ROOT) --schema $(SCHEMA)

graph:
	$(PY) build_graph.py --root $(ROOT) --out ./graph

hooks:
	pre-commit install
	pre-commit run --all-files
