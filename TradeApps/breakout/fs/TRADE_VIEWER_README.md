# Breakout Trade Viewer

A modern, interactive web dashboard for viewing and analyzing trades from all breakout strategy scripts.

## Features

✨ **Summary View**
- Aggregates trades by app name and strategy parameters
- Groups by direction (BUY/SELL) and status (OPEN/CLOSED)
- Shows Net P&L and Alt Net for each group
- Real-time performance metrics

🔍 **Drill-Down Capability**
- Click any strategy card to view detailed trade listClick any strategy card to view detailed trade list
- Complete trade information including entry/exit prices, timestamps, and P&L

📊 **Statistics Dashboard**
- Total Net P&L
- Total Alt Net P&L
- Open vs Closed trade counts
- Strategy-specific performance

## Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors
```

### 2. Start the API Server

```bash
cd C:\Users\edebe\eds\TradeApps\breakout
python trade_viewer_api.py
```

You should see:
```
🚀 Starting Breakout Trade Viewer API Server...
📁 Trade data path: C:\Users\edebe\eds\TradeApps\breakout\json
🌐 Server running at: http://localhost:5000
```

### 3. Open the Viewer

Open `trade_viewer.html` in your web browser:
```bash
start trade_viewer.html
```

Or simply double-click the file in Windows Explorer.

### 4. Load Trades

1. Select **Run Mode** (Live or Simulation)
2. Select **Date** (defaults to today)
3. Optionally filter by **Strategy**
4. Click **📊 Load Trades**

### 5. Configure Multiple Window Sizes

All breakout scripts read `config.json`. You can now supply either a single integer or a list for `window_size`:

```json
"window_size": [2, 3]
```

Each value runs as a separate in-process strategy (`breakout_2`, `breakout_3`, etc.) while sharing every other parameter. This keeps output JSON/tradeable files isolated per variation.

Profitability guardrails are also centralized in `config.json` under `"profitability_guard"` with `mode`, `threshold_y`, and `count_x` fields (`all_time`, `today`, or `recent_x`). All strategies honor the same guard settings when deciding whether to emit live orders.

## Directory Structure

The viewer expects JSON files in this structure:
```
C:\Users\edebe\eds\TradeApps\breakout\json\
├── live\
│   └── 2025-12-12\
│       ├── breakout_20251212_121637_5_0.0001_10.0_6.0.json
│       ├── breakout_R_20251212_103310_5_0.0001_10.0_6.0.json
│       └── ...
└── sim\
    └── 2025-12-12\
        ├── breakout_Rev_20251212_224823_5_0.0001_10.0_6.0.json
        └── ...
```

## Strategy Grouping

Trades are grouped by:
- **App Name**: `breakout`, `breakout_R`, `breakout_Rev`, `breakout_R_Rev`
- **Strategy Parameters**: `{window_size}_{pip_buffer}_{tp_pips}_{sl_pips}`

Example: `breakout - {5_0.0001_10.0_6.0}`

## Understanding the Display

Each strategy card shows:

```
breakout - {5_0.0001_10.0_6.0}
├── 📈 BUY
│   ├── Closed: Net: $150.00 | Alt: -$75.00 (5 trades)
│   └── Open: Net: $25.00 | Alt: -$10.00 (2 trades)
└── 📉 SELL
    ├── Closed: Net: -$50.00 | Alt: $30.00 (3 trades)
    └── Open: Net: $10.00 | Alt: -$5.00 (1 trade)
```

### Color Coding

- **Green** = Positive P&L
- **Red** = Negative P&L
- **Yellow** = Open trades
- **Gray** = Closed trades

## Features & Controls

### Auto Refresh
Click **🔄 Auto Refresh** to automatically reload trades every 10 seconds. Great for monitoring live trading sessions.

### Drill-Down Modal
Click on any strategy card to view:
- Individual trade details
- Complete trade history
- Sortable columns
- Entry/exit prices and timestamps
- Gross P&L in pips
- Net and Alt Net returns

### Filtering
- **Run Mode**: Switch between live and simulated trades
- **Date**: View trades from any historical date
- **Strategy**: Filter to specific strategy scripts

## API Endpoints

The backend API provides:

- `GET /api/trades?mode={live|sim}&date={YYYY-MM-DD}&strategy={app_name}`
  - Returns all trades for the specified criteria

- `GET /api/dates?mode={live|sim}`
  - Returns available dates with trade data

- `GET /api/health`
  - Health check endpoint

## Troubleshooting

### "Error loading trades"

Make sure:
1. The API server is running (`python trade_viewer_api.py`)
2. The JSON files exist in the expected directory structure
3. The date has trading data
4. Your browser allows local API calls (CORS)

### No trades found

- Check that JSON files exist for the selected date and mode
- Try changing the date or run mode
- Verify the directory path in `trade_viewer_api.py`

### API Server Won't Start

- Ensure Flask is installed: `pip install flask flask-cors`
- Check if port 5000 is available
- Review console output for error messages

## Advanced Usage

### Custom Port

Edit `trade_viewer_api.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # Change port
```

Then update the API URL in `trade_viewer.html`:
```javascript
const apiUrl = `http://localhost:8080/api/trades?...`;  // Match port
```

### Network Access

To access from other devices on your network:
1. Use your machine's IP address instead of `localhost`
2. Update the fetch URL in `trade_viewer.html`
3. Ensure firewall allows incoming connections on port 5000

## Tips

- 💡 Use **Auto Refresh** during live trading sessions
- 💡 Compare live vs sim performance for the same date
- 💡 Group by strategy parameters to find optimal settings
- 💡 Monitor Alt Net to see what opposite trades would have yielded

## Support

For issues or questions:
- Check the browser console (F12) for JavaScript errors
- Review the API server console output
- Verify JSON file format matches expected structure

---

**Created**: 2025-12-12  
**Version**: 1.0
