from twitter_browser import TwitterBrowser
try:
    with TwitterBrowser(headless=True) as tb:
        tb.page.goto('https://x.com/settings/account', wait_until='networkidle')
        content = tb.page.content()
        print(f'Content length: {len(content)}')
        print(f'Content preview: {content[:500]}')
except Exception as e:
    print(f'[ERROR] {e}')
