import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:EDS,1433;Database=tradedb;Trusted_Connection=yes;')
cur = conn.cursor()

cur.execute("""
    SELECT ROUTINE_NAME 
    FROM INFORMATION_SCHEMA.ROUTINES 
    WHERE ROUTINE_NAME LIKE '%combined%snapshot%' OR ROUTINE_NAME LIKE '%snapshot%'
    ORDER BY ROUTINE_NAME;
""")
print("Matching Stored Procedures:")
for r in cur.fetchall():
    print(" -", r[0])

cur.execute("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME LIKE '%combined%snapshot%' OR TABLE_NAME LIKE '%snapshot%'
    ORDER BY TABLE_NAME;
""")
print("\nMatching Tables:")
for r in cur.fetchall():
    print(" -", r[0])

conn.close()
