import pyodbc

conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:EDS,1433;Database=tradedb;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)
cur = conn.cursor()

cur.execute("SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_002_pos_buy_sell_count_gbp_tradepoint_signal'))")
row = cur.fetchone()
if row and row[0]:
    print("Found definition! Length:", len(row[0]))
    with open(r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\vw_002_signal.sql", "w", encoding="utf-8") as f:
        f.write(row[0])
    print(row[0][:500])
else:
    print("NOT FOUND in SQL Server!")

conn.close()
