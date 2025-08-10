"""
Event models package for the Event Bridge Log Analytics Platform.

This package contains all event models organized by domain:
- user: User authentication and profile events
- ecommerce: Shopping cart and order events  
- inventory: Stock management events
- payment: Financial transaction events
- analytics: User behavior and analytics events
"""

from .base import EventType, BaseEvent

from .user import (
    UserRegisteredEvent,
    UserLoginEvent,
    UserLogoutEvent,
    UserProfileUpdatedEvent,
    UserDeletedEvent,
)

from .ecommerce import (
    ProductViewedEvent,
    ProductSearchedEvent,
    CartItemAddedEvent,
    CartItemRemovedEvent,
    CartAbandonedEvent,
    OrderCreatedEvent,
    OrderPaidEvent,
    OrderShippedEvent,
    OrderDeliveredEvent,
)

from .inventory import (
    InventoryLowStockEvent,
    InventoryOutOfStockEvent,
    InventoryRestockedEvent,
)

from .payment import (
    PaymentProcessedEvent,
    PaymentFailedEvent,
    PaymentRefundedEvent,
)

from .analytics import (
    ReviewSubmittedEvent,
    UserSessionEvent,
    PageViewEvent,
)

# Event Union Type for type hints (compatible with Python 3.9+)
from typing import Union

EventModel = Union[
    # User events
    UserRegisteredEvent, UserLoginEvent, UserLogoutEvent, UserProfileUpdatedEvent, UserDeletedEvent,
    
    # E-commerce events
    ProductViewedEvent, ProductSearchedEvent,
    CartItemAddedEvent, CartItemRemovedEvent, CartAbandonedEvent,
    OrderCreatedEvent, OrderPaidEvent, OrderShippedEvent, OrderDeliveredEvent,
    
    # Inventory events
    InventoryLowStockEvent, InventoryOutOfStockEvent, InventoryRestockedEvent,
    
    # Payment events
    PaymentProcessedEvent, PaymentFailedEvent, PaymentRefundedEvent,
    
    # Analytics events
    ReviewSubmittedEvent, UserSessionEvent, PageViewEvent,
]

__all__ = [
    # Base classes
    "EventType", "BaseEvent",
    
    # User events
    "UserRegisteredEvent", "UserLoginEvent", "UserLogoutEvent", "UserProfileUpdatedEvent", "UserDeletedEvent",
    
    # E-commerce events
    "ProductViewedEvent", "ProductSearchedEvent",
    "CartItemAddedEvent", "CartItemRemovedEvent", "CartAbandonedEvent",
    "OrderCreatedEvent", "OrderPaidEvent", "OrderShippedEvent", "OrderDeliveredEvent",
    
    # Inventory events
    "InventoryLowStockEvent", "InventoryOutOfStockEvent", "InventoryRestockedEvent",
    
    # Payment events
    "PaymentProcessedEvent", "PaymentFailedEvent", "PaymentRefundedEvent",
    
    # Analytics events
    "ReviewSubmittedEvent", "UserSessionEvent", "PageViewEvent",
    
    # Union type
    "EventModel",
]
