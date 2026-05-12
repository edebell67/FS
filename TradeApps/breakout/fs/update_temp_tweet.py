import json
from pathlib import Path
from paths import BREAKOUT_DATA_FS_ROOT, BREAKOUT_JSON_ROOT

# [2026-04-02 00:50] V20260402_0050 - Extract latest consolidated post for Twitter
PACKAGE_DIR = BREAKOUT_JSON_ROOT / "live" / "social_posting_package" / "2026-04-02"
JSON_PATH = PACKAGE_DIR / "top5_weekly_posting_package.json"
OUTPUT_PATH = BREAKOUT_DATA_FS_ROOT / "temp_tweet.txt"

def main():
    if not JSON_PATH.exists():
        print(f"[ERROR] Package not found at {JSON_PATH}")
        return
    
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        post_text = data.get("consolidated_twitter_post")
        if post_text:
            with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
                out.write(post_text)
            print(f"[SUCCESS] Updated temp_tweet.txt with latest canonical data.")
            print("--- NEW TWEET ---")
            print(post_text)
        else:
            print("[ERROR] No consolidated post found in JSON.")

if __name__ == "__main__":
    main()
