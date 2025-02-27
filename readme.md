# DataClouder Python Template

### Description

This repository contains additional services required by the DataClouder template. For reference implementations, check out our other templates:

- [DataClouder Angular Template](https://github.com/dataclouder-dev/dataclouder-template-angular)
- [DataClouder Node Template](https://github.com/dataclouder-dev/dataclouder-template-node)

## Getting Started

### Clone the Project

```bash
git clone https://github.com/dataclouder-dev/dataclouder-template-python [your-project-name]
```

## 🛠️ Prerequisites

- Python >= 3.11
- Poetry >= 2.0.0 (Optional but recommended)
- Docker (Optional)
- Google Cloud credentials and environment variables
- Access to Polilan repository

## 🚀 Installation Options

### Option 1: Using Makefile (Recommended)

Requires Poetry and Docker to be installed.

```bash
# Single command setup (Work in Progress)
make start
```

### Option 2: Traditional Setup

#### 1. Environment Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# For Unix/MacOS:
source .venv/bin/activate
# For Windows:
.venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

#### 3. Configuration
You'll need to obtain the following from the Polilan development team:
- Google Cloud credential file (place in `/.cred` folder)
- Environment variables template (`.env` file)

#### 4. Launch Application
```bash
# Option 1: Using uvicorn
uvicorn app.main:app --reload

# Option 2: Using FastAPI development server
fastapi dev app/main.py
```

Once running, access the API documentation at: http://127.0.0.1:8000/docs

## 🌎 Deployment Environments

| Environment | URL |
|------------|-----|
| QA | https://..... |
| Production | https://..... |

## Deployment Options

### Manual Deployment

1. Set environment variables:
   - Add `.env` file to the project root

2. Build Docker image:
   ```bash
   make gcp-build
   ```

3. Deploy to Google Cloud Run:
   ```bash
   make gcp-deploy
   ```

### Automated Deployment with Cloud Build

**Note:** Before setting up automated deployment, we recommend performing one manual deployment to verify everything works correctly. Initial deployments require setting up Cloud Run service variables, while subsequent deployments do not. Also note that manual deployments use the default GCR repository for artifacts, while automated deployments use a custom repository.

Steps:
1. Fork the repository
2. Go to Cloud Build and create a new trigger
3. Grant GitHub access, select the repository, and accept conditions
4. Configure trigger settings according to your needs
5. Optional: Add permissions to the service account (Logs Writer, Cloud Run Admin, or default logs only)
6. Add the repository in Artifact Registry (recommended: add policies to remove old versions)

## Development Tools

### Poetry Package Manager

Poetry is the recommended package manager for this project. Here are some useful commands:

```bash
poetry add <package>        # Add a new package
poetry remove <package>     # Remove a package
poetry update <package>     # Update a package
poetry install             # Install all dependencies
poetry build               # Build the project
poetry publish            # Publish the package
poetry show               # Check dependencies
```

### Docker Commands

```bash
# Build the image
docker build -t dc_python_server_image .

# Run the container
docker run -it -p 8080:8080 dc_python_server_image
```

### Code Quality Tools

We highly recommend using [Ruff](https://pypi.org/project/ruff/), a fast Python linter and formatter that replaces multiple tools like flake8. Settings are configured in the `pyproject.toml` file.

#### VSCode Integration
Install the [Ruff VSCode Extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

#### Useful Ruff Commands
```bash
ruff check .                  # Check for issues
ruff check --fix .           # Fix issues automatically
ruff format .                # Format code
ruff check --fix --format .  # Fix issues and format code
```

For more information about Ruff rules and configuration, visit the [official documentation](https://docs.astral.sh/ruff/).




