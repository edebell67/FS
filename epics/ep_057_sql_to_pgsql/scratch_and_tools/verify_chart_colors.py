# Verification script for chart color convention
import urllib.request

url = 'http://localhost:8088/top10_5min_equity_curves.html'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8')
        print(f'HTTP Status: {resp.status}')
        
        has_v = "[V20260920_2309]" in html
        has_green_buy = "'#10b981'" in html
        has_red_sell = "'#ef4444'" in html
        has_blue_net = "'#0284c7'" in html
        has_delta_blue = "Total Net (Blue)" in html
        has_delta_green = "Buy Net (Green)" in html
        has_delta_red = "Sell Net (Red)" in html

        print(f'Check Version V20260920_2309: {has_v}')
        print(f'Check Green Buy Line (#10b981): {has_green_buy}')
        print(f'Check Red Sell Line (#ef4444): {has_red_sell}')
        print(f'Check Blue Net Line (#0284c7): {has_blue_net}')
        print(f'Check UI Delta Buttons (Blue/Green/Red): {has_delta_blue and has_delta_green and has_delta_red}')

        assert has_v and has_green_buy and has_red_sell and has_blue_net and has_delta_blue, "Color verification failed!"
        print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")
except Exception as e:
    print('Error:', e)
