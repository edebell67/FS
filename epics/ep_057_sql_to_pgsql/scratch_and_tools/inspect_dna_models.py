import pyodbc

ms_conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:EDS,1433;Database=tradedb;Trusted_Connection=yes;')
ms_cur = ms_conn.cursor()

ms_cur.execute("""
    SELECT TOP 10 model, product, strategy_name, dna_json
    FROM dbo.product_forex
    WHERE model LIKE 'DNA_2%'
    ORDER BY model;
""")
print("DNA_2 models sample:")
for r in ms_cur.fetchall():
    print(f" Model: {r[0]}, Strategy: {r[2]}, JSON: {r[3]}")

ms_cur.execute("""
    SELECT TOP 5 model, signal, net_return, alt_net_return, created
    FROM dbo.combined_trades_closed
    WHERE model LIKE 'DNA%'
    ORDER BY created DESC;
""")
print("\nRecent DNA trades in combined_trades_closed:")
for r in ms_cur.fetchall():
    print(f" Model: {r[0]}, Signal: {r[1]}, Net: {r[2]}, Alt: {r[3]}, Created: {r[4]}")

ms_conn.close()
