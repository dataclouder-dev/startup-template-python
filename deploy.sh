#!/bin/bash

# Configuration
PROJECT_ID="appingles-qa"
IMAGE_NAME="test-Python"
REGION="us-central1"
SERVICE_NAME="ai-services"

# Build the container image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --project $PROJECT_ID \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated