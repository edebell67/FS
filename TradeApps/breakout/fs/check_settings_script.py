from twitter_browser import TwitterBrowser
from pathlib import Path
import time
try:
    with TwitterBrowser(headless=True) as tb:
        print('[INFO] Navigating to settings/account...')
        tb.page.goto('https://x.com/settings/account', wait_until='networkidle')
        print(f'Final URL: {tb.page.url}')
        tb.page.screenshot(path='check_settings.png')
        print('Screenshot saved to check_settings.png')
except Exception as e:
    print(f'[ERROR] {e}')
