from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_to_database():
    try:
        conn = sqlite3.connect('enroll.sqlite')
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

class ProgramCourseResource:
    def get(self, program_course_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM program_courses WHERE id = ?', (program_course_id,))
                program_course = cursor.fetchone()
                conn.close()

                if program_course:
                    return jsonify({'program_course': program_course}), 200
                else:
                    return jsonify({'error': 'Program/course not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, program_course_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE program_courses SET program_name=?, application_deadline=?, available_slots=?, program_requirements=? WHERE id=?',
                                   (data.get('program_name'), data.get('application_deadline'), data.get('available_slots'), data.get('program_requirements'), program_course_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Program/course updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, program_course_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM program_courses WHERE id = ?', (program_course_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Program/course deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

program_course_resource = ProgramCourseResource()

@app.route('/program-courses/<int:program_course_id>', methods=['GET'])
def get_program_course(program_course_id):
    return program_course_resource.get(program_course_id)

@app.route('/program-courses/<int:program_course_id>', methods=['PUT'])
def update_program_course(program_course_id):
    return program_course_resource.put(program_course_id)

@app.route('/program-courses/<int:program_course_id>', methods=['DELETE'])
def delete_program_course(program_course_id):
    return program_course_resource.delete(program_course_id)

if __name__ == '__main__':
    app.run(debug=True)
