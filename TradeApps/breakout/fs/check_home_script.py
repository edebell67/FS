from twitter_browser import TwitterBrowser
import time
try:
    with TwitterBrowser(headless=True) as tb:
        print('[INFO] Navigating to home...')
        tb.page.goto('https://x.com/home', wait_until='domcontentloaded')
        print(f'Final URL: {tb.page.url}')
        time.sleep(5)
        print(f'URL after wait: {tb.page.url}')
        tb.page.screenshot(path='check_home.png')
except Exception as e:
    print(f'[ERROR] {e}')
