from flask import Flask, request, jsonify
import sqlite3

app = Flask('users',__name__)

def connect_to_database():
    try:
        conn = sqlite3.connect('enroll.sqlite')
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

class UsersResource:
    def get(self, user_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
                user = cursor.fetchone()
                conn.close()

                if user:
                    # Remove sensitive data (e.g., password) before returning the user information.
                    user_info = {
                        'id': user[0],
                        'uname': user[1],
                        'email': user[3]
                    }
                    return jsonify({'user': user_info}), 200
                else:
                    return jsonify({'error': 'User not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, user_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE Users SET uname=?, pword=?, email=? WHERE id=?',
                                   (data.get('uname'), data.get('pword'), data.get('email'), user_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'User updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, user_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

users_resource = UsersResource()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return users_resource.get(user_id)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return users_resource.put(user_id)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return users_resource.delete(user_id)

if __name__ == '__main__':
    app.run(debug=True)
