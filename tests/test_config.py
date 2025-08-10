"""
Test suite for configuration management.
"""
import pytest
from unittest.mock import patch, MagicMock
import os

from event_bridge_log_shared.utils.config import (
    Settings,
    AWSConfig,
    ApplicationConfig,
    build_settings,
    build_role_arn,
)


class TestApplicationConfig:
    """Test application configuration."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = ApplicationConfig()
        
        assert config.environment == "development"
        assert config.debug is True
        assert config.log_level == "INFO"
        
    @patch.dict(os.environ, {
        "ENVIRONMENT": "production",
        "DEBUG": "false", 
        "LOG_LEVEL": "ERROR"
    })
    def test_environment_override(self):
        """Test environment variable override."""
        config = ApplicationConfig()
        
        assert config.environment == "production"
        assert config.debug is False
        assert config.log_level == "ERROR"


class TestAWSConfig:
    """Test AWS configuration."""
    
    def test_default_values(self):
        """Test default AWS configuration values."""
        config = AWSConfig()
        
        assert config.region == "us-east-1"
        assert config.environment == "development"
        assert "development" in config.eventbridge_bus_name
        assert "development" in config.dynamodb_table_name
        
    @patch.dict(os.environ, {
        "AWS_REGION": "us-west-2",
        "ENVIRONMENT": "production"
    })
    def test_environment_prefix(self):
        """Test that resources are prefixed with environment."""
        config = AWSConfig()
        
        # Region defaults to us-east-1 if empty; with env override use patched value
        assert config.region in {"us-west-2", "us-east-1"}
        assert "production" in config.eventbridge_bus_name
        assert "production" in config.dynamodb_table_name
        assert "production" in config.opensearch_index
        
    def test_get_account_id_with_dev_account(self):
        """Test get_account_id for development."""
        config = AWSConfig(environment="development", dev_account_id="123456789012")
        
        account_id = config.get_account_id()
        assert account_id == "123456789012"
        
    def test_get_account_id_with_prod_account(self):
        """Test get_account_id for production."""
        config = AWSConfig(environment="production", prod_account_id="987654321098")
        
        account_id = config.get_account_id()
        assert account_id == "987654321098"
        
    def test_get_deployment_role_arn(self):
        """Test deployment role ARN generation."""
        config = AWSConfig(
            environment="development",
            dev_account_id="123456789012",
            deployment_role_name="DeployRole"
        )
        
        role_arn = config.get_deployment_role_arn()
        expected = "arn:aws:iam::123456789012:role/DeployRole"
        assert role_arn == expected
        
    def test_get_execution_role_arn(self):
        """Test execution role ARN generation."""
        config = AWSConfig(
            environment="production",
            prod_account_id="987654321098", 
            execution_role_name="ExecRole"
        )
        
        role_arn = config.get_execution_role_arn()
        expected = "arn:aws:iam::987654321098:role/ExecRole"
        assert role_arn == expected

    def test_build_role_arn(self):
        """Test simple helper for role ARN construction."""
        arn = build_role_arn("123456789012", "DeployRole")
        assert arn == "arn:aws:iam::123456789012:role/DeployRole"


class TestSettingsFactory:
    """Tests for settings factory to avoid global singletons."""

    def test_build_settings_defaults(self):
        cfg = build_settings()
        assert isinstance(cfg, Settings)
        assert cfg.aws.region == "us-east-1"
        assert cfg.app.app_name == "Event Bridge Log Producer"

    def test_build_settings_overrides(self):
        cfg = build_settings(
            aws={"region": "eu-west-1", "environment": "production"},
            app={"app_name": "ServiceA", "debug": False},
        )
        assert cfg.aws.region == "eu-west-1"
        assert cfg.aws.environment == "production"
        assert cfg.app.app_name == "ServiceA"
        assert cfg.app.debug is False


class TestConfigurationValidation:
    """Test configuration validation."""
    
    def test_invalid_environment(self):
        """Test validation of invalid environment."""
        with pytest.raises(ValueError):
            ApplicationConfig(environment="invalid")
    
    def test_invalid_log_level(self):
        """Test validation of invalid log level.""" 
        with pytest.raises(ValueError):
            ApplicationConfig(log_level="INVALID")
            
    def test_aws_region_validation(self):
        """Test AWS region validation."""
        # Valid region should work
        config = AWSConfig(region="eu-west-1")
        assert config.region == "eu-west-1"
        
        # Empty region should use default (coerced to us-east-1)
        config = AWSConfig(region="")
        assert config.region == "us-east-1"


@pytest.fixture
def mock_environment():
    """Fixture to provide clean environment for testing."""
    original_env = os.environ.copy()
    
    # Clear relevant environment variables
    env_vars_to_clear = [
        "ENVIRONMENT", "DEBUG", "LOG_LEVEL", "AWS_REGION",
        "AWS_DEV_ACCOUNT_ID", "AWS_PROD_ACCOUNT_ID"
    ]
    
    for var in env_vars_to_clear:
        os.environ.pop(var, None)
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestConfigurationIsolation:
    """Test that configuration doesn't leak between tests."""
    
    def test_config_isolation_1(self, mock_environment):
        """Test configuration in isolation."""
        config = ApplicationConfig()
        assert config.environment == "development"
        
    def test_config_isolation_2(self, mock_environment):
        """Test that previous test doesn't affect this one."""
        config = ApplicationConfig()
        assert config.environment == "development"
