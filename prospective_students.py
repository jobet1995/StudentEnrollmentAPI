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

class ProspectiveStudentResource:
    def get(self, prospective_student_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM prospective_students WHERE id = ?', (prospective_student_id,))
                prospective_student = cursor.fetchone()
                conn.close()

                if prospective_student:
                    return jsonify({'prospective_student': prospective_student}), 200
                else:
                    return jsonify({'error': 'Prospective student not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, prospective_student_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE prospective_students SET lead_source=?, lead_qualification_status=?, interests_preferences=?, demographic_information=? WHERE id=?',
                                   (data.get('lead_source'), data.get('lead_qualification_status'), data.get('interests_preferences'), data.get('demographic_information'), prospective_student_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Prospective student updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, prospective_student_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM prospective_students WHERE id = ?', (prospective_student_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Prospective student deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

prospective_student_resource = ProspectiveStudentResource()

@app.route('/prospective-students/<int:prospective_student_id>', methods=['GET'])
def get_prospective_student(prospective_student_id):
    return prospective_student_resource.get(prospective_student_id)

@app.route('/prospective-students/<int:prospective_student_id>', methods=['PUT'])
def update_prospective_student(prospective_student_id):
    return prospective_student_resource.put(prospective_student_id)

@app.route('/prospective-students/<int:prospective_student_id>', methods=['DELETE'])
def delete_prospective_student(prospective_student_id):
    return prospective_student_resource.delete(prospective_student_id)

if __name__ == '__main__':
    app.run(debug=True)
