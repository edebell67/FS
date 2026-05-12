from pathlib import Path
import datetime
import json
import sys
import time

from playwright.sync_api import sync_playwright
from paths import BREAKOUT_DATA_FS_ROOT, TWITTER_SESSION_DIR

if sys.stdout.encoding != "utf-8":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SESSION_DIR = TWITTER_SESSION_DIR
TWEET_FILE = BREAKOUT_DATA_FS_ROOT / "temp_tweet.txt"
STATUS_FILE = BREAKOUT_DATA_FS_ROOT / "twitter_post_status.json"
LOGIN_SCREENSHOT = BREAKOUT_DATA_FS_ROOT / "twitter_login_check.png"
SUCCESS_SCREENSHOT = BREAKOUT_DATA_FS_ROOT / "twitter_post_success.png"
ERROR_SCREENSHOT = BREAKOUT_DATA_FS_ROOT / "twitter_post_error.png"


def _new_status() -> dict:
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "tweet_file": str(TWEET_FILE),
        "session_dir": str(SESSION_DIR),
        "steps": {
            "load_tweet": {"ok": False, "details": ""},
            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_SCREENSHOT)},
            "submit_post": {"ok": False, "details": ""},
            "verify_publication": {"ok": False, "details": "", "artifact": str(SUCCESS_SCREENSHOT)},
        },
        "final_status": "failed",
    }


def _write_status(status: dict) -> None:
    STATUS_FILE.write_text(json.dumps(status, indent=2), encoding="utf-8")


def _mark_step(status: dict, step: str, ok: bool, details: str) -> None:
    status["steps"][step]["ok"] = ok
    status["steps"][step]["details"] = details
    _write_status(status)


def _dismiss_cookie_banner(page) -> str:
    selectors = [
        'button:has-text("Accept all cookies")',
        'button:has-text("Refuse non-essential cookies")',
    ]
    for selector in selectors:
        try:
            button = page.locator(selector).first
            if button.is_visible():
                button.click(force=True)
                time.sleep(1)
                return f"Clicked cookie banner button: {selector}"
        except Exception:
            continue
    return "No cookie banner action required."


def _type_tweet_human_like(page, tweet_text: str) -> None:
    for line_index, line in enumerate(tweet_text.splitlines()):
        if line:
            page.keyboard.type(line, delay=35)
        if line_index < len(tweet_text.splitlines()) - 1:
            page.keyboard.press("Shift+Enter")
            time.sleep(0.2)
    time.sleep(1.5)


def _click_post_button(page) -> tuple[bool, str]:
    button_selectors = [
        "[data-testid=\"tweetButton\"]",
        "[data-testid=\"tweetButtonInline\"]",
    ]
    for selector in button_selectors:
        try:
            print(f"[DEBUG] Checking selector: {selector}")
            button = page.locator(selector).first
            if button.count() == 0:
                print(f"[DEBUG] Selector {selector} not found.")
                continue
            is_vis = button.is_visible()
            is_en = button.is_enabled()
            print(f"[DEBUG] Selector {selector} found. Visible: {is_vis}, Enabled: {is_en}")
            if not is_vis or not is_en:
                print(f"[DEBUG] Selector {selector} is hidden or disabled.")
                continue
            button.click(force=True)
            return True, f"Clicked post button via {selector}"
        except Exception as e:
            print(f"[DEBUG] Error checking {selector}: {e}")
            continue
    return False, "No enabled post button was available." 


def _is_logged_in(page) -> tuple[bool, str]:
    current_url = page.url.lower()
    if "login" in current_url or "flow" in current_url:
        return False, f"Session redirected to authentication flow: {page.url}"

    selectors = [
        '[data-testid="SideNav_NewTweet_Button"]',
        '[data-testid="AppTabBar_Home_Link"]',
        'a[href="/compose/post"]',
        '[data-testid="SideNav_AccountSwitcher_Button"]',
    ]
    for selector in selectors:
        try:
            page.wait_for_selector(selector, timeout=10000)
            return True, f"Authenticated selector found: {selector}"
        except Exception:
            continue
    return False, "No authenticated navigation selectors were found."


def _looks_like_post_failure(page) -> str | None:
    lowered = page.content().lower()
    if "something went wrong" in lowered:
        return "Twitter returned a generic failure message."
    if "post failed" in lowered:
        return "Twitter reported that the post failed."
    if "try again" in lowered and "post" in lowered:
        return "Twitter surfaced a retry/failure message after submit."
    if "login" in page.url or "flow" in page.url:
        return f"Session redirected to authentication flow: {page.url}"
    return None


def _wait_for_post_confirmation(page, editor, timeout_seconds: int = 20) -> tuple[bool, str]:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        failure_reason = _looks_like_post_failure(page)
        if failure_reason:
            return False, failure_reason
        try:
            editor_visible = editor.is_visible()
        except Exception:
            editor_visible = False
        current_url = page.url
        if "/compose/post" not in current_url and not editor_visible:
            return True, f"Compose page closed after submit; current URL is {current_url}"
        time.sleep(1)
    return False, f"No post confirmation detected within {timeout_seconds}s; still on {page.url}"


def _verify_publication(page, tweet_text: str) -> tuple[bool, str]:
    current_url = page.url
    if "/status/" in current_url:
        return True, f"Navigated to tweet detail URL: {current_url}"

    lowered = page.content().lower()
    snippet = " ".join(tweet_text.split())[:32].lower()
    if snippet and snippet in lowered and "/compose/post" not in current_url:
        return True, "Tweet text snippet is visible after submit."

    success_markers = [
        "your post was sent",
        "your post was posted",
        "post sent",
    ]
    for marker in success_markers:
        if marker in lowered:
            return True, f"Success marker detected: {marker}"

    return False, f"No publication marker detected after submit; current URL is {current_url}"


def main():
    status = _new_status()
    _write_status(status)

    if not TWEET_FILE.exists():
        print("[ERROR] temp_tweet.txt not found.")
        _mark_step(status, "load_tweet", False, "temp_tweet.txt not found")
        return 1

    tweet_text = TWEET_FILE.read_text(encoding="utf-8").strip()
    if not tweet_text:
        print("[ERROR] temp_tweet.txt is empty.")
        _mark_step(status, "load_tweet", False, "temp_tweet.txt is empty")
        return 1
    _mark_step(status, "load_tweet", True, f"Loaded tweet text ({len(tweet_text)} chars)")

    print("[INFO] Attempting to post tweet using authenticated session...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True,
            viewport={"width": 1280, "height": 720},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
            ],
        )
        page = context.pages[0]

        try:
            page.goto("https://x.com/home")
            time.sleep(5)
            page.screenshot(path=LOGIN_SCREENSHOT)

            logged_in, login_reason = _is_logged_in(page)
            if not logged_in:
                print("[ERROR] Session is not authenticated. Please run auto_twitter_login.py again.")
                _mark_step(status, "verify_login", False, login_reason)
                return 1
            _mark_step(status, "verify_login", True, login_reason)

            print("[INFO] Navigating to compose tweet...")
            page.goto("https://x.com/compose/post")
            time.sleep(2)
            _dismiss_cookie_banner(page)

            print("[INFO] Waiting for editor...")
            editor = page.locator('div[role="textbox"]').first
            editor.wait_for(timeout=30000)
            editor.click()
            _type_tweet_human_like(page, tweet_text)

            page.keyboard.press("Control+Enter"); clicked = True; submit_reason = "Forced Control+Enter shortcut"
            if not clicked:
                print("[INFO] Post button click unavailable; falling back to Control+Enter...")
                page.keyboard.press("Control+Enter")
                submit_reason = "Submit shortcut sent via Control+Enter fallback"
            _mark_step(status, "submit_post", True, submit_reason)

            print("[INFO] Waiting for post confirmation...")
            confirmed, confirm_reason = _wait_for_post_confirmation(page, editor)
            if not confirmed:
                raise RuntimeError(confirm_reason)

            published, publish_reason = _verify_publication(page, tweet_text)
            if not published:
                raise RuntimeError(publish_reason)

            page.screenshot(path=SUCCESS_SCREENSHOT)
            _mark_step(status, "verify_publication", True, publish_reason)

            print("[SUCCESS] Tweet successfully posted.")
            with open("posted_tweets.log", "a", encoding="utf-8") as log:
                log.write(f"{datetime.datetime.now().isoformat()} | {tweet_text[:50]}...\n")

            status["final_status"] = "success"
            _write_status(status)
            return 0

        except Exception as exc:
            print(f"[ERROR] Failed to post: {exc}")
            try:
                page.screenshot(path=ERROR_SCREENSHOT)
            except Exception:
                pass
            status["final_status"] = "failed"
            _write_status(status)
            return 1
        finally:
            context.close()


if __name__ == "__main__":
    raise SystemExit(main())
