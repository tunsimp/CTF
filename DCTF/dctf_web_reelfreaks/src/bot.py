from playwright.sync_api import sync_playwright
import os

def visit(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--ignore-ssl-errors=yes',
                '--ignore-certificate-errors',
                '--start-maximized',
                '--disable-infobars',
                '--disable-extensions',
                '--disable-gpu',
                '--no-sandbox'
            ]
        )
        page = browser.new_page()
        page.goto("https://127.0.0.1:5000/login")

        page.fill("#username", os.getenv("ADMIN_USER") or 'admin')
        page.fill("#password", os.getenv("ADMIN_PASS") or 'admin')

        page.click("#submit")

        page.goto(url,wait_until="networkidle",timeout=60000)

        browser.close()