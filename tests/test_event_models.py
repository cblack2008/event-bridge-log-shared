"""
Test suite for event models.
"""
import pytest
from datetime import datetime
from uuid import UUID

from event_bridge_log_shared.models.events.base import BaseEvent, EventType
from event_bridge_log_shared.models.events.user import UserRegisteredEvent, UserLoginEvent
from event_bridge_log_shared.models.events.ecommerce import OrderCreatedEvent, ProductViewedEvent
from event_bridge_log_shared.models.events.payment import PaymentProcessedEvent
from event_bridge_log_shared.models.events.analytics import UserSessionEvent


class TestBaseEvent:
    """Test BaseEvent functionality."""
    
    def test_base_event_creation(self):
        """Test basic event creation."""
        event = BaseEvent(
            event_type=EventType.USER_REGISTERED,
            source="test.source"
        )
        
        assert event.event_type == EventType.USER_REGISTERED
        assert event.source == "test.source"
        assert isinstance(event.event_id, UUID)
        assert isinstance(event.timestamp, datetime)
        assert event.environment in ["development", "production"]
        
    def test_base_event_serialization(self):
        """Test event serialization."""
        event = BaseEvent(
            event_type=EventType.ORDER_CREATED,
            source="test.api"
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert isinstance(event_dict, dict)
        assert event_dict["event_type"] == "order.created"
        assert "event_id" in event_dict
        assert "timestamp" in event_dict
        
        # Test JSON conversion
        event_json = event.model_dump_json()
        assert isinstance(event_json, str)
        assert "order.created" in event_json
        
    def test_base_event_with_metadata(self):
        """Test event with metadata."""
        metadata = {"test_flag": True, "request_id": "req-123"}
        event = BaseEvent(
            event_type=EventType.USER_LOGIN,
            source="auth.service",
            metadata=metadata
        )
        
        assert event.metadata == metadata
        
    def test_base_event_correlation_id(self):
        """Test correlation ID functionality."""
        from uuid import uuid4
        correlation_id = str(uuid4())
        event = BaseEvent(
            event_type=EventType.USER_SESSION,
            source="analytics.service",
            correlation_id=correlation_id
        )
        
        assert str(event.correlation_id) == correlation_id


class TestUserEvents:
    """Test user-related events."""
    
    def test_user_registered_event(self):
        """Test UserRegistered event."""
        event = UserRegisteredEvent(
            user_id="user123",
            email="test@example.com",
            username="testuser",
            source="test.api",
            registration_method="email",
            terms_accepted=True
        )
        
        assert event.event_type == EventType.USER_REGISTERED
        assert event.user_id == "user123"
        assert event.email == "test@example.com"
        assert event.username == "testuser"
        
    def test_user_login_event(self):
        """Test UserLogin event."""
        event = UserLoginEvent(
            user_id="user123",
            session_id="sess123",
            source="test.api",
            login_method="password",
            login_successful=True
        )
        
        assert event.event_type == EventType.USER_LOGIN
        assert event.user_id == "user123"
        assert event.session_id == "sess123"
        
    def test_user_registered_validation(self):
        """Test UserRegistered validation."""
        # Minimal valid payload should not raise
        evt = UserRegisteredEvent(
            user_id="user123",
            email="test@example.com",
            username="testuser",
            source="test.api",
            registration_method="email",
            terms_accepted=True
        )
        assert evt.email.endswith("@example.com")


class TestEcommerceEvents:
    """Test ecommerce-related events."""
    
    def test_order_created_event(self):
        """Test OrderCreated event."""
        event = OrderCreatedEvent(
            user_id="user123",
            order_id="order456",
            source="checkout.service",
            order_number="ORD-456",
            order_total=99.99,
            order_status="created",
            items=[],
            item_count=0,
            customer_email="test@example.com",
            shipping_address={"line1": "123 Test St", "city": "Testville"},
            billing_address={"line1": "123 Test St", "city": "Testville"},
            payment_method="credit_card",
            shipping_method="standard"
        )
        
        assert event.event_type == EventType.ORDER_CREATED
        assert event.user_id == "user123"
        assert event.order_id == "order456"
        assert float(event.order_total) == 99.99
        
    def test_product_viewed_event(self):
        """Test ProductViewed event."""
        event = ProductViewedEvent(
            user_id="user123",
            product_id="prod789",
            product_name="Test Product",
            product_category="electronics",
            product_price=29.99,
            is_authenticated=True,
            source="web"
        )
        
        assert event.event_type == EventType.PRODUCT_VIEWED
        assert event.user_id == "user123"
        assert event.product_id == "prod789"
        assert event.product_name == "Test Product"
        assert event.product_category == "electronics"
        assert float(event.product_price) == 29.99


class TestPaymentEvents:
    """Test payment-related events."""
    
    def test_payment_processed_event(self):
        """Test PaymentProcessed event."""
        event = PaymentProcessedEvent(
            user_id="user123",
            order_id="order456",
            payment_id="pay789",
            transaction_id="txn_1",
            payment_amount=99.99,
            payment_currency="USD",
            processor="stripe",
            processing_time_ms=120,
            order_number="ORD-456",
            customer_id="user123",
            customer_email="test@example.com",
            payment_method="credit_card",
            source="payments.service"
        )
        
        assert event.event_type == EventType.PAYMENT_PROCESSED
        assert event.user_id == "user123"
        assert event.order_id == "order456"
        assert event.payment_id == "pay789"
        assert event.amount == 99.99
        assert event.currency == "USD"
        assert event.payment_method == "credit_card"


class TestAnalyticsEvents:
    """Test analytics-related events."""
    
    def test_user_session_event(self):
        """Test UserSession event."""
        from datetime import datetime
        event = UserSessionEvent(
            user_id="user123",
            session_id="sess456",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0...",
            session_start=datetime.utcnow(),
            device_type="desktop",
            browser="Chrome",
            operating_system="macOS",
            source="web"
        )
        
        assert event.event_type == EventType.USER_SESSION
        assert event.user_id == "user123"
        assert event.session_id == "sess456"
        assert event.ip_address == "192.168.1.1"
        assert event.user_agent == "Mozilla/5.0..."
        assert event.duration_seconds == 300


class TestEventSerialization:
    """Test event serialization across all types."""
    
    @pytest.mark.parametrize("event_class,event_data", [
        (UserRegisteredEvent, {
            "user_id": "user123",
            "email": "test@example.com", 
            "username": "testuser",
            "source": "test.api",
            "registration_method": "email",
            "terms_accepted": True
        }),
        (OrderCreatedEvent, {
            "user_id": "user123",
            "order_id": "order456",
            "source": "checkout.service",
            "order_number": "ORD-456",
            "order_total": 99.99,
            "order_status": "created",
            "items": [],
            "item_count": 0,
            "customer_email": "test@example.com",
            "shipping_address": {"line1": "123 Test St"},
            "billing_address": {"line1": "123 Test St"},
            "payment_method": "credit_card",
            "shipping_method": "standard"
        }),
        (PaymentProcessedEvent, {
            "user_id": "user123",
            "order_id": "order456", 
            "payment_id": "pay789",
            "payment_amount": 99.99,
            "payment_currency": "USD",
            "transaction_id": "txn_1",
            "processor": "stripe",
            "processing_time_ms": 120,
            "order_number": "ORD-456",
            "customer_id": "user123",
            "customer_email": "test@example.com",
            "payment_method": "credit_card",
            "source": "payments.service"
        })
    ])
    def test_event_round_trip_serialization(self, event_class, event_data):
        """Test that events can be serialized and deserialized."""
        # Create event
        original_event = event_class(**event_data)
        
        # Serialize to dict
        event_dict = original_event.model_dump()
        
        # Deserialize back
        recreated_event = event_class.model_validate(event_dict)
        
        # Should be equivalent
        assert recreated_event.event_type == original_event.event_type
        assert recreated_event.event_id == original_event.event_id
        assert recreated_event.timestamp == original_event.timestamp
        
        # Test specific fields
        from decimal import Decimal
        for field_name, expected_value in event_data.items():
            actual = getattr(recreated_event, field_name)
            if isinstance(actual, Decimal) and isinstance(expected_value, (int, float)):
                assert float(actual) == expected_value
            else:
                assert actual == expected_value
