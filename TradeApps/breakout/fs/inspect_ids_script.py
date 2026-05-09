from twitter_browser import TwitterBrowser
import time
try:
    with TwitterBrowser(headless=True) as tb:
        tb.page.goto('https://x.com/home', wait_until='domcontentloaded')
        time.sleep(10)
        # Get all data-testid attributes
        test_ids = tb.page.evaluate('''() => {
            return Array.from(document.querySelectorAll('[data-testid]')).map(el => el.getAttribute('data-testid'));
        }''')
        print(f'Found {len(test_ids)} test IDs')
        print(f'Test IDs: {test_ids}')
except Exception as e:
    print(f'[ERROR] {e}')
