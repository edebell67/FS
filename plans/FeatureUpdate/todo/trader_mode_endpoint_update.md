# Trader Mode Endpoint Update Checklist

- [ ] Review existing trader mode configuration flow inside Trades/trade_monitor/trade_monitor.py, confirming where config.json is saved and how the RT Config page toggles the value.
- [ ] Introduce a TRADER_MODE_API_MAP plus a load_trader_mode() helper in Trades/simple_trend_trader.py that reads trade_monitor/config.json, defaults to "live", and normalizes casing.
- [ ] Replace the hard-coded API_URL constant with logic that selects the endpoint based on the loaded trader_mode, warning and falling back to LIVE when the config contains an unexpected value.
- [ ] Ensure get_latest_price() (and any startup banner/log output) surfaces which endpoint/mode is currently active for easier troubleshooting.
- [ ] Confirm trade_monitor's config UI clearly indicates the semantics of LIVE vs SIM (LIVE -> tradedb, SIM -> tradedb_sim2) and continues persisting the selection via save_main_config().
- [ ] Ship or update Trades/trade_monitor/config.json with a default of {"trader_mode": "live"} so manual edits have a template and the trader loads without running the monitor first.
- [ ] Test workflow: toggle mode in the monitor UI, rerun simple_trend_trader.py, and verify it points at the expected endpoint in both LIVE and SIM.
