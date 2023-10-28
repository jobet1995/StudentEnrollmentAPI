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

class EnrollmentResource:
    def get(self, enrollment_id):
        try:
            conn = connect_to the database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM enrollments WHERE id = ?', (enrollment_id,))
                enrollment = cursor.fetchone()
                conn.close()

                if enrollment:
                    return jsonify({'enrollment': enrollment}), 200
                else:
                    return jsonify({'error': 'Enrollment not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, enrollment_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE enrollments SET enrollment_date=?, enrollment_status=?, payment_status=?, academic_advisor=?, student_id=? WHERE id=?',
                                   (data.get('enrollment_date'), data.get('enrollment_status'), data.get('payment_status'), data.get('academic_advisor'), data.get('student_id'), enrollment_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Enrollment updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, enrollment_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM enrollments WHERE id = ?', (enrollment_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Enrollment deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

enrollment_resource = EnrollmentResource()

@app.route('/enrollments/<int:enrollment_id>', methods=['GET'])
def get_enrollment(enrollment_id):
    return enrollment_resource.get(enrollment_id)

@app.route('/enrollments/<int:enrollment_id>', methods=['PUT'])
def update_enrollment(enrollment_id):
    return enrollment_resource.put(enrollment_id)

@app.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
def delete_enrollment(enrollment_id):
    return enrollment_resource.delete(enrollment_id)

if __name__ == '__main__':
    app.run(debug=True)
