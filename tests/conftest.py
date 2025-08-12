"""
Shared test fixtures and configuration.
"""

import pytest


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "user_id": "user-12345",
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def sample_order_data():
    """Sample order data aligned with OrderCreatedEvent model."""
    return {
        "user_id": "user-12345",
        "order_id": "order-67890",
        "order_number": "ORD-67890",
        "order_total": 149.99,
        "order_status": "created",
        "items": [],
        "item_count": 0,
        "customer_email": "test@example.com",
        "shipping_address": {"street": "1 Main St"},
        "billing_address": {"street": "1 Main St"},
        "payment_method": "credit_card",
        "shipping_method": "standard",
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data aligned with PaymentProcessedEvent model."""
    return {
        "user_id": "user-12345",
        "order_id": "order-67890",
        "order_number": "ORD-67890",
        "payment_id": "pay-abcdef",
        "payment_method": "credit_card",
        "payment_amount": 149.99,
        "payment_currency": "USD",
        "transaction_id": "txn-123",
        "processor": "stripe",
        "processing_time_ms": 120,
        "customer_id": "user-12345",
        "customer_email": "test@example.com",
    }
