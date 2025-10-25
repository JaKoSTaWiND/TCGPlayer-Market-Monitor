from playwright.sync_api import sync_playwright
import time

def get_cookies_from_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.tcgplayer.com", wait_until="networkidle")
        time.sleep(60)
        cookies = page.context.cookies()
        print(f"🔍 Found {len(cookies)} cookies")
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        print(cookie_str)
        browser.close()
        return cookie_str

