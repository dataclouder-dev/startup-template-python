include .env

# Variables for deployment replace [startup-template] for your project name
PROJECT_NAME ?= startup-template
PROJECT_ID ?= $(PROJECT_NAME)-dev
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
	poetry run ruff check .
	poetry run uvicorn app.main:app --reload

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
	poetry install

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



deploy: 
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
	poetry show

# 📦 Package Management Scripts
update-dc:
	@echo "if new library is not working check: poetry cache clear . --all -> poetry update"
	poetry cache clear . --all
	@echo "Updating Dataclouder packages to latest versions..."
	poetry add dataclouder-conversation-ai-cards@latest dataclouder-tts@latest dataclouder-core@latest dataclouder-mongo@latest
	@echo "✅ Dataclouder packages updated successfully!"



