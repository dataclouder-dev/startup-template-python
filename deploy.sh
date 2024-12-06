#!/bin/bash

# Configuration: use same sintax convention, no capital letters, no _ and no spaces
PROJECT_ID=""
IMAGE_NAME="test-image"
REGION="us-central1"
SERVICE_NAME="ai-services"

# Build the container image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME .


# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --project $PROJECT_ID \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated