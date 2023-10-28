from flask import Flask, Blueprint
from students import students
from teachers import teachers
from subjects import subjects
from programs_courses import programs_courses
from enrollments import enrollments
from communication_logs import communication_logs
from admission_decisions import admission_decisions
from prospective_students import prospective_students
from events_activities import events_activities
from document_management import document_management
from users import users

app = Flask(__name__)


app.register_blueprint(students, url_prefix='/students')
app.register_blueprint(teachers, url_prefix='/teachers')
app.register_blueprint(subjects, url_prefix='/subjects')
app.register_blueprint(programs_courses, url_prefix='/programs-courses')
app.register_blueprint(enrollments, url_prefix='/enrollments')
app.register_blueprint(communication_logs, url_prefix='/communication-logs')
app.register_blueprint(admission_decisions, url_prefix='/admission-decisions')
app.register_blueprint(prospective_students, url_prefix='/prospective-students')
app.register_blueprint(events_activities, url_prefix='/events-activities')
app.register_blueprint(document_management, url_prefix='/document-management')
app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
      app.run(debug=True)
