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
print('SIGNIFICANT MOVE ANALYSIS')
print('='*70)
print()

# TOP: price should FALL (negative outcome_pips)
# Success = outcome < 0, Significant = outcome < -5

print('[TOP] - Price should fall after detection')
print('-'*50)
cur.execute('''
    SELECT
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE outcome_10m_pips IS NOT NULL) as has_10m,

        -- Any drop
        COUNT(*) FILTER (WHERE outcome_10m_pips < 0) as fell_any,
        -- Fell by more than 5 pips
        COUNT(*) FILTER (WHERE outcome_10m_pips < -5) as fell_gt5,
        -- Fell by more than 10 pips
        COUNT(*) FILTER (WHERE outcome_10m_pips < -10) as fell_gt10,
        -- Fell by more than 20 pips
        COUNT(*) FILTER (WHERE outcome_10m_pips < -20) as fell_gt20,

        -- WRONG direction (price rose)
        COUNT(*) FILTER (WHERE outcome_10m_pips > 0) as rose_wrong,
        COUNT(*) FILTER (WHERE outcome_10m_pips > 5) as rose_gt5_wrong,

        AVG(outcome_10m_pips) as avg_10m
    FROM turning_points
    WHERE turn_type = 'TOP'
''')

row = cur.fetchone()
total, has_10m, fell_any, fell_gt5, fell_gt10, fell_gt20, rose_wrong, rose_gt5_wrong, avg_10m = row

print(f'  Total TOPs detected: {total}')
print(f'  With 10-min outcome: {has_10m}')
print()
print(f'  SUCCESS (price fell):')
print(f'    Fell ANY amount:   {fell_any:3d}/{has_10m:3d} = {100*fell_any/has_10m:5.1f}%')
print(f'    Fell > 5 pips:     {fell_gt5:3d}/{has_10m:3d} = {100*fell_gt5/has_10m:5.1f}%')
print(f'    Fell >10 pips:     {fell_gt10:3d}/{has_10m:3d} = {100*fell_gt10/has_10m:5.1f}%')
print(f'    Fell >20 pips:     {fell_gt20:3d}/{has_10m:3d} = {100*fell_gt20/has_10m:5.1f}%')
print()
print(f'  FAILURE (price rose - wrong direction):')
print(f'    Rose ANY amount:   {rose_wrong:3d}/{has_10m:3d} = {100*rose_wrong/has_10m:5.1f}%')
print(f'    Rose > 5 pips:     {rose_gt5_wrong:3d}/{has_10m:3d} = {100*rose_gt5_wrong/has_10m:5.1f}%')
print()
print(f'  Average 10-min move: {float(avg_10m or 0):+.2f} pips')
print()

# BOTTOM: price should RISE (positive outcome_pips)
# Success = outcome > 0, Significant = outcome > 5

print('[BOTTOM] - Price should rise after detection')
print('-'*50)
cur.execute('''
    SELECT
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE outcome_10m_pips IS NOT NULL) as has_10m,

        -- Any rise
        COUNT(*) FILTER (WHERE outcome_10m_pips > 0) as rose_any,
        -- Rose by more than 5 pips
        COUNT(*) FILTER (WHERE outcome_10m_pips > 5) as rose_gt5,
        -- Rose by more than 10 pips
        COUNT(*) FILTER (WHERE outcome_10m_pips > 10) as rose_gt10,
        -- Rose by more than 20 pips
        COUNT(*) FILTER (WHERE outcome_10m_pips > 20) as rose_gt20,

        -- WRONG direction (price fell)
        COUNT(*) FILTER (WHERE outcome_10m_pips < 0) as fell_wrong,
        COUNT(*) FILTER (WHERE outcome_10m_pips < -5) as fell_gt5_wrong,

        AVG(outcome_10m_pips) as avg_10m
    FROM turning_points
    WHERE turn_type = 'BOTTOM'
''')

row = cur.fetchone()
total, has_10m, rose_any, rose_gt5, rose_gt10, rose_gt20, fell_wrong, fell_gt5_wrong, avg_10m = row

print(f'  Total BOTTOMs detected: {total}')
print(f'  With 10-min outcome: {has_10m}')
print()
print(f'  SUCCESS (price rose):')
print(f'    Rose ANY amount:   {rose_any:3d}/{has_10m:3d} = {100*rose_any/has_10m:5.1f}%')
print(f'    Rose > 5 pips:     {rose_gt5:3d}/{has_10m:3d} = {100*rose_gt5/has_10m:5.1f}%')
print(f'    Rose >10 pips:     {rose_gt10:3d}/{has_10m:3d} = {100*rose_gt10/has_10m:5.1f}%')
print(f'    Rose >20 pips:     {rose_gt20:3d}/{has_10m:3d} = {100*rose_gt20/has_10m:5.1f}%')
print()
print(f'  FAILURE (price fell - wrong direction):')
print(f'    Fell ANY amount:   {fell_wrong:3d}/{has_10m:3d} = {100*fell_wrong/has_10m:5.1f}%')
print(f'    Fell > 5 pips:     {fell_gt5_wrong:3d}/{has_10m:3d} = {100*fell_gt5_wrong/has_10m:5.1f}%')
print()
print(f'  Average 10-min move: {float(avg_10m or 0):+.2f} pips')
print()

# COMBINED summary
print('='*70)
print('COMBINED SUMMARY')
print('='*70)
cur.execute('''
    SELECT
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE outcome_10m_pips IS NOT NULL) as has_10m,

        -- Correct direction (any amount)
        COUNT(*) FILTER (WHERE
            (turn_type = 'TOP' AND outcome_10m_pips < 0) OR
            (turn_type = 'BOTTOM' AND outcome_10m_pips > 0)
        ) as correct_any,

        -- Correct direction > 5 pips
        COUNT(*) FILTER (WHERE
            (turn_type = 'TOP' AND outcome_10m_pips < -5) OR
            (turn_type = 'BOTTOM' AND outcome_10m_pips > 5)
        ) as correct_gt5,

        -- Correct direction > 10 pips
        COUNT(*) FILTER (WHERE
            (turn_type = 'TOP' AND outcome_10m_pips < -10) OR
            (turn_type = 'BOTTOM' AND outcome_10m_pips > 10)
        ) as correct_gt10

    FROM turning_points
''')

total, has_10m, correct_any, correct_gt5, correct_gt10 = cur.fetchone()
print(f'Total turns: {total}')
print(f'With 10-min outcome: {has_10m}')
print()
print(f'10-minute success rates:')
print(f'  Correct direction (any): {correct_any:4d}/{has_10m:4d} = {100*correct_any/has_10m:5.1f}%')
print(f'  Correct > 5 pips:        {correct_gt5:4d}/{has_10m:4d} = {100*correct_gt5/has_10m:5.1f}%')
print(f'  Correct >10 pips:        {correct_gt10:4d}/{has_10m:4d} = {100*correct_gt10/has_10m:5.1f}%')

# Distribution
print()
print('='*70)
print('OUTCOME DISTRIBUTION (10-min)')
print('='*70)

for turn_type in ['TOP', 'BOTTOM']:
    print(f'\n[{turn_type}]')

    if turn_type == 'TOP':
        cur.execute('''
            SELECT
                CASE
                    WHEN outcome_10m_pips IS NULL THEN 'No data'
                    WHEN outcome_10m_pips < -50 THEN 'Fell >50 pips (SUCCESS)'
                    WHEN outcome_10m_pips < -20 THEN 'Fell 20-50 pips (SUCCESS)'
                    WHEN outcome_10m_pips < -10 THEN 'Fell 10-20 pips (SUCCESS)'
                    WHEN outcome_10m_pips < -5 THEN 'Fell 5-10 pips (SUCCESS)'
                    WHEN outcome_10m_pips < 0 THEN 'Fell 0-5 pips (marginal)'
                    WHEN outcome_10m_pips = 0 THEN 'No change'
                    WHEN outcome_10m_pips <= 5 THEN 'Rose 0-5 pips (FAIL)'
                    WHEN outcome_10m_pips <= 10 THEN 'Rose 5-10 pips (FAIL)'
                    ELSE 'Rose >10 pips (FAIL)'
                END as bucket,
                COUNT(*) as count
            FROM turning_points
            WHERE turn_type = 'TOP'
            GROUP BY 1
            ORDER BY MIN(outcome_10m_pips) NULLS FIRST
        ''')
    else:
        cur.execute('''
            SELECT
                CASE
                    WHEN outcome_10m_pips IS NULL THEN 'No data'
                    WHEN outcome_10m_pips > 50 THEN 'Rose >50 pips (SUCCESS)'
                    WHEN outcome_10m_pips > 20 THEN 'Rose 20-50 pips (SUCCESS)'
                    WHEN outcome_10m_pips > 10 THEN 'Rose 10-20 pips (SUCCESS)'
                    WHEN outcome_10m_pips > 5 THEN 'Rose 5-10 pips (SUCCESS)'
                    WHEN outcome_10m_pips > 0 THEN 'Rose 0-5 pips (marginal)'
                    WHEN outcome_10m_pips = 0 THEN 'No change'
                    WHEN outcome_10m_pips >= -5 THEN 'Fell 0-5 pips (FAIL)'
                    WHEN outcome_10m_pips >= -10 THEN 'Fell 5-10 pips (FAIL)'
                    ELSE 'Fell >10 pips (FAIL)'
                END as bucket,
                COUNT(*) as count
            FROM turning_points
            WHERE turn_type = 'BOTTOM'
            GROUP BY 1
            ORDER BY MIN(-outcome_10m_pips) NULLS FIRST
        ''')

    for bucket, count in cur.fetchall():
        print(f'  {bucket:30s}: {count:3d}')

cur.close()
conn.close()
