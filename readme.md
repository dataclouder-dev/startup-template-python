### Description
WIP: very basic template, don't use yet, WIP.

## 🛠️ Prerequisites

- Python >= 3.11
- Poetry >= 2.0.0 (Optinal recommended)
- Docker (optional)
- Google Cloud credentials and environment variables
- Access to Polilan repository



## 🚀 Local Setup Makefile

it depends on poetry and docker, you need to install them.


```bash
### I'm specting to handle everything in one command, WIP
make start
```

## 🏗️ Local Development Setup Traditional Way

### 1. Environment Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# For Unix/MacOS:
source .venv/bin/activate
# For Windows:
.venv\Scripts\activate
```

### 2. Dependencies
```bash
# Install required packages
pip install -r requirements.txt

```

### 3. Configuration
You'll need to obtain the following from the Polilan dev team:
- Google Cloud credential file (place in `/.cred` folder)
- Environment variables template (`.env` file)

### 4. Launch Application
```bash
uvicorn app.main:app --reload

# Optionally, if you want to use fastapi dev
fastapi dev app/main.py
```


Once running, access the API documentation at: http://127.0.0.1:8000/docs

## 🌎 Environments

| Environment | URL |
|------------|-----|
| QA | https://..... |
| Production | https://..... |



## Manual deploy

### 1) Set environment variables
    add .env file to the root of the project

### 2) Build docker image
    make build-docker

### 3) Deploy to Google Cloud Run
    make deploy-gcp


### Poetry quick tutorial in case first time using it

poetry add <package>


### usefull commands poetry 

poetry add <package>
poetry remove <package>
poetry update <package>
poetry install
poetry build
poetry publish
poetry show : check dependencies


### Docker commands

docker build -t dc_python_server_image .

docker run -it -p 8080:8080 dc_python_server_image
