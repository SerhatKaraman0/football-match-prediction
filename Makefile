# ETL Pipeline Template Project
# Makefile for easy CLI usage

.PHONY: help install setup clean test lint format build run docker-build docker-run docker-stop docker-clean deploy train predict status logs

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip
VENV := venv
APP_NAME := etlpipeline
DOCKER_IMAGE := $(APP_NAME)
DOCKER_CONTAINER := $(APP_NAME)
PORT := 8000
DOCKER_PORT := 8080

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ##  Show this help message
	@echo "$(BLUE)ETL Pipeline Template Project$(NC)"
	@echo "$(BLUE)==============================$(NC)"
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

# Development Environment
install: ##  Install dependencies
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN) Dependencies installed successfully!$(NC)"

setup: ##  Setup development environment
	@echo "$(GREEN)Setting up development environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(YELLOW)Activating virtual environment...$(NC)"
	@echo "Run: source $(VENV)/bin/activate"
	@echo "Then run: make install"
	@echo "$(GREEN) Virtual environment created!$(NC)"

clean: ##  Clean up temporary files and caches
	@echo "$(GREEN)Cleaning up...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	@echo "$(GREEN) Cleanup completed!$(NC)"

# Code Quality
lint: ##  Run code linting
	@echo "$(GREEN)Running linting...$(NC)"
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; \
	else \
		echo "$(YELLOW)flake8 not installed, skipping...$(NC)"; \
	fi
	@echo "$(GREEN) Linting completed!$(NC)"

format: ##  Format code with black
	@echo "$(GREEN)Formatting code...$(NC)"
	@if command -v black >/dev/null 2>&1; then \
		black . --line-length 88; \
	else \
		echo "$(YELLOW)black not installed, skipping...$(NC)"; \
	fi
	@echo "$(GREEN) Code formatting completed!$(NC)"

test: ##  Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	@if command -v pytest >/dev/null 2>&1; then \
		pytest -v; \
	else \
		echo "$(YELLOW)pytest not installed, running basic Python tests...$(NC)"; \
		$(PYTHON) -m unittest discover -s . -p "*test*.py" -v; \
	fi
	@echo "$(GREEN) Tests completed!$(NC)"

# Application
run: ##  Run the application locally
	@echo "$(GREEN)Starting application on port $(PORT)...$(NC)"
	@echo "$(BLUE)Access at: http://localhost:$(PORT)$(NC)"
	@echo "$(BLUE)API docs at: http://localhost:$(PORT)/docs$(NC)"
	$(PYTHON) app.py

train: ##  Train the ML model
	@echo "$(GREEN)Starting ETL pipeline training...$(NC)"
	curl -X GET http://localhost:$(PORT)/train || echo "$(RED)Error: Make sure the app is running (make run)$(NC)"
	@echo "$(GREEN) ETL training pipeline triggered!$(NC)"

predict: ##  Run ETL prediction pipeline (requires CSV file)
	@echo "$(GREEN)Running ETL prediction pipeline...$(NC)"
	@if [ -f "test_sample.csv" ]; then \
		curl -X POST -F "file=@test_sample.csv" http://localhost:$(PORT)/predict; \
	else \
		echo "$(RED)Error: test_sample.csv not found!$(NC)"; \
		echo "$(YELLOW)Create a CSV file or use: make create-sample$(NC)"; \
	fi
	@echo ""

create-sample: ##  Create sample test data for ETL pipeline
	@echo "$(GREEN)Creating sample ETL test data...$(NC)"
	$(PYTHON) -c "import pandas as pd; import numpy as np; \
	data = pd.read_csv('data/phisingData.csv').drop('Result', axis=1).head(5); \
	data.to_csv('test_sample.csv', index=False); \
	print(' Sample ETL data created: test_sample.csv')"

# Docker Commands
docker-build: ##  Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t $(DOCKER_IMAGE) .
	@echo "$(GREEN) Docker image built: $(DOCKER_IMAGE)$(NC)"

docker-run: ##  Run Docker container
	@echo "$(GREEN)Starting Docker container...$(NC)"
	docker run -d -p $(DOCKER_PORT):$(PORT) \
		--name $(DOCKER_CONTAINER) \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-e AWS_REGION=${AWS_REGION} \
		$(DOCKER_IMAGE)
	@echo "$(GREEN) Container started!$(NC)"
	@echo "$(BLUE)Access at: http://localhost:$(DOCKER_PORT)$(NC)"

docker-stop: ##  Stop Docker container
	@echo "$(GREEN)Stopping Docker container...$(NC)"
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true
	@echo "$(GREEN)✅ Container stopped and removed!$(NC)"

docker-logs: ##  Show Docker container logs
	@echo "$(GREEN)Docker container logs:$(NC)"
	docker logs $(DOCKER_CONTAINER)

docker-shell: ##  Open shell in Docker container
	@echo "$(GREEN)Opening shell in container...$(NC)"
	docker exec -it $(DOCKER_CONTAINER) /bin/bash

docker-clean: ##  Clean Docker images and containers
	@echo "$(GREEN)Cleaning Docker resources...$(NC)"
	docker system prune -f
	docker image prune -f
	@echo "$(GREEN) Docker cleanup completed!$(NC)"

# Deployment
deploy: docker-build ##  Build and deploy to production
	@echo "$(GREEN)Deploying to production...$(NC)"
	@echo "$(YELLOW)Pushing to Git repository...$(NC)"
	git add .
	git commit -m "Deploy: $(shell date)" || true
	git push
	@echo "$(GREEN) Deployment triggered via GitHub Actions!$(NC)"

# Monitoring
status: ##  Check application status
	@echo "$(GREEN)Checking application status...$(NC)"
	@echo "$(BLUE)Local application:$(NC)"
	@curl -s http://localhost:$(PORT)/ >/dev/null && echo "$(GREEN)✅ Local app is running$(NC)" || echo "$(RED)❌ Local app is not running$(NC)"
	@echo "$(BLUE)Docker container:$(NC)"
	@docker ps | grep $(DOCKER_CONTAINER) >/dev/null && echo "$(GREEN)✅ Docker container is running$(NC)" || echo "$(RED)❌ Docker container is not running$(NC)"

logs: ##  Show application logs
	@echo "$(GREEN)Application logs:$(NC)"
	@if [ -d "logs" ]; then \
		tail -f logs/*.log; \
	else \
		echo "$(YELLOW)No log files found$(NC)"; \
	fi

# Development Workflow
dev: setup install ##  Complete development setup
	@echo "$(GREEN) Development environment ready!$(NC)"
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "1. source $(VENV)/bin/activate"
	@echo "2. make run"

full-test: clean lint test ##  Run full test suite
	@echo "$(GREEN) Full test suite completed!$(NC)"

docker-dev: docker-build docker-stop docker-run ##  Full Docker development cycle
	@echo "$(GREEN) Docker development environment ready!$(NC)"

# CI/CD Helpers
ci-install: ##  CI/CD: Install dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

ci-test: ##  CI/CD: Run tests
	$(PYTHON) -m pytest -v || $(PYTHON) -m unittest discover -s . -p "*test*.py" -v

ci-build: ##  CI/CD: Build application
	$(PYTHON) -c "import app; print(' App imports successfully')"

# Utilities
check-deps: ##  Check for outdated dependencies
	@echo "$(GREEN)Checking for outdated dependencies...$(NC)"
	$(PIP) list --outdated

update-deps: ##  Update dependencies
	@echo "$(GREEN)Updating dependencies...$(NC)"
	$(PIP) install --upgrade -r requirements.txt

env-info: ##  Show environment information
	@echo "$(BLUE)Environment Information:$(NC)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"
	@echo "Docker: $(shell docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Git: $(shell git --version 2>/dev/null || echo 'Not installed')"
	@echo "Working Directory: $(PWD)"

# Quick commands for common workflows
quick-start: install run ##  Quick start: install and run
	@echo "$(GREEN) Quick start completed!$(NC)"

quick-docker: docker-build docker-run ##  Quick Docker: build and run
	@echo "$(GREEN) Quick Docker setup completed!$(NC)"

restart: docker-stop docker-run ##  Restart Docker container
	@echo "$(GREEN) Container restarted!$(NC)"

# Help for specific topics
help-dev: ##  Development help
	@echo "$(BLUE)Development Workflow:$(NC)"
	@echo "1. make setup          # Create virtual environment"
	@echo "2. source venv/bin/activate"
	@echo "3. make install        # Install dependencies"
	@echo "4. make run            # Start application"
	@echo ""
	@echo "$(BLUE)Testing:$(NC)"
	@echo "make test              # Run tests"
	@echo "make lint              # Check code quality"
	@echo "make format            # Format code"
	@echo ""

help-docker: ##  Docker help
	@echo "$(BLUE)Docker Workflow:$(NC)"
	@echo "1. make docker-build   # Build image"
	@echo "2. make docker-run     # Run container"
	@echo "3. make docker-logs    # View logs"
	@echo "4. make docker-stop    # Stop container"
	@echo ""
	@echo "$(BLUE)Quick commands:$(NC)"
	@echo "make quick-docker      # Build and run"
	@echo "make restart           # Restart container"
	@echo ""

help-deploy: ##  Deployment help
	@echo "$(BLUE)Deployment Workflow:$(NC)"
	@echo "1. Set environment variables in GitHub Secrets"
	@echo "2. make deploy         # Trigger deployment"
	@echo "3. Check GitHub Actions for progress"
	@echo ""
	@echo "$(BLUE)Required GitHub Secrets for ETL Pipeline:$(NC)"
	@echo "- AWS_ACCESS_KEY_ID"
	@echo "- AWS_SECRET_ACCESS_KEY"
	@echo "- AWS_REGION"
	@echo "- AWS_ECR_LOGIN_URI"
	@echo "- ECR_REPOSITORY_NAME"
	@echo ""
	@echo "$(BLUE)Template Customization:$(NC)"
	@echo "1. Update data sources in data/ directory"
	@echo "2. Modify ML models in etl_project/components/"
	@echo "3. Configure pipeline parameters in config/"
	@echo "4. Customize frontend in templates/"
	@echo ""
