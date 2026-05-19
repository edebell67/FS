import psycopg2

conn = psycopg2.connect(
    dbname='pattern_engine',
    user='postgres',
    password='admin6093',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

print('='*50)
print('DATA MODE ANALYSIS')
print('='*50)

# Check frequency_snapshots market_mode
cur.execute('''
    SELECT market_mode, COUNT(*)
    FROM frequency_snapshots
    GROUP BY market_mode
''')
print('\nFrequency Snapshots by Mode:')
for mode, count in cur.fetchall():
    print(f'  {mode or "NULL"}: {count}')

# Check if turning_points have mode info
cur.execute('''
    SELECT
        fs.market_mode,
        COUNT(DISTINCT tp.turn_id) as turns
    FROM turning_points tp
    JOIN turning_point_windows tpw ON tpw.turn_id = tp.turn_id
    JOIN frequency_snapshots fs ON fs.snapshot_id = tpw.snapshot_id
    GROUP BY fs.market_mode
''')
print('\nTurning Points by Snapshot Mode:')
for mode, count in cur.fetchall():
    print(f'  {mode or "NULL"}: {count}')

# Check date range
cur.execute('''
    SELECT MIN(turn_time), MAX(turn_time), COUNT(*)
    FROM turning_points
''')
min_t, max_t, total = cur.fetchone()
print(f'\nTurning Points Date Range:')
print(f'  From: {min_t}')
print(f'  To:   {max_t}')
print(f'  Total: {total}')

cur.close()
conn.close()
