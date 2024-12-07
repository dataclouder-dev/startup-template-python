#!/bin/bash

# Configuration: use same sintax convention, no capital letters, no _ and no spaces
PROJECT_ID="poder-del-guion"
IMAGE_NAME="fastapi-back"
REGION="us-central1"
SERVICE_NAME="python-back"
BILLING_ACCOUNT_ID="YOUR_BILLING_ACCOUNT_ID" # Replace with your actual billing account ID


# First problem.  how to set permissions to another email. may be they don't need


# export PROJECT_ID="your-project-id"

gcloud config set project $PROJECT_ID

# Enable required APIs
echo __Enabling required APIs__
gcloud services enable run.googleapis.com --project $PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project $PROJECT_ID

echo __ All services are enabled __
# Enable billing for the project: 
# TODO: ill do this step manually, but check for next time how to enable it
# gcloud beta billing projects link $PROJECT_ID --billing-account $BILLING_ACCOUNT_ID

# cloudbuild.googleapis.com

# # Build the container image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME .


# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --project $PROJECT_ID \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated