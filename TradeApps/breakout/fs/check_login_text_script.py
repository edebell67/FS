from twitter_browser import TwitterBrowser
try:
    with TwitterBrowser(headless=True) as tb:
        tb.page.goto('https://x.com/settings/account', wait_until='networkidle')
        content = tb.page.content().lower()
        print(f'Contains login: {"login" in content}')
        print(f'Contains sign up: {"sign up" in content}')
        print(f'Current URL: {tb.page.url}')
except Exception as e:
    print(f'[ERROR] {e}')
