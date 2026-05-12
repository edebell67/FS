from playwright.sync_api import sync_playwright
import time
import re
import shutil
from pathlib import Path
import sys
from paths import KEY_FILE, TWITTER_SESSION_DIR

if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_creds():
    with open(KEY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    username_match = re.search(r'"username"\s*:\s*"([^"]+)"', content)
    password_match = re.search(r'"password"\s*:\s*"([^"]+)"', content)
    return (username_match.group(1) if username_match else None,
            password_match.group(1) if password_match else None)

def main():
    username, password = get_creds()
    if not username or not password:
        print("[ERROR] Credentials not found.")
        return 1

    print("[INFO] Clearing old corrupted session...")
    try:
        if SESSION_DIR.exists():
            shutil.rmtree(SESSION_DIR, ignore_errors=True)
    except Exception as e:
        print(f"[WARNING] Could not clear session: {e}")

    print("[INFO] Launching browser for login...")
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            user_data_dir=SESSION_DIR,
            headless=True,
            viewport={"width": 1280, "height": 720},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0]

        try:
            print("[INFO] Navigating to Twitter login...")
            page.goto("https://x.com/i/flow/login")
            
            for i in range(3):
                time.sleep(10)
                if "Something went wrong" in page.content():
                    print(f"[INFO] Attempt {i+1}: Found error, reloading...")
                    page.reload()
                else:
                    break

            print("[INFO] Waiting for username field...")
            # Find the visible input field for username
            username_input = page.locator('input[autocomplete="username"]')
            username_input.wait_for(timeout=20000)
            username_input.fill(username)
            print("[INFO] Filled username. Proceeding to next step...")
            page.keyboard.press("Enter")

            time.sleep(5)

            # Check for security prompt
            if "Enter your phone number or email address" in page.content() or "unusual activity" in page.content():
                print("[INFO] Security prompt detected. Trying email guess...")
                page.evaluate("""(email) => {
                    const inputs = Array.from(document.querySelectorAll('input'));
                    const target = inputs.find(i => i.offsetHeight > 0 && i.offsetWidth > 0);
                    if (target) {
                        target.value = email;
                        target.dispatchEvent(new Event('input', { bubbles: true }));
                        target.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }""", "ed.ebell@gmail.com")
                time.sleep(2)
                page.keyboard.press("Enter")
                time.sleep(5)

            password_input = page.locator('input[name="password"]')
            password_input.wait_for(timeout=20000)

            print("[INFO] Entering password...")
            password_input.fill(password)
            print("[INFO] Submitted password.")
            page.keyboard.press("Enter")

            print("[INFO] Waiting for login to complete...")
            time.sleep(15)
            page.screenshot(path="login_result.png")
            
            if "home" in page.url or "x.com/home" in page.url:
                print("[SUCCESS] Successfully logged into Twitter/X.")
                return 0
            else:
                print(f"[WARNING] Did not reach /home. Current URL: {page.url}")
                if "login" not in page.url and "flow" not in page.url:
                     print("[SUCCESS] Appears to have logged in despite not reaching /home.")
                     return 0
                return 1

        except Exception as e:
            print(f"[ERROR] Login automation failed: {e}")
            page.screenshot(path="login_automation_error.png")
            return 1
        finally:
            context.close()

if __name__ == '__main__':
    exit(main())
