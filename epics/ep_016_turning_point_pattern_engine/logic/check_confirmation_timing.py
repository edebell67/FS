import psycopg2

conn = psycopg2.connect(
    dbname='pattern_engine',
    user='postgres',
    password='admin6093',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

print('='*70)
print('CONFIRMATION DELAY ANALYSIS')
print('='*70)
print()
print('Outcomes are measured from turn_time (T), but the turn is only')
print('CONFIRMED after price moves 5 pips, which takes X minutes.')
print()

cur.execute('''
    SELECT
        turn_type,
        confirmation_delay_minutes,
        COUNT(*) as count
    FROM turning_points
    WHERE confirmation_delay_minutes IS NOT NULL
    GROUP BY turn_type, confirmation_delay_minutes
    ORDER BY turn_type, confirmation_delay_minutes
''')

print('Confirmation Delay Distribution:')
print('-'*40)
print(f'{"Turn Type":10s} | {"Delay":>8s} | {"Count":>6s}')
print('-'*40)
for turn_type, delay, count in cur.fetchall():
    print(f'{turn_type:10s} | {delay:>6d} min | {count:>6d}')

print()
print('='*70)
print('REMAINING TIME AFTER CONFIRMATION')
print('='*70)
print()
print('If outcome is measured at T+10m, and confirmation happens at T+Xm,')
print('then remaining time to trade = 10 - X minutes')
print()

cur.execute('''
    SELECT
        turn_type,
        confirmation_delay_minutes,
        COUNT(*) as count,

        -- Success rates at different horizons
        ROUND(100.0 * COUNT(*) FILTER (WHERE
            (turn_type = 'TOP' AND outcome_10m_pips < -5) OR
            (turn_type = 'BOTTOM' AND outcome_10m_pips > 5)
        ) / COUNT(*), 1) as success_gt5_10m,

        ROUND(100.0 * COUNT(*) FILTER (WHERE
            (turn_type = 'TOP' AND outcome_15m_pips < -5) OR
            (turn_type = 'BOTTOM' AND outcome_15m_pips > 5)
        ) / COUNT(*), 1) as success_gt5_15m,

        ROUND(AVG(
            CASE WHEN turn_type = 'BOTTOM' THEN outcome_10m_pips
                 ELSE -outcome_10m_pips END
        )::numeric, 2) as avg_fav_10m

    FROM turning_points
    WHERE confirmation_delay_minutes IS NOT NULL
    GROUP BY turn_type, confirmation_delay_minutes
    ORDER BY turn_type, confirmation_delay_minutes
''')

print(f'{"Type":8s} | {"Delay":>5s} | {"Count":>5s} | {">5pip@10m":>10s} | {">5pip@15m":>10s} | {"Avg Fav":>8s}')
print('-'*65)
for turn_type, delay, count, s10, s15, avg in cur.fetchall():
    remaining_10m = max(0, 10 - delay)
    print(f'{turn_type:8s} | {delay:>3d}m  | {count:>5d} | {s10:>9.1f}% | {s15:>9.1f}% | {avg:>+8.2f}')

print()
print('='*70)
print('WHAT THIS MEANS FOR TRADING')
print('='*70)
print()
print('Most turns are confirmed at T+5min (1 snapshot after the turn).')
print('So when trading based on a confirmed turn:')
print('  - outcome_10m_pips = only 5 more minutes of runway')
print('  - outcome_15m_pips = 10 more minutes of runway')
print()

cur.close()
conn.close()
