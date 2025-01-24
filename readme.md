### Description
WIP: very basic template, don't use. 

### Create virtual env

python3 -m venv .venv

unix: 
    source .venv/bin/activate  
windows: 
    .venv\Scripts\activate

pip3 install -r requirements.txt

### Run service locally

uvicorn app.main:app --reload



### Upload Service to GCP Cloud Run

deploy.sh



### Manual deploy

gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME ../.

gcloud run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$IMAGE_NAME --platform managed --region $REGION --allow-unauthenticated

### Example Deploy

gcloud builds submit --tag gcr.io/dataclouder-dev/python-app-image .

gcloud run deploy python-web-service --image gcr.io/dataclouder-dev/python-app-image --platform managed --region us-central1 --allow-unauthenticated