#!/bin/bash

# Event Bridge Log Analytics - Shared Package Setup Script
# This script prepares the standalone shared package for publishing

set -e

echo "🚀 Setting up Event Bridge Log Analytics Shared Package"
echo "======================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}1. Installing dependencies...${NC}"
if command -v uv &> /dev/null; then
    uv sync --extra dev
else
    pip install -e .[dev]
fi

echo -e "${YELLOW}2. Running code quality checks...${NC}"
echo "   - Formatting with black..."
black src/ tests/

echo "   - Linting with ruff..."
ruff check src/ tests/ --fix

echo "   - Type checking with mypy..."
mypy src/

echo -e "${YELLOW}3. Running tests with coverage...${NC}"
pytest --cov=src/event_bridge_log_shared --cov-report=html --cov-report=term-missing

echo -e "${YELLOW}4. Building package...${NC}"
if command -v uv &> /dev/null; then
    uv build
else
    python -m build
fi

echo -e "${YELLOW}5. Checking built package...${NC}"
python -m twine check dist/*

echo -e "${GREEN}✅ Package ready for publishing!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Create a new GitHub repository: event-bridge-log-shared"
echo "2. Push this code to the repository"
echo "3. Create a release on GitHub to trigger automatic PyPI publishing"
echo "4. Update your microservices to use: pip install event-bridge-log-shared"
echo ""
echo -e "${BLUE}Local testing:${NC}"
echo "pip install -e ."
echo "python -c 'from event_bridge_log_shared import UserRegistered; print(\"✅ Import works!\")'"
