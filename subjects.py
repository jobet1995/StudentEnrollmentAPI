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

class SubjectsResource:
    def get(self, subject_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,))
                subject = cursor.fetchone()
                conn.close()

                if subject:
                    subject_info = {
                        'id': subject[0],
                        'subject_name': subject[1],
                        'program_course_id': subject[2],
                        'time': subject[3],
                        'days': subject[4]
                    }
                    return jsonify({'subject': subject_info}), 200
                else:
                    return jsonify({'error': 'Subject not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, subject_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE subjects SET subject_name=?, program_course_id=?, time=?, days=? WHERE id=?',
                                   (data.get('subject_name'), data.get('program_course_id'), data.get('time'), data.get('days'), subject_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Subject updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, subject_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Subject deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

subjects_resource = SubjectsResource()

@app.route('/subjects/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    return subjects_resource.get(subject_id)

@app.route('/subjects/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    return subjects_resource.put(subject_id)

@app.route('/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    return subjects_resource.delete(subject_id)

if __name__ == '__main__':
    app.run(debug=True)
