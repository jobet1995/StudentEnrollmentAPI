from flask import Flask, request, jsonify, send_file
import sqlite3
import json

app = Flask(__name__)

def connect_to_database():
    try:
        conn = sqlite3.connect('enroll.sqlite')
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

@app.route('/students', methods=['GET'])
def get_students():
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
            conn.close()
            return jsonify({'students': students}), 200
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            student = cursor.fetchone()
            conn.close()

            if student:
                return jsonify({'student': student}), 200
            else:
                return jsonify({'error': 'Student not found'}), 404
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-json', methods=['GET'])
def generate_json_file():
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
            conn.close()

            json_data = {'students': students}
            with open('students.json', 'w') as json_file:
                json.dump(json_data, json_file)
            return send_file('students.json', as_attachment=True), 200
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
