# Verification script for B, S, X trade markers
import urllib.request

url = 'http://localhost:8088/top10_5min_equity_curves.html'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8')
        print(f'HTTP Status: {resp.status}')
        
        has_v = "[V20260920_2331]" in html
        has_compute_signals = "function computeTradeOverlaySignals(" in html
        has_draw_badge = "function drawSignalBadge(" in html
        has_toggle_btn = "id=\"toggleTradeMarkersBtn\"" in html
        has_condition_check = "showTradeMarkers && (showBuyDelta || showSellDelta)" in html

        print(f'Check Version V20260920_2331: {has_v}')
        print(f'Check computeTradeOverlaySignals: {has_compute_signals}')
        print(f'Check drawSignalBadge: {has_draw_badge}')
        print(f'Check toggleTradeMarkersBtn: {has_toggle_btn}')
        print(f'Check only active with buy_net / sell_net: {has_condition_check}')

        assert has_v and has_compute_signals and has_draw_badge and has_toggle_btn and has_condition_check, "Trade marker verification failed!"
        print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")
except Exception as e:
    print('Error:', e)
