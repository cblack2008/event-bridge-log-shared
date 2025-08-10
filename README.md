# Event Bridge Log Analytics - Shared Package

[![PyPI version](https://badge.fury.io/py/event-bridge-log-shared.svg)](https://badge.fury.io/py/event-bridge-log-shared)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive shared library for Event Bridge Log Analytics Platform, providing common models, utilities, and configurations for microservices.

## 🎯 **Purpose**

This package centralizes shared code used across multiple microservices in the Event Bridge Log Analytics Platform:

- **Event Models**: Pydantic models for all event types (user, payment, ecommerce, etc.)
- **Configuration Management**: Centralized AWS and application settings
- **Utilities**: Common functions for event processing and validation
- **Type Safety**: Full type hints and validation for enterprise reliability

## 📦 **Installation**

```bash
# From PyPI (recommended)
pip install event-bridge-log-shared

# From GitHub (latest)
pip install git+https://github.com/yourusername/event-bridge-log-shared.git

# For development
pip install event-bridge-log-shared[dev]
```

## 🚀 **Quick Start**

### **Event Models**

```python
from event_bridge_log_shared.models.events.user import UserRegisteredEvent
from event_bridge_log_shared.models.events.ecommerce import OrderCreatedEvent

# Create user registration event
user_event = UserRegisteredEvent(
    user_id="user123",
    email="user@example.com",
    username="newuser",
    registration_method="email",
    terms_accepted=True,
    source="user-service",
)

# Create order event
order_event = OrderCreatedEvent(
    user_id="user123",
    order_id="order456",
    order_number="ORD-123",
    order_total=99.99,
    order_status="created",
    items=[],
    item_count=0,
    customer_email="user@example.com",
    shipping_address={"street": "1 Main St"},
    billing_address={"street": "1 Main St"},
    payment_method="credit_card",
    shipping_method="standard",
    source="checkout-service",
)

# Events are automatically validated and timestamped
print(f"Event ID: {user_event.event_id}")
print(f"Timestamp: {user_event.timestamp}")
```

### **Configuration**

```python
from event_bridge_log_shared import build_settings

cfg = build_settings(
    aws={"environment": "development", "region": "us-east-1"},
    app={"app_name": "my-service", "debug": True},
)

print(cfg.aws.eventbridge_bus_name)
print(cfg.app.app_name)
```

### **All Available Events**

See modules under `event_bridge_log_shared.models.events` for complete class lists (e.g., `UserRegisteredEvent`, `OrderCreatedEvent`, `PaymentProcessedEvent`, `UserSessionEvent`, etc.).

## 🏗️ **Architecture**

### **Event Types**

All events extend `BaseEvent` and include:

- **Automatic ID generation**: UUID for each event
- **Timestamp**: ISO 8601 formatted creation time
- **Environment tracking**: Development/production context
- **Correlation support**: For distributed tracing
- **Metadata**: Extensible additional data

### **Configuration Management**

- **Environment-based**: Automatic dev/prod configuration
- **AWS Integration**: Native boto3 session management
- **Validation**: Pydantic-powered setting validation
- **Security**: No hardcoded credentials or endpoints

## 🔒 **Security**

- **Zero hardcoded secrets**: All sensitive data via environment variables
- **Role-based AWS access**: IAM roles with cross-account support
- **Input validation**: All data validated with Pydantic
- **Type safety**: Full type hints prevent runtime errors

## 🧪 **Development**

### **Setup**

```bash
git clone https://github.com/yourusername/event-bridge-log-shared.git
cd event-bridge-log-shared

# Developer setup (dependencies + pre-commit hooks)
make dev-setup

# Or manually
uv sync --extra dev
uv run pre-commit install
```

### **Testing**

```bash
# Run tests with coverage
make test

# Generate HTML coverage
make coverage-html

# Lint and type check
make lint

# Auto-format and fix lint
make format
```

### **Release Process**

1. Update version in `src/event_bridge_log_shared/__init__.py`
2. Update `CHANGELOG.md`
3. Create GitHub release
4. Automated CI/CD publishes to PyPI

## 📋 **Requirements**

- **Python**: 3.11 or higher
- **AWS SDK**: boto3 >= 1.40.0
- **Validation**: pydantic >= 2.11.0
- **Settings**: pydantic-settings >= 2.10.0

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure tests pass: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 **Related Projects**

- [Event Bridge Log Analytics](https://github.com/yourusername/event-bridge-log) - Main microservices platform
- [Documentation](https://yourusername.github.io/event-bridge-log-shared) - Complete API documentation

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/event-bridge-log-shared/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/event-bridge-log-shared/discussions)
- **Email**: your.email@example.com
