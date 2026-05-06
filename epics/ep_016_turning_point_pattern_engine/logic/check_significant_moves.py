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

print('='*70)
print('SIGNIFICANT MOVE ANALYSIS (>5 pips threshold)')
print('='*70)
print()

# TOP success = price dropped by more than 5 pips (outcome < -5)
# BOTTOM success = price rose by more than 5 pips (outcome > 5)

for turn_type in ['TOP', 'BOTTOM']:
    direction = '<' if turn_type == 'TOP' else '>'
    sign = -1 if turn_type == 'TOP' else 1

    print(f'[{turn_type}] - Price {"fell" if turn_type == "TOP" else "rose"} by >5 pips')
    print('-'*50)

    cur.execute(f'''
        SELECT
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE outcome_5m_pips IS NOT NULL) as has_5m,
            COUNT(*) FILTER (WHERE outcome_10m_pips IS NOT NULL) as has_10m,

            -- Any move in right direction
            COUNT(*) FILTER (WHERE outcome_5m_pips {direction} 0) as any_5m,
            COUNT(*) FILTER (WHERE outcome_10m_pips {direction} 0) as any_10m,

            -- >5 pip move
            COUNT(*) FILTER (WHERE outcome_5m_pips {direction} {sign * -5}) as gt5_5m,
            COUNT(*) FILTER (WHERE outcome_10m_pips {direction} {sign * -5}) as gt5_10m,

            -- >10 pip move
            COUNT(*) FILTER (WHERE outcome_5m_pips {direction} {sign * -10}) as gt10_5m,
            COUNT(*) FILTER (WHERE outcome_10m_pips {direction} {sign * -10}) as gt10_10m,

            -- >20 pip move
            COUNT(*) FILTER (WHERE outcome_10m_pips {direction} {sign * -20}) as gt20_10m,

            -- Average moves
            AVG(outcome_5m_pips) as avg_5m,
            AVG(outcome_10m_pips) as avg_10m,
            AVG(max_favourable_10m_pips) as avg_max_fav
        FROM turning_points
        WHERE turn_type = %s
    ''', (turn_type,))

    row = cur.fetchone()
    total, has_5m, has_10m, any_5m, any_10m, gt5_5m, gt5_10m, gt10_5m, gt10_10m, gt20_10m, avg_5m, avg_10m, avg_max_fav = row

    print(f'  Total {turn_type}s detected: {total}')
    print()
    print(f'  5-minute outcomes ({has_5m} with data):')
    if has_5m > 0:
        print(f'    Any move correct:  {any_5m:3d}/{has_5m:3d} = {100*any_5m/has_5m:5.1f}%')
        print(f'    > 5 pips:          {gt5_5m:3d}/{has_5m:3d} = {100*gt5_5m/has_5m:5.1f}%')
        print(f'    >10 pips:          {gt10_5m:3d}/{has_5m:3d} = {100*gt10_5m/has_5m:5.1f}%')
    print()
    print(f'  10-minute outcomes ({has_10m} with data):')
    if has_10m > 0:
        print(f'    Any move correct:  {any_10m:3d}/{has_10m:3d} = {100*any_10m/has_10m:5.1f}%')
        print(f'    > 5 pips:          {gt5_10m:3d}/{has_10m:3d} = {100*gt5_10m/has_10m:5.1f}%')
        print(f'    >10 pips:          {gt10_10m:3d}/{has_10m:3d} = {100*gt10_10m/has_10m:5.1f}%')
        print(f'    >20 pips:          {gt20_10m:3d}/{has_10m:3d} = {100*gt20_10m/has_10m:5.1f}%')
    print()
    print(f'  Average moves:')
    print(f'    5 min:  {float(avg_5m or 0):+.2f} pips')
    print(f'    10 min: {float(avg_10m or 0):+.2f} pips')
    print(f'    Max favourable (10m): {float(avg_max_fav or 0):+.2f} pips')
    print()
    print()

# Distribution of outcome sizes
print('='*70)
print('OUTCOME DISTRIBUTION (10-min)')
print('='*70)

for turn_type in ['TOP', 'BOTTOM']:
    print(f'\n[{turn_type}] Outcome distribution:')

    if turn_type == 'TOP':
        # For TOPs, negative outcomes are good (price fell)
        cur.execute('''
            SELECT
                CASE
                    WHEN outcome_10m_pips <= -50 THEN 'Fell >50 pips'
                    WHEN outcome_10m_pips <= -20 THEN 'Fell 20-50 pips'
                    WHEN outcome_10m_pips <= -10 THEN 'Fell 10-20 pips'
                    WHEN outcome_10m_pips <= -5 THEN 'Fell 5-10 pips'
                    WHEN outcome_10m_pips < 0 THEN 'Fell 0-5 pips'
                    WHEN outcome_10m_pips = 0 THEN 'No change'
                    WHEN outcome_10m_pips <= 5 THEN 'Rose 0-5 pips (WRONG)'
                    WHEN outcome_10m_pips <= 10 THEN 'Rose 5-10 pips (WRONG)'
                    ELSE 'Rose >10 pips (WRONG)'
                END as bucket,
                COUNT(*) as count
            FROM turning_points
            WHERE turn_type = 'TOP' AND outcome_10m_pips IS NOT NULL
            GROUP BY bucket
            ORDER BY MIN(outcome_10m_pips)
        ''')
    else:
        # For BOTTOMs, positive outcomes are good (price rose)
        cur.execute('''
            SELECT
                CASE
                    WHEN outcome_10m_pips >= 50 THEN 'Rose >50 pips'
                    WHEN outcome_10m_pips >= 20 THEN 'Rose 20-50 pips'
                    WHEN outcome_10m_pips >= 10 THEN 'Rose 10-20 pips'
                    WHEN outcome_10m_pips >= 5 THEN 'Rose 5-10 pips'
                    WHEN outcome_10m_pips > 0 THEN 'Rose 0-5 pips'
                    WHEN outcome_10m_pips = 0 THEN 'No change'
                    WHEN outcome_10m_pips >= -5 THEN 'Fell 0-5 pips (WRONG)'
                    WHEN outcome_10m_pips >= -10 THEN 'Fell 5-10 pips (WRONG)'
                    ELSE 'Fell >10 pips (WRONG)'
                END as bucket,
                COUNT(*) as count
            FROM turning_points
            WHERE turn_type = 'BOTTOM' AND outcome_10m_pips IS NOT NULL
            GROUP BY bucket
            ORDER BY MIN(-outcome_10m_pips)
        ''')

    for bucket, count in cur.fetchall():
        print(f'    {bucket:25s}: {count:3d}')

cur.close()
conn.close()
