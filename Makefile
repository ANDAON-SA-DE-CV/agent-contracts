# ENIS v3.0 Agent Contracts - Makefile

.PHONY: help install validate generate-sdks test clean lint format

# Default target
help:
	@echo "ENIS v3.0 Agent Contracts - Available commands:"
	@echo ""
	@echo "  install         Install all dependencies"
	@echo "  validate        Validate all contracts and schemas"
	@echo "  generate-sdks   Generate all SDKs from contracts"
	@echo "  test            Run all tests"
	@echo "  lint            Run linting on all code"
	@echo "  format          Format all code"
	@echo "  clean           Clean generated files"
	@echo "  setup           Initial setup (install + validate + generate)"

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "Installing Node.js dependencies..."
	npm install
	@echo "Installing Go dependencies..."
	go mod tidy

# Validate contracts and schemas
validate:
	@echo "Validating OpenAPI specifications..."
	@find contracts/ -name "*.yaml" -o -name "*.yml" | while read file; do \
		echo "Validating $$file"; \
		openapi-spec-validator "$$file" || exit 1; \
	done
	@echo "Validating JSON schemas..."
	@find schemas/ -name "*.json" | while read file; do \
		echo "Validating $$file"; \
		python -c "import json, jsonschema; json.load(open('$$file'))" || exit 1; \
	done
	@echo "All validations passed!"

# Generate SDKs
generate-sdks:
	@echo "Generating TypeScript SDK..."
	npx @openapitools/openapi-generator-cli generate \
		-i contracts/nops-kernel-api.yaml \
		-g typescript-axios \
		-o sdks/typescript/nops-kernel
	@echo "Generating Python SDK..."
	npx @openapitools/openapi-generator-cli generate \
		-i contracts/nops-kernel-api.yaml \
		-g python \
		-o sdks/python/nops-kernel
	@echo "Generating Go SDK..."
	npx @openapitools/openapi-generator-cli generate \
		-i contracts/nops-kernel-api.yaml \
		-g go \
		-o sdks/go/nops-kernel
	@echo "All SDKs generated!"

# Run tests
test:
	@echo "Running Python tests..."
	python -m pytest tests/ -v
	@echo "Running TypeScript tests..."
	npm test
	@echo "Running Go tests..."
	go test ./...

# Lint code
lint:
	@echo "Linting Python code..."
	flake8 src/ tests/
	@echo "Linting TypeScript code..."
	npm run lint
	@echo "Linting Go code..."
	golangci-lint run

# Format code
format:
	@echo "Formatting Python code..."
	black src/ tests/
	isort src/ tests/
	@echo "Formatting TypeScript code..."
	npm run format

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf sdks/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	@echo "Clean complete!"

# Initial setup
setup: install validate generate-sdks
	@echo "Setup complete! Repository is ready for development."

# Development workflow
dev: validate generate-sdks test
	@echo "Development workflow complete!"

# CI/CD workflow
ci: validate test lint
	@echo "CI/CD workflow complete!"
