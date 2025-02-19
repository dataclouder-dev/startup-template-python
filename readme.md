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

#### 1) Set environment variables
    add .env file to the root of the project

#### 2) Build docker image
    make gcp-build

#### 3) Deploy to Google Cloud Run
    make gcp-deploy

### Automated Deployment With Cloud Build 

Note: before try to automate the deployment, i highly recommend do one manual deployment to check if everything is working. specially becouse for every cloud run service, variables need to be set first time, consecutives times no need. also check first deployment is in gcr default repository for artifact, but for automated is in custom repository

1. Fork the repository
2. Go to cloud build and create a new trigger
3. Grant github access, select the repository and accept conditions
4. Add seetings for the trigger to your needs
5. Optional: Add permissions to the service account, Logs Writer, Cloud Run Admin or log only default logs
6. Add the repository in artifact registry (recommended add policies to remove old versions)


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


### Developer Experience

highly recommend this tools
https://pypi.org/project/ruff/
Ruff is a replacement for flake8, and linters and other formatters tools. settings are placed in pyproject.toml file.

Install extention in vscode

https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff

Check documentation and rules 
https://docs.astral.sh/ruff/

Coomands 
ruff check .
ruff check --fix .
ruff format .
ruff check --fix --format .




