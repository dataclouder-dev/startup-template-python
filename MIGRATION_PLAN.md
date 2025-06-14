# Migration Plan: Poetry to UV

**Goal:** Transition the project's dependency management and virtual environment handling from Poetry to UV, ensuring local development, Docker builds, and GCP deployments function correctly with UV.

**Key Advantages of UV:**

*   **Speed:** UV is significantly faster at dependency resolution and installation.
*   **Simplicity:** It aims to be a drop-in replacement for `pip` and `venv` workflows, often with simpler commands.
*   **Compatibility:** UV works directly with `pyproject.toml` (PEP 621) for project metadata and dependencies.

---

## Phase 1: Preparation & Understanding

1.  **Backup Your Project:**
    *   **Action:** Before making any changes, ensure your project is fully committed to Git, and consider creating a new branch for this migration (e.g., `feature/uv-migration`).
    *   **Reasoning:** Safeguards against any unforeseen issues during the migration.

2.  **Install UV:**
    *   **Action (User):** Install UV on your local development machine. The recommended way is usually via `pipx` or `pip`:
        ```bash
        pipx install uv
        # OR
        pip install uv
        ```
    *   **Reference:** [UV Installation Guide](https://astral.sh/docs/uv/install)
    *   **Reasoning:** You'll need UV locally to test commands and manage your environment.

---

## Phase 2: Core Migration - Local Environment & Docker

1.  **Update `Makefile` Commands:**
    *   **Action:** Replace Poetry commands in your [`Makefile`](./Makefile) with their UV equivalents.
    *   **Details:**
        *   **Virtual Environment Creation/Management:**
            *   Poetry: `poetry install`, `poetry env use /path/to/python`
            *   UV: `uv venv` (creates `.venv`), `uv sync` (installs dependencies from `pyproject.toml` into the active venv).
        *   **Running Commands in Venv:**
            *   Poetry: `poetry run <command>`
            *   UV: If `.venv` is activated (`source .venv/bin/activate`), just run `<command>`. If not, `uv run <command>`.
        *   **Adding Dependencies:**
            *   Poetry: `poetry add <package>`
            *   UV: `uv pip install <package>` (UV will update `pyproject.toml` if it's a project, or you might manage `pyproject.toml` manually and then `uv sync`). *For this project, since `pyproject.toml` is the source of truth, you'd typically add dependencies there manually or via a tool that edits it, then run `uv sync`.*
        *   **Locking:**
            *   Poetry: `poetry lock`
            *   UV: `uv lock` (creates/updates `uv.lock`) or `uv pip compile pyproject.toml -o requirements.txt` if a `requirements.txt` flow is preferred for some reason.
    *   **Specific [`Makefile`](./Makefile) Changes (Illustrative - actual changes will be applied in implementation):**
        *   **`start` target:**
            *   `poetry run ruff check .` -> `uv run ruff check .`
            *   `poetry run uvicorn app.main:app --reload` -> `uv run uvicorn app.main:app --reload`
        *   **`install` target:**
            *   `poetry install` -> `uv venv && uv sync`
        *   **`update-dc` target:**
            *   Manual update of [`pyproject.toml`](./pyproject.toml) versions, then `uv sync`.
        *   **`reinstall` target:**
            *   `poetry env remove --all` -> `rm -rf .venv`
            *   `poetry install` -> `uv venv && uv sync`
            *   Remove `pip install -r requirements.txt`.
        *   **`force-reinstall` target:**
            *   `poetry lock` -> `uv lock` (or `uv pip compile ...`)
            *   `poetry install` -> `uv sync` (or `uv pip sync ...`)
    *   **Reasoning:** Aligns your local build and utility scripts with UV's command structure.

2.  **Update `Dockerfile`:**
    *   **Action:** Modify the [`Dockerfile`](./Dockerfile) to use UV for installing dependencies.
    *   **Details (Illustrative):**
        *   **Builder Stage:**
            *   Replace `RUN pip install poetry==1.8.3` with `RUN pip install uv`.
            *   Remove Poetry-specific ENV variables.
            *   Replace `RUN poetry install --no-root` with:
                ```dockerfile
                # Assuming the whole project is copied first as in current Dockerfile
                COPY . . 
                RUN uv venv --python 3.12.7 && \
                    uv sync --no-dev 
                ```
        *   **Runtime Stage:** No changes anticipated if the builder stage correctly creates `/app/.venv`.
    *   **Reasoning:** Uses UV's speed and capabilities within your Docker image build process.

3.  **Handle Lock Files:**
    *   **Action:** Adopt `uv.lock`.
        1.  Generate `uv.lock`: `uv lock` (after `pyproject.toml` is potentially updated to PEP 621 format if chosen).
        2.  Add `uv.lock` to Git.
        3.  Update [`Dockerfile`](./Dockerfile) to use `uv sync --locked` if `uv.lock` is present.
        4.  Remove [`poetry.lock`](./poetry.lock) from the project and Git.
    *   **Reasoning:** `uv.lock` is UV's native lock file format, ensuring reproducible builds.

4.  **Address `requirements.txt`:**
    *   **Action:** Remove [`requirements.txt`](./requirements.txt) as [`pyproject.toml`](./pyproject.toml) is the designated source of truth.
    *   **Reasoning:** Simplifies dependency management.

---

## Phase 3: Testing & CI/CD

1.  **Local Testing:**
    *   **Action:**
        1.  Delete any existing `.venv` created by Poetry.
        2.  Run the new `make install` (or equivalent `uv venv && uv sync`).
        3.  Activate the environment: `source .venv/bin/activate`.
        4.  Run `make start` and test other relevant [`Makefile`](./Makefile) targets.
    *   **Reasoning:** Verifies the local development workflow.

2.  **Docker Build & Run Testing:**
    *   **Action:**
        1.  Run `make docker-build` (using the updated [`Dockerfile`](./Dockerfile)).
        2.  Run `make docker-run` and test the application.
    *   **Reasoning:** Ensures containerization works correctly.

3.  **CI/CD Pipeline (`cloudbuild.yaml`):**
    *   **Action:** The changes to the [`Dockerfile`](./Dockerfile) should be automatically picked up by [`cloudbuild.yaml`](./cloudbuild.yaml). Trigger a build in GCP to verify.
    *   **Reasoning:** Confirms automated build and deployment pipeline compatibility.

---

## Phase 4: Cleanup

1.  **Refine `pyproject.toml` to PEP 621 (Optional but Recommended):**
    *   **Action:** If not done earlier, transition `[tool.poetry]` sections in [`pyproject.toml`](./pyproject.toml) to standard `[project]` sections (dependencies, optional-dependencies, etc.) as per PEP 621.
        ```toml
        # Example Structure
        [project]
        name = "startup-template-python"
        version = "0.0.1"
        # ... other metadata
        dependencies = [
            "fastapi[all]==0.110.1",
            # ...
        ]

        [project.optional-dependencies]
        dev = [
            "ruff>=0.9.6",
            # ...
        ]

        # Update build-system if poetry-core is no longer used for building
        [build-system]
        requires = ["hatchling"] # Or another suitable backend
        build-backend = "hatchling.build"
        backend-path = ["."]
        ```
    *   **Reasoning:** Enhances interoperability and adherence to Python standards.

2.  **Update Documentation:**
    *   **Action:** Update `README.md` and any other developer documentation to reflect the use of UV and new setup/usage commands.
    *   **Reasoning:** Ensures project documentation is current and accurate for all developers.

---

## Visual Plan (Mermaid Diagram)

```mermaid
graph TD
    A[Start: Current Poetry Setup] --> C[Remove requirements.txt];
    C --> E[Install UV Locally (User Task)];
    E --> F[Update Makefile: Poetry -> UV commands];
    F --> G[Update Dockerfile: Use UV for deps];
    G --> I[Generate uv.lock, Add to Git, Remove poetry.lock];
    I --> K[Local Testing: New venv, Run app, Test Makefile];
    K --> L[Docker Build & Run Test];
    L --> M[Test CI/CD Pipeline (Cloud Build)];
    M --> N[Cleanup: Refine pyproject.toml to PEP 621 (Optional), Update Docs];
    N --> O[End: Project Migrated to UV];