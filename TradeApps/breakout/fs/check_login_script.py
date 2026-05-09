from twitter_browser import TwitterBrowser
from pathlib import Path
import time
try:
    with TwitterBrowser(headless=True) as tb:
        print('[INFO] Navigating to check login...')
        logged_in = tb.is_logged_in()
        print(f'Logged in: {logged_in}')
        tb.page.screenshot(path='check_login.png')
        print('Screenshot saved to check_login.png')
        print(f'Current URL: {tb.page.url}')
except Exception as e:
    print(f'[ERROR] {e}')
