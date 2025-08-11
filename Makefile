SHELL := /bin/bash
.DEFAULT_GOAL := help

.PHONY: dev-setup hooks format lint test coverage-html precommit precommit-changed clean help

dev-setup: ## One-time developer setup (deps + hooks)
	uv sync --extra dev
	@if command -v git &>/dev/null && git rev-parse --is-inside-work-tree &>/dev/null; then \
		uv run pre-commit install; \
		echo "pre-commit hooks installed"; \
	else \
		echo "Skipping pre-commit install (not a git repo)"; \
	fi

hooks: ## Install pre-commit hooks (pinned; no autoupdate)
	uv sync --extra dev
	uv run pre-commit install

format: ## Auto-format (black) and auto-fix lint (ruff)
	uv run black src/ tests/
	uv run ruff check --fix src/ tests/

lint: ## Lint (no fixes) + type check
	uv run ruff check src/ tests/
	uv run black --check src/ tests/
	uv run mypy src/

test: ## Run tests with coverage (terminal)
	uv run pytest --cov=src/event_bridge_log_shared --cov-report=term-missing

coverage-html: ## Generate HTML coverage report and open (macOS)
	uv run pytest --cov=src/event_bridge_log_shared --cov-report=html
	open htmlcov/index.html

precommit: ## Run all pre-commit hooks against all files
	uv run pre-commit run --all-files

precommit-changed: ## Run pre-commit hooks on staged/changed files only
	uv run pre-commit run

clean: ## Remove caches and build artifacts
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache htmlcov dist build *.egg-info

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
