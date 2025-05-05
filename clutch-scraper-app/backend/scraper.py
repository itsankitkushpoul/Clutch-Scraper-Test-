import asyncio
import random
from urllib.parse import urlparse
from playwright.async_api import async_playwright

async def scrape_clutch(url: str, headless: bool, ua: str | None, proxy: str | None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context_kwargs = {}
        if proxy:
            context_kwargs['proxy'] = {'server': proxy}
        context = await browser.new_context(**context_kwargs)
        if ua:
            await context.set_extra_http_headers({'User-Agent': ua})
        page = await context.new_page()
        await page.goto(url, timeout=120_000)
        await page.wait_for_load_state('networkidle')
        # ... your scraping selectors here ...
        names = []
        data = []
        locations = []
        await browser.close()
        return names, data, locations
