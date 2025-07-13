DoubleIt Model Deployment
Overview
Deploys a PyTorch model that doubles an input tensor: ( y = 2x ), where ( x \in \mathbb{R}^n ).
Setup

Python 3.13, PyTorch, Docker Desktop (Windows with WSL2).
requirements.txt: torch

Recreating doubleit_model.pt

doubleit_model.pt missing; recreated with create_model.py:python create_model.py


Fixed NameError in __torch__.py by removing invalid type hint __torch__.Model.

Running Locally

python inference.py outputs tensor([2, 4, 6, 8]).

Docker

Build: docker build -t doubleit-model .
Run: docker run doubleit-model
Note: Ensure Docker Desktop is running with WSL2 backend.

Unit Tests

Run: python -m unittest tests/test_model.py

CI/CD

GitHub Actions in .github/workflows/ci.yml runs tests on push.

IaC

main.tf defines Google Cloud Run service (placeholders).

Assumptions

doubleit_model.pt recreated from __torch__.py.
Files (__torch__.py, .pkl) in root; tests in tests/.
constants.pkl, data.pkl: Likely metadata/sample data, not used in inference.
No live GCP deployment required.

Optional Proposals

Flask REST API: POST /infer {input: [1,2,3,4]} → {output: [2,4,6,8]}.
MLflow for model versioning.
