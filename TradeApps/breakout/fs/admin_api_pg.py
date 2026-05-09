from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
from db_utils import fetch_all, fetch_one, execute_query
import subprocess

# [V20260306_0430] PostgreSQL Admin API Implementation

app = Flask(__name__)
CORS(app)

ROOT_PATH = Path(__file__).resolve().parent
ADMIN_UI_PATH = ROOT_PATH / "admin"

if not ADMIN_UI_PATH.exists():
    os.makedirs(ADMIN_UI_PATH)

@app.route('/admin/')
@app.route('/admin/<path:path>')
def serve_admin_ui(path='index.html'):
    return send_from_directory(str(ADMIN_UI_PATH), path)

# --- CONFIG ENDPOINTS ---

@app.route('/api/admin/config', methods=['GET'])
def get_config():
    rows = fetch_all("SELECT config_name, config_value, config_value_unit FROM config ORDER BY config_name")
    return jsonify(rows)

@app.route('/api/admin/config', methods=['PUT'])
def update_config():
    data = request.json
    name = data.get('config_name')
    val = data.get('config_value')
    if not name:
        return jsonify({"error": "config_name required"}), 400
    
    execute_query("UPDATE config SET config_value = %s WHERE config_name = %s", (val, name), commit=True)
    return jsonify({"success": True})

# --- PRODUCT ENDPOINTS ---

@app.route('/api/admin/products', methods=['GET'])
def get_products():
    rows = fetch_all("SELECT * FROM product_forex ORDER BY product, model")
    return jsonify(rows)

@app.route('/api/admin/products', methods=['POST', 'PUT'])
def save_product():
    data = request.json
    model = data.get('model')
    if not model:
        return jsonify({"error": "model required"}), 400
    
    # Simple upsert logic
    cols = []
    vals = []
    for k, v in data.items():
        cols.append(k)
        vals.append(v)
    
    placeholders = ", ".join(["%s"] * len(cols))
    col_names = ", ".join(cols)
    update_clause = ", ".join([f"{c} = EXCLUDED.{c}" for c in cols if c != 'model'])
    
    query = f"""
        INSERT INTO product_forex ({col_names}) 
        VALUES ({placeholders})
        ON CONFLICT (model) DO UPDATE SET {update_clause}
    """
    execute_query(query, tuple(vals), commit=True)
    return jsonify({"success": True})

# --- SUMMARY DASHBOARD ENDPOINT ---

@app.route('/api/admin/summary', methods=['GET'])
def get_summary():
    # Grouped as: product, model, strategy_name, signal, trade_status
    # Providing: net_return, alt_net_return, trade_count
    query = """
        SELECT 
            product, 
            model, 
            strategy_name, 
            signal, 
            trade_status,
            SUM(net_return) as total_net,
            SUM(alt_net_return) as total_alt_net,
            COUNT(*) as trade_count
        FROM vw_113_combined_trades_all
        GROUP BY product, model, strategy_name, signal, trade_status
        ORDER BY product, model, strategy_name, signal, trade_status
    """
    rows = fetch_all(query)
    return jsonify(rows)

# --- DNA GENERATION ---

@app.route('/api/admin/dna/generate', methods=['POST'])
def generate_dna():
    data = request.json
    product = data.get('product')
    if not product:
        return jsonify({"error": "product required"}), 400
    
    # This triggers the existing DNA generation script in the background
    # We use the advanced forex signal generator detected earlier
    script_path = r"C:\Users\edebe\eds\advanced_forex_signal_generator.py"
    try:
        subprocess.Popen(['python', script_path, '--product', product])
        return jsonify({"success": True, "message": f"DNA generation started for {product}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = 5052
    print(f"PostgreSQL Admin API running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
