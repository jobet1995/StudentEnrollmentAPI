from flask import Flask, request, jsonify, send_file
import sqlite3
import json

app = Flask('document_management',__name__)

def connect_to_database():
    try:
        conn = sqlite3.connect('enroll.sqlite')
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

class DocumentManagementResource:
    def get(self, document_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM document_management WHERE id = ?', (document_id,))
                document = cursor.fetchone()
                conn.close()

                if document:
                   
                    file_path = document[2]
                    return send_file(file_path, as_attachment=True), 200
                else:
                    return jsonify({'error': 'Document not found'}), 404
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def put(self, document_id):
        try:
            data = request.get_json()
            if data:
                conn = connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE document_management SET document_name=?, document_type=? WHERE id=?',
                                   (data.get('document_name'), data.get('document_type'), document_id))
                    conn.commit()
                    conn.close()
                    return jsonify({'message': 'Document updated successfully'}), 200
                else:
                    return jsonify({'error': 'Database connection failed'}), 500
            else:
                return jsonify({'error': 'Invalid request data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, document_id):
        try:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM document_management WHERE id = ?', (document_id,))
                conn.commit()
                conn.close()
                return jsonify({'message': 'Document deleted successfully'}), 200
            else:
                return jsonify({'error': 'Database connection failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

document_management_resource = DocumentManagementResource()

@app.route('/document-management/<int:document_id>', methods=['GET'])
def get_document(document_id):
    return document_management_resource.get(document_id)

@app.route('/document-management/<int:document_id>', methods=['PUT'])
def update_document(document_id):
    return document_management_resource.put(document_id)

@app.route('/document-management/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    return document_management_resource.delete(document_id)

if __name__ == '__main__':
    app.run(debug=True)
