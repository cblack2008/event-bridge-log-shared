"""
Configuration utilities intended to be service-agnostic.

This module defines lightweight, validated configuration models and
helpers that can be reused across services. It intentionally avoids
creating AWS SDK sessions/clients or binding to environment variables
at import time. Each service should construct its own runtime clients
and own its environment variable mapping.
"""

from typing import Optional, Dict, Any
from pydantic import Field, validator
try:
    # Pydantic v2
    from pydantic import field_validator  # type: ignore
except Exception:  # pragma: no cover
    field_validator = None  # type: ignore
from pydantic_settings import BaseSettings


class AWSConfig(BaseSettings):
    """AWS-specific configuration settings with multi-account support."""
    
    # Environment-specific settings
    environment: str = Field(default="development", env="ENVIRONMENT")
    region: str = Field(default="us-east-1", env="AWS_REGION")
    
    # Multi-account configuration
    dev_account_id: Optional[str] = Field(default=None, env="AWS_DEV_ACCOUNT_ID")
    prod_account_id: Optional[str] = Field(default=None, env="AWS_PROD_ACCOUNT_ID")
    
    # Role-based access (recommended for prod)
    deployment_role_name: str = Field(default="EventBridgeLogDeploymentRole", env="AWS_DEPLOYMENT_ROLE_NAME")
    execution_role_name: str = Field(default="EventBridgeLogExecutionRole", env="AWS_EXECUTION_ROLE_NAME")
    
    # AWS Profile support (for local development)
    profile: Optional[str] = Field(default=None, env="AWS_PROFILE")
    
    # Legacy credential support (discouraged for prod)
    access_key_id: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    secret_access_key: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    session_token: Optional[str] = Field(default=None, env="AWS_SESSION_TOKEN")
    
    # Resource naming with environment prefix
    eventbridge_bus_name: str = Field(default="event-bridge-log-bus", env="EVENTBRIDGE_BUS_NAME")
    eventbridge_source: str = Field(default="ecommerce.platform", env="EVENTBRIDGE_SOURCE")
    dynamodb_table_name: str = Field(default="event-bridge-log-events", env="DYNAMODB_TABLE_NAME")
    opensearch_endpoint: Optional[str] = Field(default=None, env="OPENSEARCH_ENDPOINT")
    opensearch_index: str = Field(default="events", env="OPENSEARCH_INDEX")
    
    @validator('eventbridge_bus_name', 'dynamodb_table_name', 'opensearch_index')
    def add_environment_prefix(cls, v, values):
        """Add environment prefix to resource names for isolation."""
        environment = values.get('environment', 'development')
        if not v.startswith(f"{environment}-"):
            return f"{environment}-{v}"
        return v

    # Backward-compatible validators for common fields
    @validator('region', pre=True, always=True)
    def coalesce_region(cls, v):  # type: ignore
        if not v:
            return 'us-east-1'
        return v

    @validator('environment', pre=True, always=True)
    def normalize_environment(cls, v):  # type: ignore
        val = (v or 'development').lower()
        if val not in {'development', 'production'}:
            return 'development'
        return val
    
    def get_account_id(self) -> Optional[str]:
        """Get the account ID for the current environment."""
        if self.environment == "production":
            return self.prod_account_id
        else:
            return self.dev_account_id
    
    def get_deployment_role_arn(self) -> Optional[str]:
        """Get the deployment role ARN for cross-account access."""
        account_id = self.get_account_id()
        if account_id:
            return f"arn:aws:iam::{account_id}:role/{self.deployment_role_name}"
        return None
    
    def get_execution_role_arn(self) -> Optional[str]:
        """Get the execution role ARN for Lambda functions."""
        account_id = self.get_account_id()
        if account_id:
            return f"arn:aws:iam::{account_id}:role/{self.execution_role_name}"
        return None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class ApplicationConfig(BaseSettings):
    """Application-level configuration settings."""
    
    app_name: str = Field(default="Event Bridge Log Producer", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json or text
    
    # Producer settings
    batch_size: int = Field(default=10, env="PRODUCER_BATCH_SIZE")
    max_retries: int = Field(default=3, env="PRODUCER_MAX_RETRIES")
    retry_delay_seconds: float = Field(default=1.0, env="PRODUCER_RETRY_DELAY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator('environment', pre=True, always=True)
    def validate_environment(cls, v):  # type: ignore
        val = (v or 'development').lower()
        if val not in {'development', 'production'}:
            raise ValueError('environment must be development or production')
        return val

    @validator('log_level', pre=True, always=True)
    def validate_log_level(cls, v):  # type: ignore
        allowed = {'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'critical', 'error', 'warning', 'info', 'debug'}
        if v not in allowed:
            raise ValueError('invalid log level')
        return v


class Settings(BaseSettings):
    """Main settings class combining all configuration sections."""
    
    aws: AWSConfig = AWSConfig()
    app: ApplicationConfig = ApplicationConfig()
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def build_role_arn(account_id: str, role_name: str) -> str:
    """Build an IAM Role ARN for the provided account and role name."""
    return f"arn:aws:iam::{account_id}:role/{role_name}"


def build_settings(*, aws: Optional[Dict[str, Any]] = None, app: Optional[Dict[str, Any]] = None) -> "Settings":
    """Create a Settings instance without relying on process env.

    Services should call this factory and pass only the values they own.
    Any omitted values fall back to sane defaults.
    """
    aws_cfg = AWSConfig(**(aws or {}))
    app_cfg = ApplicationConfig(**(app or {}))
    return Settings(aws=aws_cfg, app=app_cfg)
