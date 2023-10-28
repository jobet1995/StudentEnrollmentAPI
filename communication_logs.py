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

class CommunicationLogResource:
    def get(self, communication_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM communication_logs WHERE id = ?', (communication_id,))
                communication_log = cursor.fetchone()
                conn.close()

                if communication_log:
                    return jsonify({'communication_log': communication_log}), 200
                else:
                    return jsonify({'error': 'Communication log not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, communication_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE communication_logs SET datetime=?, communication_type=?, communication_content=?, related_to=?, student_id=? WHERE id=?',
                                   (data.get('datetime'), data.get('communication_type'), data.get('communication_content'), data.get('related_to'), data.get('student_id'), communication_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Communication log updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, communication_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM communication_logs WHERE id = ?', (communication_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Communication log deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

communication_log_resource = CommunicationLogResource()

@app.route('/communication-logs/<int:communication_id>', methods=['GET'])
def get_communication_log(communication_id):
    return communication_log_resource.get(communication_id)

@app.route('/communication-logs/<int:communication_id>', methods=['PUT'])
def update_communication_log(communication_id):
    return communication_log_resource.put(communication_id)

@app.route('/communication-logs/<int:communication_id>', methods=['DELETE'])
def delete_communication_log(communication_id):
    return communication_log_resource.delete(communication_id)

if __name__ == '__main__':
    app.run(debug=True)
