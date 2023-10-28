import unittest
from main import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_students(self):
        response = self.app.get('/students')
        self.assertEqual(response.status_code, 200)

    def test_get_student(self):
        response = self.app.get('/students/1')
        self.assertEqual(response.status_code, 404)

    def test_get_student_not_found(self):
        response = self.app.get('/students/999')
        self.assertEqual(response.status_code, 404)

    def test_generate_json_file(self):
        response = self.app.get('/generate-json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
