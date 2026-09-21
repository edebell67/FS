import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:EDS,1433;Database=tradedb;Trusted_Connection=yes;')
cur = conn.cursor()

cur.execute("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME LIKE '%tbl_dna%' OR TABLE_NAME LIKE '%5min%' OR TABLE_NAME LIKE '%snapshot%'
    ORDER BY TABLE_NAME;
""")
print("Existing matching tables in SQL Server:")
for r in cur.fetchall():
    print(" -", r[0])

conn.close()
