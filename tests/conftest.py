"""
Shared test fixtures and configuration.
"""
import pytest
import os
from unittest.mock import patch


@pytest.fixture
def clean_environment():
    """Fixture that provides a clean environment for tests."""
    original_env = os.environ.copy()
    
    # Clear AWS and app-related environment variables
    env_vars_to_clear = [
        "ENVIRONMENT", "DEBUG", "LOG_LEVEL", 
        "AWS_REGION", "AWS_PROFILE",
        "AWS_DEV_ACCOUNT_ID", "AWS_PROD_ACCOUNT_ID",
        "EVENTBRIDGE_BUS_NAME", "DYNAMODB_TABLE_NAME", "OPENSEARCH_INDEX"
    ]
    
    for var in env_vars_to_clear:
        os.environ.pop(var, None)
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "user_id": "user-12345",
        "email": "test@example.com", 
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def sample_order_data():
    """Sample order data for testing."""
    return {
        "user_id": "user-12345",
        "order_id": "order-67890",
        "total_amount": 149.99,
        "currency": "USD",
        "items": [
            {"product_id": "prod-1", "quantity": 2, "price": 49.99},
            {"product_id": "prod-2", "quantity": 1, "price": 49.99}
        ]
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for testing."""
    return {
        "user_id": "user-12345",
        "order_id": "order-67890",
        "payment_id": "pay-abcdef",
        "amount": 149.99,
        "currency": "USD",
        "payment_method": "credit_card"
    }


@pytest.fixture
def mock_aws_session():
    """Mock AWS session for testing."""
    with patch('boto3.Session') as mock_session:
        mock_instance = mock_session.return_value
        mock_instance.region_name = "us-east-1"
        yield mock_instance
