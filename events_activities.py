from flask import Flask, request, jsonify
import sqlite3

app = Flask('event_activities',__name__)

def connect_to_database():
    try:
        conn = sqlite3.connect('enroll.sqlite')
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

class EventsActivitiesResource:
    def get(self, event_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM events_activities WHERE id = ?', (event_id,))
                event = cursor.fetchone()
                conn.close()

                if event:
                    return jsonify({'event': event}), 200
                else:
                    return jsonify({'error': 'Event not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, event_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE events_activities SET event_name=?, event_type=?, attendance_participation=?, follow_up_actions=? WHERE id=?',
                                   (data.get('event_name'), data.get('event_type'), data.get('attendance_participation'), data.get('follow_up_actions'), event_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Event updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, event_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM events_activities WHERE id = ?', (event_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Event deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

events_activities_resource = EventsActivitiesResource()

@app.route('/events-activities/<int:event_id>', methods=['GET'])
def get_event(event_id):
    return events_activities_resource.get(event_id)

@app.route('/events-activities/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    return events_activities_resource.put(event_id)

@app.route('/events-activities/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    return events_activities_resource.delete(event_id)

if __name__ == '__main__':
    app.run(debug=True)
