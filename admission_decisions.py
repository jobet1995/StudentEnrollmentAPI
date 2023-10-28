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

@app.route('/admission-decisions', methods=['GET'])
def get_admission_decisions():
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM admission_decisions')
            decisions = cursor.fetchall()
            conn.close()
            return jsonify({'admission_decisions': decisions}), 200
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admission-decisions/<int:decision_id>', methods=['GET'])
def get_admission_decision(decision_id):
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM admission_decisions WHERE id = ?', (decision_id,))
            decision = cursor.fetchone()
            conn.close()

            if decision:
                return jsonify({'admission_decision': decision}), 200
            else:
                return jsonify({'error': 'Admission decision not found'}), 404
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admission-decisions', methods=['POST'])
def create_admission_decision():
    try:
        data = request.get_json()
        if data:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO admission_decisions (decision_date, admission_decision, financial_aid_offered, scholarships_awarded, notes_comments) VALUES (?, ?, ?, ?, ?)',
                               (data.get('decision_date'), data.get('admission_decision'), data.get('financial_aid_offered'), data.get('scholarships_awarded'), data.get('notes_comments')))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Admission decision created successfully'}), 201
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        else:
            return jsonify({'error': 'Invalid request data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admission-decisions/<int:decision_id>', methods=['PUT'])
def update_admission_decision(decision_id):
    try:
        data = request.get_json()
        if data:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE admission_decisions SET decision_date=?, admission_decision=?, financial_aid_offered=?, scholarships_awarded=?, notes_comments=? WHERE id=?',
                               (data.get('decision_date'), data.get('admission_decision'), data.get('financial_aid_offered'), data.get('scholarships_awarded'), data.get('notes_comments'), decision_id))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Admission decision updated successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        else:
            return jsonify({'error': 'Invalid request data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admission-decisions/<int:decision_id>', methods=['DELETE'])
def delete_admission_decision(decision_id):
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM admission_decisions WHERE id = ?', (decision_id,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Admission decision deleted successfully'}), 200
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)