.PHONY: help venv install dev-install clean lint test docs

VENV = .venv
PYTHON = python3

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  venv         Create Python virtual environment"
	@echo "  install      Create venv + install dev dependencies + optimizers package"
	@echo "  dev-install  All of the above + Sphinx"
	@echo "  clean        Remove venv, caches, and build artifacts"
	@echo "  lint         Run pre-commit hooks on all files"
	@echo "  test         Run pytest"
	@echo "  docs         Build Sphinx HTML documentation"

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(VENV)/bin/pip install -r dev-requirements.txt
	$(VENV)/bin/pip install -e optimizers/

dev-install: install
	$(VENV)/bin/pip install sphinx

clean:
	rm -rf $(VENV)
	rm -rf .venv
	rm -rf **/__pycache__
	rm -rf .pytest_cache
	rm -rf docs/_build
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null; true

lint:
	$(VENV)/bin/pre-commit run --all-files

test:
	$(VENV)/bin/pytest

docs:
	$(VENV)/bin/sphinx-apidoc -o docs/ optimizers/src/ --force
	$(VENV)/bin/sphinx-build -b html docs/ docs/_build/html
