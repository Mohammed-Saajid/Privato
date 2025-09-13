# Use .DEFAULT_GOAL to set the command that runs when you just type "make".
.DEFAULT_GOAL := help


# VARIABLES
# Define variables centrally. Use `:=` for immediate evaluation.

PYTHON_VERSION := 3.11
VENV_DIR       := .venv
PYTHON         := $(VENV_DIR)/bin/python

# For Windows compatibility
ifeq ($(OS),Windows_NT)
    PYTHON := $(VENV_DIR)/Scripts/python
endif


# PHONY TARGETS
# Declare all command-based targets as .PHONY.

.PHONY: help install-dev install test run clean deploy down


# PROJECT COMMANDS


help:
	@echo "Available commands:"
	@echo "  install      Install all project dependencies for production."
	@echo "  install-dev   Install all project dependencies for development."
	@echo "  test          Run the test suite."
	@echo "  run           Run the FastAPI development server."
	@echo "  clean         Remove all temporary files and build artifacts."
	@echo "  deploy        Build and run the application with Docker Compose."
	@echo "  down          Stop and remove the Docker Compose containers."

install: ## Install production dependencies
	@echo "--> Setting up virtual environment in $(VENV_DIR)..."
	python -m venv $(VENV_DIR)
	@echo "--> Installing production dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install uv
	$(PYTHON) -m uv pip install -e "."
	@echo "Dependencies installed."

install-dev: ## Install development dependencies
	@echo "--> Setting up virtual environment in $(VENV_DIR)..."
	python -m venv $(VENV_DIR)
	@echo "--> Installing development dependencies with uv..."
	$(PYTHON) -m pip install uv
	$(PYTHON) -m uv pip install -e ".[dev]"
	@echo "Dependencies installed."

test: ## Run the test suite
	@echo "--> Running tests with pytest..."
	$(PYTHON) -m pytest tests -vv

run: install-dev ## Run the FastAPI development server
	@echo "--> Starting FastAPI server on http://0.0.0.0:8080..."
	$(PYTHON) -m uvicorn app.main:app --reload --reload-dir app --host 0.0.0.0 --port 8080

clean: ## Remove all build artifacts and temporary files
	@echo "--> Cleaning up project..."
	$(PYTHON) -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.cache', 'build', 'dist', '.pytest_cache', '__pycache__', '.venv'] if p]"
	@echo "Cleanup complete."

deploy: ## Build and run Docker containers
	@echo "--> Building and starting Docker containers..."
	docker-compose up --build -d
	@echo "Application deployed."

down: ## Stop and remove Docker containers
	@echo "--> Stopping and removing Docker containers..."
	docker-compose down
	@echo "Containers stopped."

# This is a hidden target used by others, not meant to be called directly
.env:
	@if [ ! -f .env ]; then \
		echo "--> Creating .env file from .env.example..."; \
		cp .env.example .env; \
	fi