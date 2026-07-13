from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from api import app
from model_artifact import DEFAULT_MANIFEST, ArtifactManifest


class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_reports_verified_artifact(self):
        manifest = ArtifactManifest.load(DEFAULT_MANIFEST)
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["model"], manifest.name)
        self.assertEqual(payload["framework"], manifest.framework)
        self.assertEqual(payload["sha256"], manifest.sha256)
        self.assertEqual(payload["contract"], manifest.contract)

    def test_infer(self):
        response = self.client.post("/infer", json={"input": [1, 2, 3, 4]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"output": [2.0, 4.0, 6.0, 8.0]})

    def test_rejects_non_finite_input(self):
        response = self.client.post("/infer", json={"input": ["NaN"]})

        self.assertEqual(response.status_code, 422)

    def test_rejects_empty_input(self):
        response = self.client.post("/infer", json={"input": []})

        self.assertEqual(response.status_code, 422)

    def test_rejects_nested_input(self):
        response = self.client.post("/infer", json={"input": [[1, 2]]})

        self.assertEqual(response.status_code, 422)

    def test_rejects_oversized_input(self):
        response = self.client.post("/infer", json={"input": [1] * 1025})

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
