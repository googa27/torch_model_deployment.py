from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_portfolio_architecture_contract() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_portfolio_architecture.py"],
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_model_serving_boundary_is_recorded() -> None:
    contract = json.loads((ROOT / "docs" / "ARCHITECTURE.yaml").read_text())
    forbidden = "\n".join(contract["architecture"]["import_boundaries"]["forbidden"])
    assert "torch.jit.load per request" in forbidden
    assert "SHA-256 verification" in forbidden
    decision = contract["libraries"]["decisions"][0]
    assert decision["capability"] == "model serving demo runtime"
    assert "FastAPI 0.116.1" in decision["selected"]
    assert "PyTorch TorchScript 2.7.1" in decision["selected"]


def test_docker_and_ci_use_manifest_boundary_without_raw_pickle() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "model_artifact.py" in dockerfile
    assert "artifacts/" in dockerfile
    assert not re.search(r"\b(constants|data|.*debug)_?\.pkl\b", dockerfile)
    assert "python -m pytest -q" in ci
    assert "docker build" in ci
