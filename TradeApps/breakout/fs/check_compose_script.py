from twitter_browser import TwitterBrowser
import time
try:
    with TwitterBrowser(headless=True) as tb:
        print('[INFO] Navigating to compose...')
        tb.page.goto('https://x.com/compose/post', wait_until='domcontentloaded')
        print(f'Current URL: {tb.page.url}')
        time.sleep(10) # Wait manually
        editor_selectors = [
            '[data-testid=\"tweetTextarea_0\"]',
            'div[role=\"textbox\"][data-testid=\"tweetTextarea_0\"]',
            'div[role=\"textbox\"]',
        ]
        found = False
        for selector in editor_selectors:
            try:
                el = tb.page.wait_for_selector(selector, timeout=10000)
                if el:
                    print(f'[SUCCESS] Found editor with selector: {selector}')
                    found = True
                    break
            except:
                continue
        if not found:
            print('[FAIL] Could not find editor.')
        tb.page.screenshot(path='check_compose.png')
except Exception as e:
    print(f'[ERROR] {e}')
