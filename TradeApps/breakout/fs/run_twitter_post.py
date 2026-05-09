from twitter_browser import TwitterBrowser
import sys
import os
from pathlib import Path

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
    
    # Run in headless mode if possible, but for first time login or if session expired,
    # headless=False might be needed to see what's happening.
    # We'll try headless=True first since session exists.
    with TwitterBrowser(headless=False) as tb:
        if not tb.is_logged_in():
            tb.login()
            print("[INFO] Please log in manually in the opened browser window.")
            print("[INFO] The script will wait up to 5 minutes for login to be detected.")
            if not tb.wait_for_login(timeout_seconds=300):
                print("[ERROR] Login failed or timed out.")
                return 1
        
        # Once logged in, post the tweet
        success = tb.post_tweet(tweet_text)
        if success:
            print("[SUCCESS] Summary posted to Twitter.")
            # Log the success
            with open("posted_tweets.log", "a", encoding="utf-8") as log:
                import datetime
                log.write(f"{datetime.datetime.now().isoformat()} | {tweet_text[:50]}...\n")
            return 0
        else:
            print("[ERROR] Failed to post tweet.")
            return 1

if __name__ == "__main__":
    exit(main())
