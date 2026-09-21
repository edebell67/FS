from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
import os
import json
from datetime import date, datetime
from pathlib import Path
from db_utils import fetch_all, fetch_one, execute_query
import subprocess

# [V20260306_0450] PostgreSQL Admin API with Robust Serialization

app = Flask(__name__)
CORS(app)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

def json_response(data):
    return Response(
        json.dumps(data, cls=DateTimeEncoder),
        mimetype='application/json'
    )

ROOT_PATH = Path(__file__).resolve().parent
ADMIN_UI_PATH = ROOT_PATH / "admin"

@app.route('/admin/')
@app.route('/admin/<path:path>')
def serve_admin_ui(path='index.html'):
    return send_from_directory(str(ADMIN_UI_PATH), path)

# --- CONFIG ENDPOINTS ---

@app.route('/api/admin/config', methods=['GET'])
def get_config():
    rows = fetch_all("SELECT config_name, config_value, config_value_unit FROM config ORDER BY config_name")
    return json_response(rows)

@app.route('/api/admin/config', methods=['PUT'])
def update_config():
    data = request.json
    name = data.get('config_name')
    val = data.get('config_value')
    execute_query("UPDATE config SET config_value = %s WHERE config_name = %s", (val, name), commit=True)
    return json_response({"success": True})

# --- PRODUCT ENDPOINTS ---

@app.route('/api/admin/products', methods=['GET'])
def get_products():
    rows = fetch_all("SELECT * FROM product_forex ORDER BY product, model")
    return json_response(rows)

@app.route('/api/admin/products', methods=['POST', 'PUT'])
def save_product():
    data = request.json
    model = data.get('model')
    cols = []
    vals = []
    for k, v in data.items():
        cols.append(k); vals.append(v)
    placeholders = ", ".join(["%s"] * len(cols))
    col_names = ", ".join(cols)
    update_clause = ", ".join([f"{c} = EXCLUDED.{c}" for c in cols if c != 'model'])
    query = f"INSERT INTO product_forex ({col_names}) VALUES ({placeholders}) ON CONFLICT (model) DO UPDATE SET {update_clause}"
    execute_query(query, tuple(vals), commit=True)
    return json_response({"success": True})

# --- SUMMARY ENDPOINTS ---

@app.route('/api/admin/summary/performance', methods=['GET'])
def get_performance_summary():
    # Force query arc table directly for debugging
    query = """
        SELECT 
            DATE(t.created) as trade_date,
            t.product, 
            COALESCE(pf.strategy_name, 'No Strategy') as strategy,
            SUM(t.net_return) as total_net,
            COUNT(*) as trade_count,
            SUM(CASE WHEN UPPER(t.signal) = 'BUY' THEN t.net_return ELSE 0 END) as buy_net,
            COUNT(CASE WHEN UPPER(t.signal) = 'BUY' THEN 1 END) as buy_count,
            CASE WHEN COUNT(CASE WHEN UPPER(t.signal) = 'BUY' THEN 1 END) > 0 
                 THEN (COUNT(CASE WHEN UPPER(t.signal) = 'BUY' AND t.net_return > 0 THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN UPPER(t.signal) = 'BUY' THEN 1 END), 0))
                 ELSE 0 END as buy_perc_profitable,
            SUM(CASE WHEN UPPER(t.signal) = 'BUY' THEN t.alt_net_return ELSE 0 END) as alt_net_buy,
            SUM(CASE WHEN UPPER(t.signal) = 'SELL' THEN t.net_return ELSE 0 END) as sell_net,
            COUNT(CASE WHEN UPPER(t.signal) = 'SELL' THEN 1 END) as sell_count,
            CASE WHEN COUNT(CASE WHEN UPPER(t.signal) = 'SELL' THEN 1 END) > 0 
                 THEN (COUNT(CASE WHEN UPPER(t.signal) = 'SELL' AND t.net_return > 0 THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN UPPER(t.signal) = 'SELL' THEN 1 END), 0))
                 ELSE 0 END as sell_perc_profitable,
            SUM(CASE WHEN UPPER(t.signal) = 'SELL' THEN t.alt_net_return ELSE 0 END) as alt_net_sell
        FROM combined_trades_closed_arc t
        LEFT JOIN product_forex pf ON t.model = pf.model
        GROUP BY DATE(t.created), t.product, pf.strategy_name
        ORDER BY trade_date DESC, total_net DESC
        LIMIT 1000
    """
    rows = fetch_all(query)
    return json_response(rows)

@app.route('/api/admin/summary/stats', methods=['GET'])
def get_summary_stats():
    include_history = request.args.get('all', 'false').lower() == 'true'
    source = "vw_113_combined_trades_all"
    if include_history:
        source = f"(SELECT net_return, alt_net_return FROM {source} UNION ALL SELECT net_return, alt_net_return FROM combined_trades_closed_arc)"
    query = f"SELECT SUM(net_return) as total_net, SUM(alt_net_return) as total_alt_net, COUNT(*) as trade_count FROM {source}"
    row = fetch_one(query)
    return json_response(row)

@app.route('/api/admin/summary/hierarchical', methods=['GET'])
def get_hierarchical_summary():
    source = "combined_trades_closed_arc" # Use arc by default for testing
    query = f"""
        SELECT 
            COALESCE(DATE(created)::TEXT, 'ALL DATES') as trade_date,
            COALESCE(product, 'TOTAL') as product,
            COALESCE(strategy_name, 'ALL STRATEGIES') as strategy_name,
            COALESCE(model, 'ALL MODELS') as model,
            COALESCE(signal, 'BOTH') as signal,
            COALESCE(trade_status, 'ALL') as trade_status,
            SUM(net_return) as total_net,
            SUM(alt_net_return) as total_alt_net,
            COUNT(*) as trade_count
        FROM {source} t
        LEFT JOIN product_forex pf ON t.model = pf.model
        GROUP BY ROLLUP(DATE(created), product, strategy_name, model, signal, trade_status)
        HAVING COUNT(*) > 0
        ORDER BY trade_date DESC, product, strategy_name, model, signal, trade_status
    """
    rows = fetch_all(query)
    return json_response(rows)

# --- DNA GENERATION ---

@app.route('/api/admin/dna/generate', methods=['POST'])
def generate_dna():
    data = request.json
    product = data.get('product')
    script_path = r"C:\Users\edebe\eds\advanced_forex_signal_generator.py"
    subprocess.Popen(['python', script_path, '--product', product])
    return json_response({"success": True, "message": f"DNA generation started for {product}"})

if __name__ == "__main__":
    port = 5052
    print(f"PostgreSQL Admin API running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
