import pyodbc

conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:EDS,1433;Database=tradedb;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)
cur = conn.cursor()

cur.execute("SELECT config_name, config_value, config_value_unit FROM dbo.config ORDER BY config_name;")
rows = cur.fetchall()
print(f"Fetched {len(rows)} config rows from SQL Server:")
for r in rows[:10]:
    print(f"  {r[0]} = {r[1]} ({r[2]})")

conn.close()
