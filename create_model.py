from __future__ import annotations

import hashlib
import json
from pathlib import Path

import torch as tc

from __torch__ import Model

ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = ROOT / "doubleit_model.pt"
DEFAULT_MANIFEST_PATH = ROOT / "artifacts" / "doubleit.manifest.json"


def _relative_repo_path(path: Path, label: str) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside the repository root") from exc


def build_artifact(
    model_path: Path = DEFAULT_MODEL_PATH,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, str]:
    """Build the local TorchScript demo artifact and its explicit manifest."""
    artifact_path = _relative_repo_path(model_path, "model artifact path")
    _relative_repo_path(manifest_path, "manifest path")
    model = Model()
    scripted_model = tc.jit.script(model)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    scripted_model.save(str(model_path))
    digest = hashlib.sha256(model_path.read_bytes()).hexdigest()
    payload = {
        "schema_version": "1.0.0",
        "name": "doubleit",
        "framework": "torchscript",
        "artifact_path": artifact_path,
        "sha256": digest,
        "input_dtype": "float32",
        "output_dtype": "float32",
        "contract": "output = input * 2 for a one-dimensional finite numeric vector",
        "loader_policy": (
            "Load only this local TorchScript artifact after manifest path containment "
            "and SHA-256 verification; do not accept per-request model paths or raw pickle artifacts."
        ),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return {"model_path": str(model_path), "manifest_path": str(manifest_path), "sha256": digest}


if __name__ == "__main__":
    print(build_artifact())
