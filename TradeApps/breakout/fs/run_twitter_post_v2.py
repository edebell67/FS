from twitter_browser import TwitterBrowser
import sys
import os
import time
from pathlib import Path
import tempfile

# Fix encoding for emoji printing
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    tweet_file = Path("temp_tweet.txt")
    if not tweet_file.exists():
        print("[ERROR] temp_tweet.txt not found.")
        return 1
    
    with open(tweet_file, "r", encoding="utf-8") as f:
        tweet_text = f.read()
    
    print(f"[INFO] Attempting to post tweet:\n{tweet_text}")
    
    # Using a temporary directory to avoid profile locks
    temp_dir = tempfile.mkdtemp(prefix="twitter_automation_")
    print(f"[INFO] Using temporary profile: {temp_dir}")

    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        # Launch fresh context
        context = p.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            headless=False,
            viewport={"width": 1280, "height": 720}
        )
        page = context.pages[0]
        
        # Initial check/login
        page.goto("https://x.com/home")
        time.sleep(5)
        
        if "login" in page.url or "flow" in page.url:
            print("[INFO] Please log in manually in the opened browser window.")
            # Simple poll for login detection
            logged_in = False
            for _ in range(60): # 5 minutes
                if "login" not in page.url.lower() and "flow" not in page.url.lower() and "/home" in page.url.lower():
                    print("[SUCCESS] Login detected.")
                    logged_in = True
                    break
                time.sleep(5)
            
            if not logged_in:
                print("[ERROR] Login timed out.")
                return 1
        
        # Post the tweet (integrated logic from TwitterBrowser)
        try:
            print("[INFO] Navigating to compose tweet...")
            page.goto("https://x.com/compose/post")
            
            print("[INFO] Waiting for editor...")
            editor = page.locator('div[role="textbox"]').first
            editor.wait_for(timeout=30000) # Increased to 30s
            editor.click()
            page.keyboard.insert_text(tweet_text)
            time.sleep(2)
            
            post_button = page.locator('[data-testid="tweetButtonInline"], [data-testid="tweetButton"]').first
            post_button.wait_for(timeout=5000)
            post_button.click()
            
            print("[INFO] Waiting for post confirmation...")
            time.sleep(10) # Wait for it to clear
            
            print("[SUCCESS] Tweet should be posted.")
            
            # Log success
            with open("posted_tweets.log", "a", encoding="utf-8") as log:
                import datetime
                log.write(f"{datetime.datetime.now().isoformat()} | {tweet_text[:50]}...\n")
            
            return 0
        except Exception as e:
            print(f"[ERROR] Failed to post: {e}")
            page.screenshot(path="twitter_error_final.png")
            return 1
        finally:
            context.close()

if __name__ == "__main__":
    exit(main())
