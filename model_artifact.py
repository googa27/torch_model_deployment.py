from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch

ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "artifacts" / "doubleit.manifest.json"
_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
_REQUIRED_FIELDS = {
    "schema_version",
    "name",
    "framework",
    "artifact_path",
    "sha256",
    "input_dtype",
    "output_dtype",
    "contract",
    "loader_policy",
}


def _require_under_root(path: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside the repository root") from exc
    return resolved


@dataclass(frozen=True)
class ArtifactManifest:
    schema_version: str
    name: str
    framework: str
    artifact_path: Path
    sha256: str
    input_dtype: str
    output_dtype: str
    contract: str
    loader_policy: str

    @classmethod
    def load(cls, path: Path = DEFAULT_MANIFEST) -> "ArtifactManifest":
        manifest_path = _require_under_root(path, "artifact manifest path")
        if not manifest_path.is_file():
            raise FileNotFoundError(f"artifact manifest not found: {manifest_path}")
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("artifact manifest must be a JSON object")
        missing = _REQUIRED_FIELDS - set(payload)
        if missing:
            raise ValueError(f"artifact manifest missing fields: {sorted(missing)}")

        schema_version = str(payload["schema_version"])
        framework = str(payload["framework"])
        sha256 = str(payload["sha256"])
        input_dtype = str(payload["input_dtype"])
        output_dtype = str(payload["output_dtype"])
        loader_policy = str(payload["loader_policy"])
        if schema_version != "1.0.0":
            raise ValueError(f"unsupported artifact manifest schema: {schema_version}")
        if framework != "torchscript":
            raise ValueError(f"unsupported artifact framework: {framework}")
        if not _SHA256_RE.fullmatch(sha256):
            raise ValueError("artifact sha256 must be 64 lowercase hexadecimal characters")
        if input_dtype != "float32" or output_dtype != "float32":
            raise ValueError("doubleit artifact contract requires float32 input/output dtype")
        if "raw pickle" not in loader_policy.lower():
            raise ValueError("loader policy must explicitly forbid raw pickle artifacts")

        artifact_value = Path(str(payload["artifact_path"]))
        artifact_path = artifact_value if artifact_value.is_absolute() else ROOT / artifact_value
        artifact_path = _require_under_root(artifact_path, "artifact path")
        return cls(
            schema_version=schema_version,
            name=str(payload["name"]),
            framework=framework,
            artifact_path=artifact_path,
            sha256=sha256,
            input_dtype=input_dtype,
            output_dtype=output_dtype,
            contract=str(payload["contract"]),
            loader_policy=loader_policy,
        )

    def verify(self) -> None:
        digest = hashlib.sha256(self.artifact_path.read_bytes()).hexdigest()
        if digest != self.sha256:
            raise ValueError(
                f"artifact hash mismatch for {self.artifact_path.name}: {digest} != {self.sha256}"
            )

    def health_payload(self) -> dict[str, str]:
        return {
            "model": self.name,
            "framework": self.framework,
            "sha256": self.sha256,
            "contract": self.contract,
        }


class DoubleItModelService:
    """Safe inference boundary: one verified local artifact, loaded once."""

    def __init__(self, manifest: ArtifactManifest, module: Any):
        self.manifest = manifest
        self._module = module
        self._module.eval()

    @classmethod
    def from_manifest(cls, path: Path = DEFAULT_MANIFEST) -> "DoubleItModelService":
        manifest = ArtifactManifest.load(path)
        manifest.verify()
        module = torch.jit.load(str(manifest.artifact_path), map_location="cpu")
        return cls(manifest=manifest, module=module)

    def predict(self, values: list[float]) -> list[float]:
        tensor = torch.tensor(values, dtype=torch.float32)
        with torch.inference_mode():
            output = self._module(tensor)
        return [float(value) for value in output.tolist()]
