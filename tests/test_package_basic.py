"""
Basic functionality tests to ensure the package works.
"""
from datetime import datetime
from uuid import UUID

from event_bridge_log_shared.models.events.base import BaseEvent, EventType


class TestBasicFunctionality:
    """Test basic package functionality."""

    def test_base_event_creation(self):
        """Test basic event creation."""
        event = BaseEvent(event_type=EventType.USER_REGISTERED, source="test.source")

        assert event.event_type == EventType.USER_REGISTERED
        assert event.source == "test.source"
        assert isinstance(event.event_id, UUID)
        assert isinstance(event.timestamp, datetime)

    def test_base_event_serialization(self):
        """Test basic event serialization."""
        event = BaseEvent(event_type=EventType.ORDER_CREATED, source="test.api")

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

    def test_event_with_metadata(self):
        """Test event with metadata."""
        metadata = {"test_flag": True, "request_id": "req-123"}
        event = BaseEvent(event_type=EventType.USER_LOGIN, source="auth.service", metadata=metadata)

        assert event.metadata == metadata

    def test_event_correlation_id(self):
        """Test correlation ID functionality."""
        from uuid import uuid4

        correlation_id = str(uuid4())
        event = BaseEvent(
            event_type=EventType.USER_SESSION,
            source="analytics.service",
            correlation_id=correlation_id,
        )

        assert str(event.correlation_id) == correlation_id


class TestPackageImports:
    """Test that package imports work correctly."""

    def test_import_base_classes(self):
        """Test importing base classes."""
        from event_bridge_log_shared.models.events.base import BaseEvent, EventType

        assert BaseEvent is not None
        assert EventType is not None

    def test_import_user_events(self):
        """Test importing user event classes."""
        from event_bridge_log_shared.models.events.user import (
            UserLoginEvent,
            UserLogoutEvent,
            UserRegisteredEvent,
        )

        assert UserRegisteredEvent is not None
        assert UserLoginEvent is not None
        assert UserLogoutEvent is not None

    def test_import_helpers(self):
        """Test importing helper utilities."""
        from event_bridge_log_shared.utils import build_role_arn, normalize_env, prefix_name

        assert normalize_env("development") == "dev"
        assert normalize_env("prod") == "prod"
        assert prefix_name("dev", "events") == "dev-events"
        assert build_role_arn("123456789012", "Role") == "arn:aws:iam::123456789012:role/Role"

    def test_package_level_imports(self):
        """Test package-level imports work."""
        import event_bridge_log_shared

        # Should have version
        assert hasattr(event_bridge_log_shared, "__version__")
        assert event_bridge_log_shared.__version__ == "1.0.0"
