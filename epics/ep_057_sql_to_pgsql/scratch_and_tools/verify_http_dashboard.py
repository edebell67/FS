# Verify HTTP server response
import urllib.request

url = 'http://localhost:8088/top10_5min_equity_curves.html'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8')
        print(f'HTTP Status: {resp.status}')
        has_curr_date = "let currentDate = '2026-09-18';" in html
        has_v = "[V20260920_2136]" in html
        has_dates = "const availableDates" in html
        has_modal = 'id="scenarioModal"' in html
        print(f'Check currentDate default to 2026-09-18: {has_curr_date}')
        print(f'Check Version tag V20260920_2136: {has_v}')
        print(f'Check availableDates exists: {has_dates}')
        print(f'Check Scenario Modal exists: {has_modal}')
        assert has_curr_date and has_v and has_dates and has_modal, "Verification assertion failed!"
        print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")
except Exception as e:
    print('Error:', e)
