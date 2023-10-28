from flask import Flask, Blueprint
from students import students_api
from teachers import teachers_api
from subjects import subjects_api
from programs_courses import programs_courses_api
from enrollments import enrollments_api
from communication_logs import communication_logs_api
from admission_decisions import admission_decisions_api
from prospective_students import prospective_students_api
from events_activities import events_activities_api
from document_management import document_management_api
from users import users_api

app = Flask(__name__)

app.register_blueprint(students_api, url_prefix='/students')
app.register_blueprint(teachers_api, url_prefix='/teachers')
app.register_blueprint(subjects_api, url_prefix='/subjects')
app.register_blueprint(programs_courses_api, url_prefix='/programs-courses')
app.register_blueprint(enrollments_api, url_prefix='/enrollments')
app.register_blueprint(communication_logs_api, url_prefix='/communication-logs')
app.register_blueprint(admission_decisions_api, url_prefix='/admission-decisions')
app.register_blueprint(prospective_students_api, url_prefix='/prospective-students')
app.register_blueprint(events_activities_api, url_prefix='/events-activities')
app.register_blueprint(document_management_api, url_prefix='/document-management')
app.register_blueprint(users_api, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)
