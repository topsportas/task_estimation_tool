#!/bin/bash

# Exit on error
set -e

# Clear previous coverage data
coverage erase

echo "Running pytest with coverage..."
pytest --cov=estimation_app --cov-report=term-missing -v tests/

# Generate HTML coverage report
coverage html
echo "HTML coverage report generated at htmlcov/index.html"