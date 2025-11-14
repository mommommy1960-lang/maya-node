# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
#
# MAYA Node - Development Makefile
# Provides convenient commands for common development tasks

.PHONY: help install install-dev test test-coverage lint format security check clean docs run

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
ISORT := $(PYTHON) -m isort
FLAKE8 := $(PYTHON) -m flake8
PYLINT := $(PYTHON) -m pylint
MYPY := $(PYTHON) -m mypy
BANDIT := $(PYTHON) -m bandit
SAFETY := $(PYTHON) -m safety

# Directories
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
FIRMWARE_DIR := firmware

help: ## Show this help message
	@echo "MAYA Node - Development Commands"
	@echo "================================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make install-dev    # Install development dependencies"
	@echo "  make test           # Run all tests"
	@echo "  make check          # Run all checks (lint + security + test)"
	@echo ""

install: ## Install production dependencies
	@echo "Installing production dependencies..."
	$(PIP) install -e .

install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
	$(PIP) install -e ".[dev]"
	@echo "Setting up pre-commit hooks..."
	pre-commit install
	@echo "✓ Development environment ready!"

install-docs: ## Install documentation dependencies
	@echo "Installing documentation dependencies..."
	$(PIP) install -e ".[docs]"

test: ## Run all tests
	@echo "Running tests..."
	$(PYTEST) $(TEST_DIR) -v

test-coverage: ## Run tests with coverage report
	@echo "Running tests with coverage..."
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html --cov-report=xml
	@echo "Coverage report generated in htmlcov/index.html"

test-runtime: ## Run runtime tests only
	@echo "Running runtime tests..."
	$(PYTEST) $(TEST_DIR)/runtime -v

test-ethics: ## Run ethics tests only
	@echo "Running ethics tests..."
	$(PYTEST) $(TEST_DIR)/ethics -v

test-ledger: ## Run ledger tests only
	@echo "Running ledger tests..."
	$(PYTEST) $(TEST_DIR)/ledger -v

lint: ## Run all linters
	@echo "Running linters..."
	@echo "→ Flake8..."
	-$(FLAKE8) $(SRC_DIR) $(TEST_DIR) --max-line-length=88 --extend-ignore=E203,W503
	@echo "→ Pylint..."
	-$(PYLINT) $(SRC_DIR) --exit-zero
	@echo "→ Type checking with mypy..."
	-$(MYPY) $(SRC_DIR) --ignore-missing-imports
	@echo "✓ Linting complete"

format: ## Format code with black and isort
	@echo "Formatting code..."
	@echo "→ isort..."
	$(ISORT) $(SRC_DIR) $(TEST_DIR) $(FIRMWARE_DIR)
	@echo "→ black..."
	$(BLACK) $(SRC_DIR) $(TEST_DIR) $(FIRMWARE_DIR)
	@echo "✓ Code formatted"

format-check: ## Check code formatting without modifying
	@echo "Checking code formatting..."
	$(BLACK) --check $(SRC_DIR) $(TEST_DIR) $(FIRMWARE_DIR)
	$(ISORT) --check-only $(SRC_DIR) $(TEST_DIR) $(FIRMWARE_DIR)

security: ## Run security checks
	@echo "Running security checks..."
	@echo "→ Bandit (code security)..."
	-$(BANDIT) -r $(SRC_DIR) -f text || true
	@echo "→ Safety (dependency vulnerabilities)..."
	-$(PIP) freeze | $(SAFETY) check --stdin || true
	@echo "✓ Security scan complete"

security-report: ## Generate detailed security report
	@echo "Generating security report..."
	$(BANDIT) -r $(SRC_DIR) -f json -o bandit-report.json || true
	$(BANDIT) -r $(SRC_DIR) -f html -o bandit-report.html || true
	@echo "Security reports generated:"
	@echo "  - bandit-report.json"
	@echo "  - bandit-report.html"

check: lint security test ## Run all checks (lint + security + test)
	@echo ""
	@echo "============================================"
	@echo "✓ All checks complete!"
	@echo "============================================"

check-cerl: ## Verify CERL-1.0 headers in all source files
	@echo "Checking for CERL-1.0 license headers..."
	@missing=0; \
	for file in $$(find $(SRC_DIR) $(TEST_DIR) -name "*.py"); do \
		if ! grep -q "CERL-1.0" "$$file"; then \
			echo "Missing CERL header: $$file"; \
			missing=$$((missing + 1)); \
		fi; \
	done; \
	if [ $$missing -gt 0 ]; then \
		echo "ERROR: $$missing files missing CERL-1.0 headers"; \
		exit 1; \
	else \
		echo "✓ All files have CERL-1.0 headers"; \
	fi

clean: ## Clean build artifacts and cache files
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.py,cover" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf coverage.xml
	rm -rf bandit-report.json
	rm -rf bandit-report.html
	@echo "✓ Clean complete"

clean-all: clean ## Clean everything including venv
	@echo "Cleaning virtual environment..."
	rm -rf venv/
	rm -rf env/
	@echo "✓ Deep clean complete"

docs: ## Build documentation
	@echo "Building documentation..."
	cd $(DOCS_DIR) && $(MAKE) html
	@echo "Documentation built in $(DOCS_DIR)/_build/html/"

docs-serve: docs ## Build and serve documentation locally
	@echo "Serving documentation at http://localhost:8000"
	cd $(DOCS_DIR)/_build/html && $(PYTHON) -m http.server

run: ## Run the Flask API server
	@echo "Starting Flask API server..."
	FLASK_APP=$(SRC_DIR)/api/endpoints.py FLASK_ENV=development $(PYTHON) -m flask run

run-debug: ## Run Flask API server with debug logging
	@echo "Starting Flask API server (debug mode)..."
	FLASK_APP=$(SRC_DIR)/api/endpoints.py FLASK_ENV=development FLASK_DEBUG=1 $(PYTHON) -m flask run

build: ## Build distribution packages
	@echo "Building distribution packages..."
	$(PYTHON) -m build
	@echo "✓ Build complete. Packages in dist/"

install-build-tools: ## Install build tools
	$(PIP) install --upgrade pip setuptools wheel build

version: ## Show version information
	@echo "MAYA Node version information:"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "pip: $$($(PIP) --version | cut -d' ' -f2)"
	@grep "version" pyproject.toml | head -1
	@echo ""
	@echo "Installed packages:"
	@$(PIP) list | grep -E "flask|pytest|black|pylint|bandit"

pre-commit: ## Run pre-commit hooks on all files
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

update-deps: ## Update all dependencies to latest versions
	@echo "Updating dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -e ".[dev]"
	@echo "✓ Dependencies updated"

freeze: ## Generate requirements.txt from current environment
	@echo "Freezing current environment..."
	$(PIP) freeze > requirements-frozen.txt
	@echo "Requirements saved to requirements-frozen.txt"

init: install-dev ## Initialize development environment (alias for install-dev)
	@echo "✓ Development environment initialized!"

ci: check-cerl lint security test ## Run CI checks locally
	@echo ""
	@echo "============================================"
	@echo "✓ CI checks complete!"
	@echo "============================================"

# Firmware-specific targets
firmware-test: ## Run firmware controller tests
	@echo "Running firmware tests..."
	cd $(FIRMWARE_DIR) && $(PYTEST) edge-tests/ -v

firmware-run: ## Run firmware controller
	@echo "Starting firmware controller..."
	cd $(FIRMWARE_DIR)/controller && $(PYTHON) main.py

# UI Dashboard targets (requires Node.js)
ui-install: ## Install UI dashboard dependencies
	@echo "Installing UI dashboard dependencies..."
	cd ui/web-dashboard && npm install

ui-dev: ## Run UI dashboard in development mode
	@echo "Starting UI dashboard (development)..."
	cd ui/web-dashboard && npm start

ui-build: ## Build UI dashboard for production
	@echo "Building UI dashboard..."
	cd ui/web-dashboard && npm run build

ui-test: ## Run UI dashboard tests
	@echo "Running UI tests..."
	cd ui/web-dashboard && npm test
