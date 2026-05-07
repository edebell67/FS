import os
import time
import asyncio
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def capture_screenshot(url, output_path):
    """
    Captures a screenshot of the given URL using Playwright.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print(f"Navigating to {url} for screenshot...")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.screenshot(path=output_path)
            print(f"Screenshot saved to {output_path}")
        except Exception as e:
            print(f"Failed to capture screenshot for {url}: {e}")
        finally:
            await browser.close()

def scan_site_for_broken_links(url, owner_name):
    """
    Scans a website for broken links (404s), creates owner folder structure,
    and captures screenshot evidence.
    """
    print(f"Starting enhanced scan for {url} (Owner: {owner_name})...")
    
    # Define and create owner folder structure
    base_epic_path = r"C:\Users\edebe\eds\epics\ep_014_website_break_fix"
    owner_path = os.path.join(base_epic_path, "owners", owner_name)
    evidence_path = os.path.join(owner_path, "evidence")
    solutions_path = os.path.join(owner_path, "solutions")
    tests_path = os.path.join(owner_path, "tests")
    
    for folder in [owner_path, evidence_path, solutions_path, tests_path]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")

    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        
        broken_links = []
        for link in links:
            href = link.get('href')
            if href and href.startswith('http'):
                try:
                    res = requests.head(href, timeout=5, allow_redirects=True)
                    if res.status_code >= 400:
                        print(f"Broken link found: {href} (Status: {res.status_code})")
                        broken_links.append({'url': href, 'status': res.status_code})
                        
                        # Capture screenshot evidence
                        filename = href.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_").replace(":", "_")[:100] + ".png"
                        screenshot_file = os.path.join(evidence_path, filename)
                        asyncio.run(capture_screenshot(href, screenshot_file))
                        
                except Exception as e:
                    print(f"Error checking {href}: {e}")
                    # Capture screenshot of the error if possible (or the site that linked to it)
                    broken_links.append({'url': href, 'status': 'ConnectionError'})
        
        # Log findings
        log_path = os.path.join(owner_path, 'broken_links_report.txt')
        with open(log_path, 'w') as f:
            f.write(f"Scan Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Target URL: {url}\n")
            f.write("-" * 50 + "\n")
            for bl in broken_links:
                f.write(f"URL: {bl['url']} | Status: {bl['status']}\n")
        
        print(f"Scan complete. Report saved to {log_path}")
        return broken_links

    except Exception as e:
        print(f"Failed to scan site: {e}")
        return []

if __name__ == "__main__":
    # To run: python broken_link_scanner.py <url> <owner_name>
    import sys
    if len(sys.argv) > 2:
        scan_site_for_broken_links(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python broken_link_scanner.py <url> <owner_name>")
