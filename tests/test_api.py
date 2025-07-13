import unittest
from fastapi.testclient import TestClient
from api import app  # Relative import from parent directory

class TestApi(unittest.TestCase):
    def setUp(self):
        """
        Set up FastAPI test client.
        """
        self.client = TestClient(app)

    def test_infer(self):
        """
        Test the /infer endpoint: y = 2x.

        Sends POST request with input [1, 2, 3, 4].
        Expects output [2, 4, 6, 8].
        """
        response = self.client.post("/infer", json={"input": [1, 2, 3, 4]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"output": [2.0, 4.0, 6.0, 8.0]})

if __name__ == "__main__":
    unittest.main()