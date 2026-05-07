import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allow CORS from GitHub Pages and localhost
CORS(app, resources={r"/api/*": {"origins": ["https://edebell67.github.io", "http://localhost:5017", "http://127.0.0.1:5017"]}})

LEADS_FILE = os.path.join(os.path.dirname(__file__), 'leads.json')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/capture_lead', methods=['POST'])
def capture_lead():
    data = request.get_json()
    if not data or 'email' not in data or 'page_id' not in data:
        return jsonify({'error': 'Missing email or page_id'}), 400

    new_lead = {
        'email': data['email'],
        'page_id': data['page_id'],
        'pain_point_key': data.get('pain_point_key'),
        'captured_at': datetime.now().isoformat(),
        'ip_address': request.remote_addr
    }

    try:
        # Read existing leads
        leads = []
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, 'r') as f:
                try:
                    leads = json.load(f)
                except json.JSONDecodeError:
                    leads = []
        
        # Append and save
        leads.append(new_lead)
        with open(LEADS_FILE, 'w') as f:
            json.dump(leads, f, indent=4)
        
        # Optional: In a cloud environment, here we would trigger a 'git commit' 
        # using the GitHub API to fulfill the "hosted in GitHub" requirement.
        
        return jsonify({'message': 'Lead captured in JSON storage'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    if not os.path.exists(LEADS_FILE):
        return jsonify({}), 200
    with open(LEADS_FILE, 'r') as f:
        leads = json.load(f)
    
    stats = {}
    for lead in leads:
        pid = lead['page_id']
        stats[pid] = stats.get(pid, 0) + 1
    return jsonify(stats), 200

if __name__ == '__main__':
    # Use environment PORT or default to 5017
    port = int(os.environ.get('PORT', 5017))
    app.run(host='0.0.0.0', port=port)
