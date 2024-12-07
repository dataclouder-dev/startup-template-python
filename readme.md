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

