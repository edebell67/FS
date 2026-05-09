import pyodbc
import time
import logging
from datetime import datetime

# [V20260126_1010] Background Service for DNA P&L Cache Refresh

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

SERVER = "tcp:EDS,1433"
DATABASE = "tradedb"
USERNAME = "sqlaccessfromapi"
PASSWORD = "apiaccess@4321"
INTERVAL = 60 # Refresh every 60 seconds

def connect_to_db():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};DATABASE={DATABASE};"
        f"UID={USERNAME};PWD={PASSWORD}"
    )
    return pyodbc.connect(conn_str)

def main():
    logging.info("Starting DNA P&L Cache Refresh Service...")
    while True:
        try:
            logging.info("Refreshing cache via sp_refresh_dna_pnl_cache...")
            start_time = time.time()
            
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("{CALL dbo.sp_refresh_dna_pnl_cache}")
            conn.commit()
            conn.close()
            
            duration = time.time() - start_time
            logging.info(f"✅ Cache refresh complete. Took {duration:.2f}s")
            
        except Exception as e:
            logging.error(f"❌ Error refreshing cache: {e}")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
