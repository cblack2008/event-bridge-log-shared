# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python shared library for the Event Bridge Log Analytics Platform, providing common models and utilities for microservices. The package centralizes Pydantic event models and small AWS utilities used across multiple services.

## Development Commands

### Setup
- **Initial setup**: `make dev-setup` (installs dependencies and pre-commit hooks)
- **Manual setup**: `uv sync --extra dev && uv run pre-commit install`

### Testing & Quality
- **Run tests**: `make test` (runs pytest with coverage reporting to terminal)
- **HTML coverage**: `make coverage-html` (generates HTML coverage report and opens on macOS)
- **Lint check**: `make lint` (runs ruff, black --check, and mypy)
- **Auto-format**: `make format` (runs ruff --fix and black formatting)
- **Pre-commit all files**: `make precommit`
- **Pre-commit changed files**: `make precommit-changed`

### Build & Release
- **Clean artifacts**: `make clean` (removes caches, build artifacts)
- **Build package**: Uses hatchling via `pyproject.toml`
- **Release process**: Merge to main → Run "Release PR (manual)" GitHub Action → Merge Release PR

## Architecture

### Event System
- **Base class**: All events inherit from `BaseEvent` (src/event_bridge_log_shared/models/events/base.py:58)
- **Event types**: Defined in `EventType` enum (src/event_bridge_log_shared/models/events/base.py:16) using `domain.action` naming
- **Categories**: User, ecommerce, inventory, payment, analytics events
- **Auto-features**: UUID generation, timestamps, environment validation, EventBridge format conversion

### Package Structure
- **Models**: `src/event_bridge_log_shared/models/events/` (analytics.py, base.py, ecommerce.py, inventory.py, payment.py, user.py)
- **Utilities**: `src/event_bridge_log_shared/utils/config.py` (normalize_env, prefix_name, build_role_arn)
- **Version**: Dynamic versioning from `src/event_bridge_log_shared/_version.py`

### Configuration Philosophy
- Service-specific configuration belongs in individual services, not this shared package
- Shared package only provides pure utility functions and common models
- No hardcoded secrets or service-specific settings

## Code Quality Standards
- **Python version**: 3.13
- **Line length**: 100 characters (black and ruff)
- **Coverage requirement**: 85% minimum
- **Type checking**: Full mypy validation with strict settings
- **Pre-commit hooks**: Automatic formatting and validation

## Dependencies
- **Core**: pydantic >= 2.11.0, boto3 >= 1.40.0, structlog >= 23.0.0
- **Dev tools**: pytest, black, ruff, mypy, pre-commit
- **Package manager**: uv (modern Python package management)
