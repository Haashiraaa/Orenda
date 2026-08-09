"""
Fetch layer. Static requests first (cheap, fast). Falls back to
Playwright only when the page is actually JS-rendered - rendering is
the expensive path, don't pay for it by default.
"""
import requests

from src.scrapper.cleaner import Cleaner


class Fetcher:
    

    def __init__(self) -> None:
        self.default_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }


    def fetch_static(self, url: str, timeout: int = 15) -> str:
        resp = requests.get(url, headers=self.default_headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text


    def fetch_rendered(self, url: str, wait_ms: int = 2500) -> str:
        """
        Requires: pip install playwright && playwright install chromium
        Only imported lazily so the static path doesn't need it installed.
        """
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(user_agent=self.default_headers["User-Agent"])
            page.goto(url, timeout=30000)
            page.wait_for_timeout(wait_ms)
            html = page.content()
            browser.close()
            return html


    def fetch(self, url: str, cleaner: Cleaner, force_render: bool = False) -> tuple[str, bool]:
        """
        Returns (html, was_rendered).
        """
        if not force_render:
            html = self.fetch_static(url)
            if not cleaner.looks_js_rendered(html):
                return html, False
        return self.fetch_rendered(url), True

