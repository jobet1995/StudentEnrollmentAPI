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

class TeachersResource:
    def get(self, teacher_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM teachers WHERE id = ?', (teacher_id,))
                teacher = cursor.fetchone()
                conn.close()

                if teacher:
                    teacher_info = {
                        'id': teacher[0],
                        'teacher_name': teacher[1],
                        'email': teacher[2],
                        'phone_number': teacher[3],
                        'subject_taught_id': teacher[4]
                    }
                    return jsonify({'teacher': teacher_info}), 200
                else:
                    return jsonify({'error': 'Teacher not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, teacher_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE teachers SET teacher_name=?, email=?, phone_number=?, subject_taught_id=? WHERE id=?',
                                   (data.get('teacher_name'), data.get('email'), data.get('phone_number'), data.get('subject_taught_id'), teacher_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Teacher updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, teacher_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM teachers WHERE id = ?', (teacher_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Teacher deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

teachers_resource = TeachersResource()

@app.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    return teachers_resource.get(teacher_id)

@app.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    return teachers_resource.put(teacher_id)

@app.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    return teachers_resource.delete(teacher_id)

if __name__ == '__main__':
    app.run(debug=True)
