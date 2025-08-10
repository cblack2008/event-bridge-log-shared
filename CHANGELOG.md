# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-08-10

### Added
- Initial release of Event Bridge Log Analytics Shared Package
- Complete event model library with Pydantic validation
- AWS configuration management with cross-account support
- Event types for user, ecommerce, payment, inventory, and analytics domains
- Comprehensive test suite with 85%+ coverage
- Type safety with full mypy support
- Professional packaging with proper metadata

### Event Models
- `BaseEvent` - Foundation class for all events
- `UserRegistered`, `UserLogin`, `UserLogout`, `UserProfileUpdated`, `UserDeleted`
- `ProductViewed`, `ProductSearched`, `CartItemAdded`, `CartItemRemoved`, `CartAbandoned`
- `OrderCreated`, `OrderPaid`, `OrderShipped`, `OrderDelivered`
- `PaymentProcessed`, `PaymentFailed`, `PaymentRefunded`
- `InventoryLowStock`, `InventoryOutOfStock`, `InventoryRestocked`
- `UserSession`, `PageView`, `ReviewSubmitted`

### Configuration
- Environment-based configuration (development/production)
- AWS resource management with IAM role support
- Cross-account deployment capabilities
- Secure credential handling (zero hardcoded secrets)

### Development Tools
- Black code formatting
- Ruff linting
- MyPy type checking
- Pytest with coverage reporting
- GitHub Actions CI/CD pipeline

### Documentation
- Comprehensive README with examples
- Type hints for all public APIs
- Docstrings for all classes and methods
- Usage examples for each event type

[Unreleased]: https://github.com/yourusername/event-bridge-log-shared/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/event-bridge-log-shared/releases/tag/v1.0.0
