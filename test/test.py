import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client()
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"msg": "Welcome to the Flask App!"})  # Validate JSON response

if __name__ == "__main__":
    unittest.main()

