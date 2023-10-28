from flask import Flask, request, jsonify
import sqlite3

app = Flask('students', __name__)

def connect_to_database():
    try:
        conn = sqlite3.connect('enroll.sqlite')
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

class StudentsResource:
    def post(self):
      try:
        data = request.get_json()
        
        if data:
          conn = connect_to_database()

          if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO students (name, contact_phone, contact_email, contact_address, application_date, application_status, program_course, test_scores, transcripts, recommendation_letters, application_fee_payment_status, application_essays, application_reviewer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (data.get('name'), data.get('contact_phone'), data.get('contact_email'), data.get('contact_address'), data.get('application_date'), data.get('application_status'), data.get('program_course'), data.get('test_scores'), data.get('transcripts'), data.get('recommendation_letters'), data.get('application_fee_payment_status'), data.get('application_essays'), data.get('application_reviewer')))
            conn.commit()
            cursor.execute("SELECT last_insert_rowid()")
            student_id = cursor.fetchone()[0]
            conn.close()
            return jsonify({'message': 'Student inserted successfully', 'student_id': student_id}), 201
          else:
            return jsonify({'message': 'Error connecting to the database'}), 500
        else:
          return jsonify({'error': 'Invalid request data'}), 400
          
      except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    def get(self, student_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
                student = cursor.fetchone()
                conn.close()

                if student:
                    student_info = {
                        'id': student[0],
                        'name': student[1],
                        'contact_phone': student[2],
                        'contact_email': student[3],
                        'contact_address': student[4],
                        'application_date': student[5],
                        'application_status': student[6],
                        'program_course': student[7],
                        'test_scores': student[8],
                        'transcripts': student[9],
                        'recommendation_letters': student[10],
                        'application_fee_payment_status': student[11],
                        'application_essays': student[12],
                        'application_reviewer': student[13]
                    }
                    return jsonify({'student': student_info}), 200
                else:
                    return jsonify({'error': 'Student not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, student_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE students SET name=?, contact_phone=?, contact_email=?, contact_address=?, application_date=?, application_status=?, program_course=?, test_scores=?, transcripts=?, recommendation_letters=?, application_fee_payment_status=?, application_essays=?, application_reviewer=? WHERE id=?',
                                   (data.get('name'), data.get('contact_phone'), data.get('contact_email'), data.get('contact_address'), data.get('application_date'), data.get('application_status'), data.get('program_course'), data.get('test_scores'), data.get('transcripts'), data.get('recommendation_letters'), data.get('application_fee_payment_status'), data.get('application_essays'), data.get('application_reviewer'), student_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Student updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, student_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Student deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

students_resource = StudentsResource()


@app.route('/students/<path:filename>', methods=['GET'])
def get_student(student_id):
    return students_resource.get(student_id)

@app.route('/students/<path:filename>', methods=['PUT'])
def update_student(student_id):
    return students_resource.put(student_id)

@app.route('/students/<path:filename>', methods=['DELETE'])
def delete_student(student_id):
    return students_resource.delete(student_id)

@app.route('/students', methods=['POST'])
def create_student():
  return students_resource.post()

if __name__ == '__main__':
    app.run(debug=True)
