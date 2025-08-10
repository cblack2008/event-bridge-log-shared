"""
Event Bridge Log Analytics - Shared Package

A comprehensive shared library for Event Bridge Log Analytics Platform,
providing common models, utilities, and configurations for microservices.

This package contains:
- Event models (user, payment, ecommerce, inventory, analytics)
- Configuration management for AWS resources
- Utilities for event handling and processing
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main components for easy access
from .models.events import *
from .utils.config import (
    Settings,
    AWSConfig,
    ApplicationConfig,
    build_settings,
    build_role_arn,
)

__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__email__",
    
    # Configuration
    "Settings",
    "AWSConfig",
    "ApplicationConfig",
    "build_settings",
    "build_role_arn",
    
    # Event models are imported via * from models.events
    # This includes: BaseEvent, UserRegistered, UserLogin, OrderCreated, etc.
]

# Package metadata
PACKAGE_NAME = "event-bridge-log-shared"
DESCRIPTION = "Shared models and utilities for Event Bridge Log Analytics Platform"
LICENSE = "MIT"
HOMEPAGE = "https://github.com/yourusername/event-bridge-log-shared"