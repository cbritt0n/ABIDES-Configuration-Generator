# ABIDES Configuration Generator v1.0.0 - Development Makefile

.PHONY: help install test lint format clean run example docker templates validate info

# Default target
help:
	@echo "🎯 ABIDES Configuration Generator v1.0.0 - Available Commands:"
	@echo ""
	@echo "📦 Installation & Setup:"
	@echo "  install     Install dependencies (none required - uses stdlib only)"
	@echo "  install-dev Install development dependencies" 
	@echo ""
	@echo "🚀 Usage:"
	@echo "  run         Run CLI with example parameters"
	@echo "  templates   List all available research templates"
	@echo "  example     Generate example configuration using RMSC03 template"
	@echo "  gym-example Generate ABIDES-Gym compatible configuration"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  test        Run comprehensive tests"
	@echo "  test-all    Run all test suites (agents, gym, comprehensive)"
	@echo "  lint        Run syntax validation"
	@echo "  validate    Validate generated configurations"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  docker      Build Docker image"
	@echo "  docker-run  Run in Docker container"
	@echo "  docker-templates List templates in Docker"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  clean       Remove generated files"
	@echo "  clean-all   Remove all build artifacts"
	@echo ""
	@echo "ℹ️  Information:"
	@echo "  info        Show project information"

# Installation (zero dependencies - stdlib only)
install:
	@echo "📦 Installing dependencies..."
	@echo "✅ No external dependencies required - uses Python standard library only!"
	@echo "   All functionality available out of the box."

install-dev:
	@echo "📦 Installing development dependencies..."
	@echo "✅ No dependencies required for this project"
	@echo "   For optional linting: pip install black flake8 mypy"

# Usage examples
run:
	@echo "🚀 Running CLI example with multiple agent types..."
	python configgen.py -f example_market --mm 5 --zi 100 --no 20 --va 10 --mo 5 --am 3 --verbose

templates:
	@echo "� Listing all available research templates..."
	python configgen.py --list-templates

example:
	@echo "📊 Generating RMSC03 research template example..."
	python configgen.py \
		--template rmsc03 \
		-f rmsc03_example \
		--symbol AAPL \
		--verbose

gym-example:
	@echo "🏋️  Generating ABIDES-Gym compatible configuration..."
	python configgen.py \
		--template minimal \
		-f gym_ready_config \
		--gym-mode \
		--mm 3 \
		--zi 50 \
		--verbose

# Testing and quality
test:
	@echo "🧪 Running comprehensive test suite..."
	python comprehensive_test.py

test-all:
	@echo "🧪 Running all test suites..."
	@echo "Testing all agent types..."
	python all_agents_test.py
	@echo "Testing ABIDES-Gym integration..."
	python gym_test.py  
	@echo "Testing comprehensive functionality..."
	python comprehensive_test.py

lint:
	@echo "🔍 Running syntax validation..."
	python -m py_compile configgen.py
	@echo "✅ Syntax validation passed!"

validate:
	@echo "✅ Validating all research templates..."
	@echo "Testing RMSC03 template..."
	python configgen.py --template rmsc03 -f validation_rmsc03 --quiet
	@echo "Testing RMSC04 template..."
	python configgen.py --template rmsc04 -f validation_rmsc04 --quiet
	@echo "Testing HFT template..."
	python configgen.py --template hft -f validation_hft --quiet
	@echo "Testing Behavioral template..."
	python configgen.py --template behavioral -f validation_behavioral --quiet
	@echo "Testing Minimal template..."
	python configgen.py --template minimal -f validation_minimal --quiet
	@echo "✅ All templates validated successfully!"

# Docker
docker:
	@echo "🐳 Building Docker image..."
	docker build -t abides-configgen:v1.0.0 .

docker-run:
	@echo "🐳 Running example in Docker..."
	docker run --rm -v $(PWD)/output:/app/output \
		abides-configgen:v1.0.0 \
		--template rmsc03 -f docker_example -o /app/output

docker-templates:
	@echo "🐳 Listing templates in Docker..."
	docker run --rm abides-configgen:v2.0.0 --list-templates

# Cleanup
clean:
	@echo "🧹 Cleaning generated configuration files..."
	@find . -name "*.py" -not -name "configgen.py" -not -name "*_test.py" -delete
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

clean-all: clean
	@echo "🧹 Deep cleaning..."
	@rm -rf .pytest_cache 2>/dev/null || true
	@rm -rf htmlcov 2>/dev/null || true
	@rm -f .coverage 2>/dev/null || true
	@rm -rf output/* 2>/dev/null || true

# Show project info
info:
	@echo "ℹ️  ABIDES Configuration Generator v1.0.0 - Production Release"
	@echo "  📁 Single-file application: configgen.py ($(shell wc -l < configgen.py) lines)"
	@echo "  🐍 Python version: $(shell python --version 2>/dev/null || echo 'Not detected')"
	@echo "  📍 Location: $(PWD)"
	@echo "  🎯 Research Templates: 5 (RMSC03, RMSC04, HFT, Behavioral, Minimal)"
	@echo "  🤖 Agent Types: 6 (Market Maker, Adaptive MM, Momentum, ZI, Noise, Value)"
	@echo "  🏋️  ABIDES-Gym: Compatible mode available"
	@echo "  📦 Dependencies: Zero external dependencies (stdlib only)"