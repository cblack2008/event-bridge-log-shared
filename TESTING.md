# Testing Guide

This document explains how to run and contribute tests for the Event Bridge Log Shared package.

## 🧪 **Quick Start**

### **Run All Tests**
```bash
# Install development dependencies
uv sync --extra dev

# Run tests with coverage
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_event_models.py -v
```

### **Coverage Reports**
```bash
# Generate HTML coverage report
uv run pytest --cov=src/event_bridge_log_shared --cov-report=html

# View coverage report
open htmlcov/index.html

# Generate XML coverage for CI
uv run pytest --cov=src/event_bridge_log_shared --cov-report=xml
```

## 📋 **Testing Commands Reference**

| Command | Purpose |
|---------|---------|
| `uv run pytest` | Run all tests with coverage |
| `uv run pytest -v` | Verbose test output |
| `uv run pytest -x` | Stop on first failure |
| `uv run pytest -k "test_user"` | Run tests matching pattern |
| `uv run pytest tests/test_config.py::TestAWSConfig` | Run specific test class |
| `uv run pytest --lf` | Run only last failed tests |
| `uv run pytest --tb=short` | Shorter traceback format |

## 🔍 **Code Quality**

### **Linting**
```bash
# Check code style
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check src/ tests/ --fix

# Format code
uv run black src/ tests/

# Type checking
uv run mypy src/
```

### **All Quality Checks**
```bash
# Run all quality checks (same as CI)
uv run ruff check src/ tests/
uv run black --check src/ tests/
uv run mypy src/
uv run pytest --cov=src/event_bridge_log_shared
```

## 📂 **Test Structure**

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_config.py           # Configuration management tests
├── test_event_models.py     # Event model tests
└── test_example_coverage.py # Basic coverage example
```

### **Test Categories**

#### **1. Event Model Tests** (`test_event_models.py`)
- ✅ Event creation and validation
- ✅ Serialization/deserialization
- ✅ Type checking for all event types
- ✅ Parameterized tests for multiple event types

#### **2. Configuration Tests** (`test_config.py`)
- ✅ AWS configuration with different environments
- ✅ Environment variable override behavior
- ✅ Role ARN generation
- ✅ Session creation (mocked)
- ✅ Configuration validation

#### **3. Integration Tests** (Future)
- ⏳ End-to-end event processing
- ⏳ AWS service integration (with mocking)

## 🎯 **Writing Tests**

### **Test Naming Convention**
```python
def test_function_name_condition():
    """Test that function behaves correctly under condition."""
    pass

class TestClassName:
    """Test suite for ClassName."""

    def test_method_name_behavior(self):
        """Test specific behavior of method."""
        pass
```

### **Using Fixtures**
```python
def test_user_event_creation(sample_user_data):
    """Test user event creation with sample data."""
    event = UserRegistered(**sample_user_data)
    assert event.user_id == sample_user_data["user_id"]
```

### **Testing Event Models**
```python
def test_event_serialization():
    """Test event serialization."""
    event = UserRegistered(
        user_id="user123",
        email="test@example.com",
        username="testuser"
    )

    # Test dict conversion
    event_dict = event.model_dump()
    assert isinstance(event_dict, dict)

    # Test round-trip
    recreated = UserRegistered.model_validate(event_dict)
    assert recreated.user_id == event.user_id
```

### **Testing Configuration**
```python
@patch.dict(os.environ, {"ENVIRONMENT": "production"})
def test_production_config():
    """Test production configuration."""
    config = ApplicationConfig()
    assert config.environment == "production"
```

## 🎛️ **Environment Setup**

### **Test Environment Variables**
Tests use isolated environments to avoid conflicts:

```python
@pytest.fixture
def clean_environment():
    """Provides clean environment for testing."""
    # Clears all relevant env vars
    # Restores after test
```

### **Mocking AWS Services**
```python
@patch('boto3.Session')
def test_aws_functionality(mock_session):
    """Test AWS functionality with mocking."""
    # Mock AWS calls to avoid real API calls
    pass
```

## 📊 **Coverage Requirements**

- **Minimum Coverage**: 85%
- **Current Coverage**: ~88%
- **Branch Coverage**: Enabled
- **Missing Coverage**: Mainly in AWS integration code

### **Coverage Exclusions**
```python
# Lines excluded from coverage:
if __name__ == "__main__":  # pragma: no cover
    pass

def __repr__(self):  # Automatically excluded
    return f"..."
```

## 🚀 **Continuous Integration**

### **GitHub Actions**
Our CI pipeline runs:
1. **Python 3.11 & 3.12** matrix testing
2. **Code quality** checks (ruff, black, mypy)
3. **Test suite** with coverage reporting
4. **Coverage upload** to Codecov

### **Local CI Simulation**
```bash
# Simulate CI environment locally
./setup-standalone.sh
```

## 🐛 **Debugging Tests**

### **Common Issues**

#### **Import Errors**
```bash
# Ensure package is installed in development mode
uv sync --extra dev

# Check package installation
uv run python -c "import event_bridge_log_shared; print('OK')"
```

#### **Pydantic Warnings**
```bash
# Run tests with warnings as errors to catch issues
uv run pytest -W error::DeprecationWarning
```

#### **Coverage Gaps**
```bash
# Find uncovered lines
uv run pytest --cov=src/event_bridge_log_shared --cov-report=term-missing

# Generate detailed HTML report
uv run pytest --cov=src/event_bridge_log_shared --cov-report=html
open htmlcov/index.html
```

## 📈 **Test Performance**

### **Current Metrics**
- **Test Count**: ~25 tests
- **Execution Time**: ~1-2 seconds
- **Coverage**: 88%+
- **Success Rate**: 100%

### **Performance Tips**
```bash
# Run tests in parallel (if needed later)
uv add pytest-xdist[dev]
uv run pytest -n auto

# Profile slow tests
uv run pytest --durations=10
```

## 🤝 **Contributing Tests**

### **Test Requirements**
1. **All new code** must have tests
2. **Coverage** must remain above 85%
3. **No warnings** in test output
4. **Fast execution** (< 5 seconds total)

### **Test Review Checklist**
- [ ] Tests cover happy path and edge cases
- [ ] Tests use appropriate fixtures
- [ ] Tests are isolated (no side effects)
- [ ] Test names are descriptive
- [ ] Docstrings explain test purpose
- [ ] No hardcoded values (use fixtures)

## 🎯 **Future Testing Goals**

### **Short Term**
- [ ] Increase coverage to 95%
- [ ] Add integration tests for AWS services
- [ ] Add performance/load tests
- [ ] Add property-based testing with Hypothesis

### **Long Term**
- [ ] Mutation testing with mutmut
- [ ] Contract testing for API compatibility
- [ ] Benchmarking suite
- [ ] Automated test generation

---

## 📞 **Help & Support**

If you encounter testing issues:

1. **Check this guide** for common solutions
2. **Run the setup script**: `./setup-standalone.sh`
3. **Check CI logs** on GitHub Actions
4. **Open an issue** with test output and environment details

Happy testing! 🧪✨
