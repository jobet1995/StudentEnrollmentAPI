import unittest
from main import app

class TestMainAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_students_api(self):
        response = self.app.get('/students')
        self.assertEqual(response.status_code, 200)

    def test_teachers_api(self):
        response = self.app.get('/teachers')
        self.assertEqual(response.status_code, 200)

    def test_subjects_api(self):
        response = self.app.get('/subjects')
        self.assertEqual(response.status_code, 200)

    def test_programs_courses_api(self):
        response = self.app.get('/programs-courses')
        self.assertEqual(response.status_code, 200)

    def test_enrollments_api(self):
        response = self.app.get('/enrollments')
        self.assertEqual(response.status_code, 200)

    def test_communication_logs_api(self):
        response = self.app.get('/communication-logs')
        self.assertEqual(response.status_code, 200)

    def test_admission_decisions_api(self):
        response = self.app.get('/admission-decisions')
        self.assertEqual(response.status_code, 200)

    def test_prospective_students_api(self):
        response = self.app.get('/prospective-students')
        self.assertEqual(response.status_code, 200)

    def test_events_activities_api(self):
        response = self.app.get('/events-activities')
        self.assertEqual(response.status_code, 200)

    def test_document_management_api(self):
        response = self.app.get('/document-management')
        self.assertEqual(response.status_code, 200)

    def test_users_api(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
