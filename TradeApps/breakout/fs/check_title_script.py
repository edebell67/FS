from twitter_browser import TwitterBrowser
try:
    with TwitterBrowser(headless=True) as tb:
        tb.page.goto('https://x.com/settings/account', wait_until='networkidle')
        print(f'Title: {tb.page.title()}')
        print(f'URL: {tb.page.url}')
except Exception as e:
    print(f'[ERROR] {e}')
