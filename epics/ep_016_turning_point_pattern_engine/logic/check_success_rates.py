import psycopg2

DB_CONFIG = {
    'dbname': 'pattern_engine',
    'user': 'postgres',
    'password': 'admin6093',
    'host': 'localhost',
    'port': '5432',
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Overall success rates
cur.execute('''
    SELECT
        turn_type,
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE outcome_5m_pips IS NOT NULL) as has_5m,
        COUNT(*) FILTER (WHERE outcome_10m_pips IS NOT NULL) as has_10m,

        -- BOTTOM success = price rose (positive pips)
        -- TOP success = price dropped (negative pips)
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_5m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_5m_pips < 0)
        ) as success_5m,
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_10m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_10m_pips < 0)
        ) as success_10m,
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_15m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_15m_pips < 0)
        ) as success_15m,
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_30m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_30m_pips < 0)
        ) as success_30m,

        -- Average moves (direction-adjusted)
        AVG(CASE WHEN turn_type = 'BOTTOM' THEN outcome_5m_pips ELSE -outcome_5m_pips END) as avg_5m_adj,
        AVG(CASE WHEN turn_type = 'BOTTOM' THEN outcome_10m_pips ELSE -outcome_10m_pips END) as avg_10m_adj,
        AVG(max_favourable_10m_pips) as avg_max_fav,
        AVG(max_adverse_10m_pips) as avg_max_adv
    FROM turning_points
    GROUP BY turn_type
    ORDER BY turn_type
''')

print('='*70)
print('TURNING POINT SUCCESS RATES')
print('='*70)
print()

results = cur.fetchall()
for row in results:
    turn_type, total, has_5m, has_10m, success_5m, success_10m, success_15m, success_30m, avg_5m, avg_10m, avg_max_fav, avg_max_adv = row

    print(f'[{turn_type}] Total: {total}')
    print(f'  Success Rate (price moved in expected direction):')
    if has_5m > 0:
        print(f'    5 min:  {success_5m:3d}/{has_5m:3d} = {100*success_5m/has_5m:5.1f}%')
    if has_10m > 0:
        print(f'    10 min: {success_10m:3d}/{has_10m:3d} = {100*success_10m/has_10m:5.1f}%')
        print(f'    15 min: {success_15m:3d}/{has_10m:3d} = {100*success_15m/has_10m:5.1f}%')
        print(f'    30 min: {success_30m:3d}/{has_10m:3d} = {100*success_30m/has_10m:5.1f}%')
    print(f'  Avg Favourable Move (pips):')
    print(f'    5 min:  {float(avg_5m or 0):+.2f}')
    print(f'    10 min: {float(avg_10m or 0):+.2f}')
    print(f'    Max Favourable (10m): {float(avg_max_fav or 0):+.2f}')
    print(f'    Max Adverse (10m):    {float(avg_max_adv or 0):+.2f}')
    print()

# Combined stats
cur.execute('''
    SELECT
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE outcome_5m_pips IS NOT NULL) as has_outcome,
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_5m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_5m_pips < 0)
        ) as success_5m,
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_10m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_10m_pips < 0)
        ) as success_10m,
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_15m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_15m_pips < 0)
        ) as success_15m,
        COUNT(*) FILTER (WHERE
            (turn_type = 'BOTTOM' AND outcome_30m_pips > 0) OR
            (turn_type = 'TOP' AND outcome_30m_pips < 0)
        ) as success_30m
    FROM turning_points
''')
total, has_outcome, success_5m, success_10m, success_15m, success_30m = cur.fetchone()

print('='*70)
print('COMBINED (ALL TURNS)')
print('='*70)
print(f'Total turns detected: {total}')
if has_outcome > 0:
    print(f'  5 min success:  {success_5m:3d}/{has_outcome:3d} = {100*success_5m/has_outcome:5.1f}%')
    print(f'  10 min success: {success_10m:3d}/{has_outcome:3d} = {100*success_10m/has_outcome:5.1f}%')
    print(f'  15 min success: {success_15m:3d}/{has_outcome:3d} = {100*success_15m/has_outcome:5.1f}%')
    print(f'  30 min success: {success_30m:3d}/{has_outcome:3d} = {100*success_30m/has_outcome:5.1f}%')

# By product breakdown
print()
print('='*70)
print('BY PRODUCT')
print('='*70)
cur.execute('''
    SELECT
        p.product_code,
        tp.turn_type,
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE outcome_10m_pips IS NOT NULL) as has_10m,
        COUNT(*) FILTER (WHERE
            (tp.turn_type = 'BOTTOM' AND outcome_10m_pips > 0) OR
            (tp.turn_type = 'TOP' AND outcome_10m_pips < 0)
        ) as success_10m
    FROM turning_points tp
    JOIN products p ON p.product_id = tp.product_id
    WHERE outcome_10m_pips IS NOT NULL
    GROUP BY p.product_code, tp.turn_type
    ORDER BY p.product_code, tp.turn_type
''')

current_product = None
for product_code, turn_type, total, has_10m, success_10m in cur.fetchall():
    if product_code != current_product:
        if current_product is not None:
            print()
        print(f'[{product_code}]')
        current_product = product_code
    if has_10m > 0:
        rate = 100 * success_10m / has_10m
        print(f'  {turn_type:6s}: {success_10m:2d}/{has_10m:2d} = {rate:5.1f}%')

cur.close()
conn.close()
