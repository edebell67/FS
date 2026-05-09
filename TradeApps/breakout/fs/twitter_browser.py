from playwright.sync_api import sync_playwright
from pathlib import Path
import time

# [2026-03-23 13:15] V20260323_1315 - Initial creation of Twitter browser automation module
# Part of task: breakout_social_content_browser_twitter_posting

SESSION_DIR = Path(__file__).parent / "twitter_session"

class TwitterBrowser:
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        if not SESSION_DIR.exists():
            SESSION_DIR.mkdir(parents=True, exist_ok=True)

        self.playwright = sync_playwright().start()
        # Use a persistent context to keep login session
        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=self.headless,
            viewport={"width": 1280, "height": 720}
        )
        self.browser.set_default_timeout(30000)
        # Ensure we have a page
        if self.browser.pages:
            self.page = self.browser.pages[0]
        else:
            self.page = self.browser.new_page()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def login(self):
        """Open Twitter for manual login setup."""
        print("[INFO] Opening Twitter login page. Please log in manually.")
        self.page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded", timeout=60000)
        print("[INFO] Leave this browser window open and complete login manually.")

    def wait_for_login(self, timeout_seconds: int = 300) -> bool:
        """Poll the current session until login completes or timeout is reached."""
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if self.is_logged_in():
                print("[SUCCESS] Login detected.")
                return True
            time.sleep(5)
        print("[WARN] Login was not detected before timeout.")
        return False

    def is_logged_in(self) -> bool:
        """Check if the session is currently valid."""
        try:
            self.page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
            # If we are redirected to /login or /i/flow/login, we are not logged in
            current_url = self.page.url
            if "login" in current_url.lower() or "flow" in current_url.lower():
                return False

            selectors = [
                '[data-testid="SideNav_NewTweet_Button"]',
                '[data-testid="AppTabBar_Home_Link"]',
                'a[href="/compose/post"]',
                '[data-testid="SideNav_AccountSwitcher_Button"]'
            ]
            for selector in selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    return True
                except Exception:
                    continue
            return False
        except Exception as e:
            print(f"[ERROR] Error checking login status: {e}")
            return False

    def post_tweet(self, text: str) -> bool:
        """Post a tweet using browser automation."""
        try:
            print("[INFO] Navigating to compose tweet...")
            self.page.goto("https://x.com/compose/post", wait_until="domcontentloaded")

            editor_selectors = [
                '[data-testid="tweetTextarea_0"]',
                'div[role="textbox"][data-testid="tweetTextarea_0"]',
                'div[role="textbox"]',
            ]
            editor = None
            for selector in editor_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    editor = self.page.locator(selector).first
                    break
                except Exception:
                    continue
            if editor is None:
                raise RuntimeError("Tweet composer was not found.")

            print("[INFO] Entering tweet text...")
            editor.click()
            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Delete")
            self.page.keyboard.insert_text(text)

            time.sleep(1)

            button_selectors = [
                '[data-testid="tweetButtonInline"]',
                '[data-testid="tweetButton"]',
            ]
            post_button = None
            for selector in button_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=5000)
                    post_button = self.page.locator(selector).first
                    break
                except Exception:
                    continue
            if post_button is None:
                raise RuntimeError("Post button was not found.")

            print("[INFO] Clicking post button...")
            post_button.click()

            # Give the compose flow time to dismiss or redirect.
            time.sleep(5)

            current_url = self.page.url.lower()
            if "compose" in current_url and "post" in current_url:
                print("[WARN] Compose page still open after click; post may not have completed.")
                return False

            print("[SUCCESS] Tweet posted successfully.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to post tweet: {e}")
            # Take a screenshot for debugging
            timestamp = int(time.time())
            screenshot_path = Path(__file__).parent / f"twitter_error_{timestamp}.png"
            self.page.screenshot(path=screenshot_path)
            print(f"[INFO] Error screenshot saved to {screenshot_path}")
            return False
