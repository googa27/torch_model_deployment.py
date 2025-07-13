# DoubleIt Model Deployment

## Overview

Deploys a PyTorch model that doubles an input tensor: ( y = 2x ), where ( $x \in \mathbb{R}^n$).

Setup

- Python 3.13, PyTorch, Docker Desktop (Windows with WSL2).
- Terraform (binary from https://www.terraform.io/downloads.html, extract to `C:\Terraform`, add to PATH).
- Virtual environment (`env/`) with `requirements.txt`: `torch`, `fastapi`, `uvicorn`.

## Recreating doubleit_model.pt

- Run: `python create_model.py`

## Running Locally

- `python inference.py` outputs `tensor([2, 4, 6, 8])`.

## FastAPI

- Run: `uvicorn api:app --host 0.0.0.0 --port 8000`
- Test: `Invoke-WebRequest -Uri http://localhost:8000/infer -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"input": [1, 2, 3, 4]}'` or `python -m unittest tests/test_api.py`

## Docker

- Build: `docker build -t doubleit-model-api .`
- Run: `docker run -p 8000:8000 doubleit-model-api`

## Unit Tests

- Run: `python -m unittest discover tests`

## CI/CD

- GitHub Actions in `.github/workflows/ci.yml` runs tests on push.

## IaC

- `main.tf` defines Google Cloud Run service (placeholders).
- Terraform installed via binary: `terraform -version`.

## Optional Enhancements

- **Package Manager**: Used `virtualenv` with `requirements.txt`.
- **REST API**: FastAPI in `api.py`: `POST /infer {input: [1,2,3,4]} → {output: [2,4,6,8]}`.
- **Monitoring/Versioning**: Propose MLflow for model versioning and output monitoring.

## Assumptions

- `doubleit_model.pt` recreated from `__torch__.py`.
- Files (`__torch__.py`, `.pkl`) in root; tests in `tests/`.
- `constants.pkl`, `data.pkl`: Likely metadata/sample data, not used in inference.
- No live GCP deployment required.