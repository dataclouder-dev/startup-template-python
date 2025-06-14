include .env

# Variables for deployment replace [startup-template] for your project name
PROJECT_NAME ?= dataclouder-dev
PROJECT_ID ?= $(PROJECT_NAME)
IMAGE_NAME ?= $(PROJECT_NAME)-python-image
SERVICE_NAME ?= $(PROJECT_NAME)-python-server
REGION ?= us-central1


.PHONY: deploy build run-local install clean help

help:
	@echo "Available commands:"
	@echo "  make install    - Install project dependencies"
	@echo "  make build      - Build Docker image"
	@echo "  make deploy     - Deploy to Google Cloud Run"
	@echo "  make clean      - Clean up build artifacts"
	@echo "  make run-local  - Run the application locally"

# Run the FastAPI application in development mode
start:
	uv run ruff check .
	uv run uvicorn app.main:app --reload

merge-upstream:
	@echo "Fetching and merging updates from upstream repository..."
	@if ! git config remote.upstream.url > /dev/null; then \
		echo "Adding upstream remote..."; \
		git remote add upstream https://github.com/dataclouder-dev/startup-template-python.git; \
	fi
	git fetch upstream
	git checkout main
	@echo "Merging upstream/main into local main branch..."
	git merge upstream/main --allow-unrelated-histories || { \
		echo "Merge conflicts detected. Please resolve conflicts and complete the merge manually."; \
		echo "After resolving conflicts, commit changes and push to origin."; \
		exit 1; \
	}

	
install:
	uv venv && uv sync

# ☁️ Google Cloud Scripts 

gcp-enable-services:
	@echo "Enabling required services for $(PROJECT_ID)..."
	gcloud config set project $(PROJECT_ID)
	gcloud services enable run.googleapis.com
	gcloud services enable cloudbuild.googleapis.com

gcp-build:
	@echo " -> upload to gcp  and building $(PROJECT_ID)/$(IMAGE_NAME)... "
	gcloud auth print-access-token >/dev/null 2>&1 || (echo "Please run 'gcloud auth login' first" && exit 1)

	gcloud config set project $(PROJECT_ID)
	gcloud builds submit --tag gcr.io/$(PROJECT_ID)/$(IMAGE_NAME) .

gcp-deploy-service:
	@echo "-> Deploying Lastest Build $(PROJECT_ID)/$(IMAGE_NAME) to Google Cloud Run... "
	@ENV_VARS=$$(python3 scripts/env-parser.py); \
	echo "Environment Variables to be deployed:"; \
	echo "$${ENV_VARS}" | tr ',' '\n'; \
	gcloud run deploy $(SERVICE_NAME) \
		--image gcr.io/$(PROJECT_ID)/$(IMAGE_NAME) \
		--project $(PROJECT_ID) \
		--region $(REGION) \
		--platform managed \
		--allow-unauthenticated \
		--set-env-vars "$${ENV_VARS}"


# Deploy without local env vars (Not used as default.)
gcp-deploy-service-no-local-env-vars:
	@echo "-> Deploying Lastest Build $(PROJECT_ID)/$(IMAGE_NAME) to Google Cloud Run... "
	gcloud run deploy $(SERVICE_NAME) \
		--image gcr.io/$(PROJECT_ID)/$(IMAGE_NAME) \
		--project $(PROJECT_ID) \
		--region $(REGION) \
		--platform managed \
		--allow-unauthenticated \


deploy:
	@echo "-> Deploying Lastest Build $(PROJECT_ID)/$(IMAGE_NAME) -> $(PROJECT_NAME) to Google Cloud Run... "
	make gcp-build
	make gcp-deploy-service

# 🚢 Docker Scripts

docker-build:
	@echo "Building Docker image named $(IMAGE_NAME) ..."
	docker build -t $(IMAGE_NAME) .

# Run the Docker image
docker-run:
	@echo "Running Docker image named $(IMAGE_NAME) ..."
	docker run -it -p 8000:8080 $(IMAGE_NAME)


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 

make show:
	uv pip list

# 📦 Package Management Scripts
update-dc:
	@echo "Assuming Dataclouder package versions in pyproject.toml have been manually updated."
	@echo "Syncing environment with pyproject.toml..."
	uv sync
	@echo "✅ Environment synced with pyproject.toml."
	@echo "If you updated dependencies, consider running 'uv lock' and committing pyproject.toml and uv.lock."


# 🔄 Reinstall everything in a fresh virtual environment
reinstall:
	@echo "🧹 Removing existing virtual environments..."
	rm -rf .venv
	@echo "🗑️ Cleaning up Python cache files..."
	make clean
	@echo "🔄 Creating a fresh virtual environment and installing dependencies..."
	uv venv && uv sync
	@echo "✅ Fresh installation completed successfully!"

force-reinstall:
	uv lock
	uv sync
