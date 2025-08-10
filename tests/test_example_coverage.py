"""
Example test file to demonstrate coverage configuration.
This ensures we have at least one test that will run.
"""
import pytest
from event_bridge_log_shared.models.events.base import BaseEvent
from datetime import datetime
from uuid import uuid4


def test_base_event_creation():
    """Test that we can create a base event."""
    event = BaseEvent(
        event_type="user.registered",
        source="test.source"
    )
    assert event is not None
    assert event.event_type == "user.registered"
    assert event.source == "test.source"


def test_base_event_validation():
    """Test event validation."""
    event = BaseEvent(
        event_type="user.login",
        source="test.source"
    )
    assert event.event_id is not None
    assert event.timestamp is not None
    assert event.environment is not None


def test_base_event_serialization():
    """Test event can be serialized."""
    event = BaseEvent(
        event_type="order.created",
        source="test.source"
    )
    
    # Test dict conversion
    event_dict = event.model_dump()
    assert isinstance(event_dict, dict)
    assert event_dict["event_type"] == "order.created"
    
    # Test JSON conversion
    event_json = event.model_dump_json()
    assert isinstance(event_json, str)


class TestCoverageExample:
    """Example test class to demonstrate coverage patterns."""
    
    def test_class_method(self):
        """Test from within a class."""
        assert True
    
    def test_with_setup(self):
        """Test with setup pattern."""
        # Setup
        test_data = {"key": "value"}
        
        # Test
        result = test_data.get("key")
        
        # Assert
        assert result == "value"
