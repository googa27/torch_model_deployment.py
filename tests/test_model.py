from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from create_model import ROOT, build_artifact
from model_artifact import ArtifactManifest, DEFAULT_MANIFEST, DoubleItModelService


class TestModelArtifact(unittest.TestCase):
    def _write_manifest(self, payload: dict[str, object]) -> Path:
        tempdir = TemporaryDirectory(dir=ROOT)
        self.addCleanup(tempdir.cleanup)
        path = Path(tempdir.name) / "test.manifest.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_manifest_verifies_current_artifact(self):
        manifest = ArtifactManifest.load(DEFAULT_MANIFEST)

        manifest.verify()
        self.assertEqual(manifest.name, "doubleit")
        self.assertEqual(manifest.framework, "torchscript")
        self.assertEqual(manifest.input_dtype, "float32")
        self.assertEqual(manifest.output_dtype, "float32")

    def test_service_doubles_input(self):
        service = DoubleItModelService.from_manifest()

        self.assertEqual(service.predict([1, 2, 3, 4]), [2.0, 4.0, 6.0, 8.0])

    def test_manifest_hash_mismatch_is_rejected(self):
        payload = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        payload["sha256"] = "0" * 64
        manifest = ArtifactManifest.load(self._write_manifest(payload))

        with self.assertRaises(ValueError):
            manifest.verify()

    def test_manifest_rejects_artifact_path_escape(self):
        payload = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        payload["artifact_path"] = "../outside.pt"

        with self.assertRaisesRegex(ValueError, "artifact path must stay inside"):
            ArtifactManifest.load(self._write_manifest(payload))

    def test_manifest_rejects_unsupported_framework(self):
        payload = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        payload["framework"] = "pickle"

        with self.assertRaisesRegex(ValueError, "unsupported artifact framework"):
            ArtifactManifest.load(self._write_manifest(payload))

    def test_manifest_rejects_malformed_sha256(self):
        payload = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        payload["sha256"] = "not-a-sha"

        with self.assertRaisesRegex(ValueError, "sha256"):
            ArtifactManifest.load(self._write_manifest(payload))

    def test_manifest_rejects_missing_required_fields(self):
        payload = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        del payload["loader_policy"]

        with self.assertRaisesRegex(ValueError, "missing fields"):
            ArtifactManifest.load(self._write_manifest(payload))

    def test_manifest_path_must_stay_in_repository(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "outside.manifest.json"
            path.write_text(DEFAULT_MANIFEST.read_text(encoding="utf-8"), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "manifest path must stay inside"):
                ArtifactManifest.load(path)

    def test_build_artifact_writes_manifest_with_hash(self):
        with TemporaryDirectory(dir=ROOT) as tmp:
            model_path = Path(tmp) / "doubleit_model.pt"
            manifest_path = Path(tmp) / "doubleit.manifest.json"

            result = build_artifact(model_path=model_path, manifest_path=manifest_path)

            self.assertTrue(model_path.is_file())
            self.assertTrue(manifest_path.is_file())
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["sha256"], result["sha256"])
            self.assertEqual(payload["artifact_path"], model_path.relative_to(ROOT).as_posix())
            self.assertRegex(result["sha256"], r"^[a-f0-9]{64}$")
            ArtifactManifest.load(manifest_path).verify()

    def test_build_artifact_rejects_output_outside_repo(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "model artifact path"):
                build_artifact(model_path=Path(tmp) / "doubleit_model.pt")


if __name__ == "__main__":
    unittest.main()
