"""
Test suite for configuration management.
"""
import os

import pytest
from event_bridge_log_shared.utils.config import (
    build_role_arn,
    normalize_env,
    prefix_name,
)


class TestHelpers:
    def test_normalize_env(self):
        assert normalize_env("development") == "dev"
        assert normalize_env("dev") == "dev"
        assert normalize_env("production") == "prod"
        assert normalize_env("prod") == "prod"
        assert normalize_env(None) == "dev"

    def test_prefix_name(self):
        assert prefix_name("dev", "events") == "dev-events"
        assert prefix_name("prod", "prod-events") == "prod-events"

    def test_build_role_arn(self):
        arn = build_role_arn("123456789012", "DeployRole")
        assert arn == "arn:aws:iam::123456789012:role/DeployRole"


class TestNoOp:  # placeholder to keep file organized for future helper tests
    def test_sanity(self):
        assert True


@pytest.fixture
def mock_environment():
    """Fixture to provide clean environment for testing."""
    original_env = os.environ.copy()

    # Clear relevant environment variables
    env_vars_to_clear = [
        "ENVIRONMENT",
        "DEBUG",
        "LOG_LEVEL",
        "AWS_REGION",
        "AWS_DEV_ACCOUNT_ID",
        "AWS_PROD_ACCOUNT_ID",
    ]

    for var in env_vars_to_clear:
        os.environ.pop(var, None)

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestConfigurationIsolation:
    """Placeholder isolation tests (no global settings to test)."""

    def test_isolation_1(self, mock_environment):
        assert os.environ.get("ENVIRONMENT") is None

    def test_isolation_2(self, mock_environment):
        assert os.environ.get("ENVIRONMENT") is None
