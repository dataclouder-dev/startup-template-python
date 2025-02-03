include .env

# Variables for deployment
PROJECT_ID ?= dataclouder-dev
IMAGE_NAME ?= python-app-image
REGION ?= us-central1
SERVICE_NAME ?= python-server


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
	poetry run uvicorn app.main:app --reload

	
install:
	pip install -r requirements.txt

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

gcp-deploy:
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



gcp-build-deploy: 
	make gcp-build
	make gcp-deploy

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

# 📦 Package Management Scripts
update-dc:
	@echo "if new library is not working check: poetry cache clear . --all -> poetry update"
	poetry cache clear . --all
	@echo "Updating Dataclouder packages to latest versions..."
	poetry add dataclouder-conversation-ai-cards@latest dataclouder-tts@latest dataclouder-core@latest
	@echo "✅ Dataclouder packages updated successfully!"



