import os
import pyodbc
import time
import random
import json
from datetime import datetime
from itertools import combinations

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
SERVER   = os.getenv("DB_SERVER", "tcp:EDS,1433")
USERNAME = os.getenv("DB_USER", "sqlaccessfromapi")
PASSWORD = os.getenv("DB_PASS", "apiaccess@4321")
DATABASE = "tradedb_sim2"
TABLE_NAME = "[dbo].[fx_quotes]"

JSON_OUTPUT_PATH = r"z:\algo_forex\prices\forex_price_sim.json"
DRIVER = "{ODBC Driver 17 for SQL Server}"

SPREAD = 0.0001
MOVE_RANGE = 0.00005
RECORD_TYPE = "F"

# ─────────────────────────────────────────────
# Initial prices
# ─────────────────────────────────────────────
prices = {
    "gbp": 1.3058,
    "eur": 1.1701,
    "aud": 0.6505,
    "nzd": 0.5050,
}

# ─────────────────────────────────────────────
def get_connection():
    conn_str = (
        f"DRIVER={DRIVER};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )
    return pyodbc.connect(conn_str)

def write_json_snapshot(snapshot):
    with open(JSON_OUTPUT_PATH, "w") as f:
        json.dump(snapshot, f, indent=4)

def generate_combinations(price_snapshot):
    combos = {}
    for a, b in combinations(price_snapshot.keys(), 2):
        name = f"{a}{b}_c"
        combos[name] = {
            "bid": round(price_snapshot[a]["bid"] + price_snapshot[b]["bid"], 6),
            "ask": round(price_snapshot[a]["ask"] + price_snapshot[b]["ask"], 6),
        }
    return combos

# ─────────────────────────────────────────────
def simulate_market_data():
    print("--- FX Simulation Started ---")

    conn = get_connection()
    cursor = conn.cursor()
    print("Database connected.")

    try:
        while True:
            timestamp = datetime.now()

            # base shocks
            shock_gbp_eur = random.uniform(-MOVE_RANGE, MOVE_RANGE)
            shock_aud_nzd = random.uniform(-MOVE_RANGE, MOVE_RANGE)
            shock_eur_aud = random.uniform(-MOVE_RANGE, MOVE_RANGE)

            # correlations
            corr_gbp_eur = random.uniform(0.87, 0.93)
            corr_aud_nzd = random.uniform(0.88, 0.92)
            corr_eur_aud = random.uniform(0.49, 0.51)

            snapshot = {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "prices": {}
            }

            # ── base instruments
            for code in prices.keys():
                independent = random.uniform(-MOVE_RANGE, MOVE_RANGE)

                if code == "gbp":
                    delta = (
                        corr_gbp_eur * shock_gbp_eur +
                        (1 - corr_gbp_eur) * independent
                    )

                elif code == "eur":
                    residual = max(0.0, 1 - corr_gbp_eur - corr_eur_aud)
                    delta = (
                        corr_gbp_eur * shock_gbp_eur +
                        corr_eur_aud * shock_eur_aud +
                        residual * independent
                    )

                elif code == "aud":
                    residual = max(0.0, 1 - corr_aud_nzd - corr_eur_aud)
                    delta = (
                        corr_aud_nzd * shock_aud_nzd +
                        corr_eur_aud * shock_eur_aud +
                        residual * independent
                    )

                elif code == "nzd":
                    delta = (
                        corr_aud_nzd * shock_aud_nzd +
                        (1 - corr_aud_nzd) * independent
                    )

                prices[code] += delta

                bid = round(prices[code] - SPREAD / 2, 6)
                ask = round(prices[code] + SPREAD / 2, 6)

                sql = f"""
                    UPDATE {TABLE_NAME}
                    SET timestamp = ?, bid = ?, ask = ?
                    WHERE code = ? AND type = ?;

                    IF @@ROWCOUNT = 0
                    BEGIN
                        INSERT INTO {TABLE_NAME}
                        (timestamp, code, type, bid, ask)
                        VALUES (?, ?, ?, ?, ?);
                    END
                """

                params = (
                    timestamp, bid, ask, code, RECORD_TYPE,
                    timestamp, code, RECORD_TYPE, bid, ask
                )

                cursor.execute(sql, params)

                snapshot["prices"][code] = {
                    "bid": bid,
                    "ask": ask
                }

                print(f"{code.upper()} | {bid:.6f} / {ask:.6f}")

            # ── synthetic combinations (_c)
            combo_prices = generate_combinations(snapshot["prices"])

            for combo_code, px in combo_prices.items():
                bid, ask = px["bid"], px["ask"]

                sql = f"""
                    UPDATE {TABLE_NAME}
                    SET timestamp = ?, bid = ?, ask = ?
                    WHERE code = ? AND type = ?;

                    IF @@ROWCOUNT = 0
                    BEGIN
                        INSERT INTO {TABLE_NAME}
                        (timestamp, code, type, bid, ask)
                        VALUES (?, ?, ?, ?, ?);
                    END
                """

                params = (
                    timestamp, bid, ask, combo_code, RECORD_TYPE,
                    timestamp, combo_code, RECORD_TYPE, bid, ask
                )

                cursor.execute(sql, params)

                snapshot["prices"][combo_code] = px

                print(f"{combo_code.upper()} | {bid:.6f} / {ask:.6f}")

            conn.commit()
            write_json_snapshot(snapshot)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    finally:
        conn.close()
        print("DB connection closed.")

# ─────────────────────────────────────────────
if __name__ == "__main__":
    simulate_market_data()
