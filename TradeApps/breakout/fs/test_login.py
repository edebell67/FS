from twitter_browser import TwitterBrowser
with TwitterBrowser(headless=True) as tw:
    print(f'Logged in: {tw.is_logged_in()}')
