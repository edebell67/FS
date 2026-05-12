from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database Configuration
DB_CONFIG = {
    'dbname': 'bizpa',
    'user': 'postgres',
    'password': 'admin6093',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/api/capture_lead', methods=['GET', 'POST'])
def capture_lead():
    if request.method == 'GET':
        return jsonify({
            'message': 'This endpoint is for lead capture (POST only).',
            'status': 'operational',
            'required_fields': ['email', 'page_id']
        }), 200
    
    data = request.get_json()
    
    if not data or 'email' not in data or 'page_id' not in data:
        return jsonify({'error': 'Missing required fields (email, page_id)'}), 400
    
    email = data.get('email')
    page_id = data.get('page_id')
    pain_point_key = data.get('pain_point_key')
    ip_address = request.remote_addr
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO leads_pain_points (email, page_id, pain_point_key, ip_address)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (email, page_id, pain_point_key, ip_address))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Lead captured successfully'}), 201
    except Exception as e:
        print(f"Error capturing lead: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT page_id, COUNT(*) as count FROM leads_pain_points GROUP BY page_id")
        rows = cur.fetchall()
        stats = {row[0]: row[1] for row in rows}
        cur.close()
        conn.close()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Running on port 5017 to avoid conflicts with existing services
    app.run(host='0.0.0.0', port=5017, debug=True)
