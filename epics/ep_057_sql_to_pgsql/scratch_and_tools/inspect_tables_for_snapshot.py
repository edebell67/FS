import pyodbc
import psycopg2

ms_conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:EDS,1433;Database=tradedb;Trusted_Connection=yes;')
ms_cur = ms_conn.cursor()

ms_cur.execute("""
    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' 
      AND (TABLE_NAME LIKE '%summary%' OR TABLE_NAME LIKE '%snapshot%' OR TABLE_NAME LIKE '%dna%' OR TABLE_NAME LIKE '%model%')
    ORDER BY TABLE_NAME;
""")
print("SQL Server candidate tables:")
for r in ms_cur.fetchall():
    print(" -", r[0])

# Check product_forex sample row
ms_cur.execute("SELECT TOP 5 model, product, strategy_name, dna_json FROM dbo.product_forex WHERE model LIKE 'DNA%' ORDER BY model;")
print("\nSample product_forex rows in SQL Server:")
for r in ms_cur.fetchall():
    print(f" Model: {r[0]}, Product: {r[1]}, Strategy: {r[2]}, JSON snippet: {str(r[3])[:100]}")

# Check views for combined trades
ms_cur.execute("""
    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS
    WHERE TABLE_NAME LIKE '%combined_trades%'
    ORDER BY TABLE_NAME;
""")
print("\nCombined trades views:")
for r in ms_cur.fetchall():
    print(" -", r[0])

ms_conn.close()
