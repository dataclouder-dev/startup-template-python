# 🐍 Startup Template Python

### 📝 Description

This repository contains additional services required by the DataClouder template. For reference implementations, check out our other templates:

- [DataClouder Angular Template](https://github.com/dataclouder-dev/dataclouder-template-angular)
- [DataClouder Node Template](https://github.com/dataclouder-dev/dataclouder-template-node)

## 🚀 Getting Started

### Clone the Project

```bash
git clone https://github.com/dataclouder-dev/dataclouder-template-python [your-project-name]
```

or use the button on github right top corner CREATE TEMPLATE

## ✅ Prerequisites

- Python >= 3.11
- Make >= 3.0.0 (Optional but highly recommended)
- UV (latest version recommended, install via `pip install uv` or `pipx install uv`)
- Docker (Optional)
- Google Cloud credentials and environment variables
- MongoDB credentials

## ⚙️ Installation Options

* .env file is required, you need to create it but can copy and paste from .env.example, then set the variables

* Google service account file is required and placed it in the `./.cred` folder at the project root

check documentation how to create service account [here](https://cloud.google.com/iam/docs/service-accounts-create)

You should be ready to go


### Option 1: Using Makefile (Recommended)

Requires UV and Docker to be installed.

```bash
make install # Only the first time
# Single command setup (Work in Progress)
make start
```

### Option 2: Traditional Setup 🚶

#### 1. Environment Setup
```bash
# Create virtual environment
uv venv .venv # Or python3 -m venv .venv

# Activate virtual environment
# For Unix/MacOS:
source .venv/bin/activate
# For Windows:
.venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
# Install dependencies using UV (ensure uv.lock is up to date)
uv sync
```

#### 3. Configuration
- Google Cloud credential file (place in `/.cred` folder)
- Environment variables template (`.env` file)

#### 4. Launch Application
```bash
# Option 1: Using uvicorn (after activating venv)
uvicorn app.main:app --reload

# Option 2: Using FastAPI development server (after activating venv)
# fastapi dev app/main.py # If fastapi-cli is installed

# Option 3) Recommended (uses uv run)
make start
```

Once running, access the API documentation at: http://127.0.0.1:8000/docs

## ☁️ Deployment Environments

| Environment | URL |
|------------|-----|
| QA | https://..... |
| Production | https://..... |

## 🚢 Deployment Options

### Manual Deployment 👨‍💻

1. Set environment variables:
   - Ensure the `.env` file is present in the project root

2. Build Docker image:
   ```bash
   make docker-build 
   ```
   (Note: `make gcp-build` submits to Google Cloud Build, `make docker-build` builds locally)


3. Deploy to Google Cloud Run:
   ```bash
   make gcp-deploy-service 
   ```
   (Note: `make gcp-deploy` includes the gcp-build step)


### Automated Deployment with Cloud Build 🤖

Change project name in `Makefile`. 
then just run 
make deploy 

Note: if you want to automate multiple environment remember that makefile just replace if the variables in the .env dont exist so adding this variables in .env will have priority. you can add per every environment



**Note:** Before setting up automated deployment, we recommend performing one manual deployment to verify everything works correctly. Initial deployments require setting up Cloud Run service variables, while subsequent deployments do not. Also note that manual deployments use the default GCR repository for artifacts, while automated deployments use a custom repository.

Steps:
1. Fork the repository
2. Go to Cloud Build and create a new trigger
3. Grant GitHub access, select the repository, and accept conditions
4. Configure trigger settings according to your needs
5. Optional: Add permissions to the service account (Logs Writer, Cloud Run Admin, or default logs only)
6. Add the repository in Artifact Registry (recommended: add policies to remove old versions)

## 🔧 Development Tools

### Dependency Management with UV 🛠️

UV is used for managing dependencies and virtual environments in this project. Key commands:

- **Create/Activate Virtual Environment & Install Dependencies:**
  ```bash
  # Create a virtual environment (if it doesn't exist) and install/sync dependencies
  make install 
  # or manually:
  uv venv
  source .venv/bin/activate # On Unix/macOS
  # .venv\Scripts\activate # On Windows
  uv sync # Installs based on pyproject.toml and uv.lock
  ```

- **Adding a new package:**
  1. Add the package to `[project.dependencies]` or `[project.optional-dependencies]` in your [`pyproject.toml`](./pyproject.toml:0).
  2. Then run:
     ```bash
     uv sync
     uv lock # To update the lock file
     ```
  Alternatively, for quick additions (which will also update `pyproject.toml` if it's a project):
     ```bash
     uv pip install <package-name>
     uv lock
     ```

- **Removing a package:**
  1. Remove the package from your [`pyproject.toml`](./pyproject.toml:0).
  2. Then run:
     ```bash
     uv sync
     uv lock
     ```

- **Updating a package:**
  1. Update the version constraint in your [`pyproject.toml`](./pyproject.toml:0).
  2. Then run:
     ```bash
     uv sync
     uv lock
     ```
  Or, to update to the latest version and update `pyproject.toml`:
     ```bash
     uv pip install <package-name>@latest
     uv lock
     ```

- **Listing installed packages:**
  ```bash
  uv pip list
  # or for a requirements.txt-like format:
  uv pip freeze
  ```

- **Generating/Updating the lock file:**
  ```bash
  uv lock
  ```
Building and publishing are handled by `hatchling` as defined in `pyproject.toml` and typically involve using tools like `twine` for publishing to PyPI.

### Merge Upstream Updates 🔄
You can create new project but, if you want to get updates from the template, you can run

```bash
make merge-upstream
```

### Docker Commands 🐳

```bash
# Build the image
make docker-build
# or manually:
# docker build -t dc_python_server_image . 
# (Ensure IMAGE_NAME in Makefile matches if using manual command)

# Run the container
make docker-run
# or manually:
# docker run -it -p 8000:8080 dc_python_server_image
```

### Code Quality Tools ✨

We highly recommend using [Ruff](https://pypi.org/project/ruff/), a fast Python linter and formatter that replaces multiple tools like flake8. Settings are configured in the `pyproject.toml` file.

#### VSCode Integration
Install the [Ruff VSCode Extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

#### Useful Ruff Commands
```bash
# These can be run directly if .venv is activated, or via 'uv run':
uv run ruff check .                  # Check for issues
uv run ruff check --fix .           # Fix issues automatically
uv run ruff format .                # Format code
uv run ruff check --fix --format .  # Fix issues and format code
```

For more information about Ruff rules and configuration, visit the [official documentation](https://docs.astral.sh/ruff/).