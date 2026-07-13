# Dockerfile
# This Dockerfile sets up a Python environment for running the doubleit model API.
FROM python:3.13-slim
WORKDIR /app
# Install python dependencies
# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Copy the application code, checked-in TorchScript artifact, and manifest.
COPY inference.py create_model.py model_artifact.py doubleit_model.pt __torch__.py api.py /app/
COPY artifacts/ /app/artifacts/
# Copy repository contracts used by the architecture tests.
COPY Dockerfile AGENTS.md /app/
COPY docs/ /app/docs/
COPY scripts/ /app/scripts/
COPY .github/ /app/.github/
COPY tests/ /app/tests/
# Expose the port for the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]