import asyncio
from playwright.async_api import async_playwright


async def scrape_profile(url: str) -> dict:
    """
    Scrape a X.com profile details e.g.: https://x.com/Scrapfly_dev
    """
    _xhr_calls = []

    def intercept_response(response):
        """capture all background requests and save them"""
        # we can extract details from background requests
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        # enable background request intercepting:
        page.on("response", intercept_response)
        # go to url and wait for the page to load
        await page.goto(url)
        await page.wait_for_selector("[data-testid='primaryColumn']")

        # find all tweet background requests:
        tweet_calls = [f for f in _xhr_calls if "UserBy" in f.url]
        
        if not tweet_calls:
            return {}

        for xhr in tweet_calls:
            data = xhr.json()
            if 'data' in data and 'user' in data['data'] and 'result' in data['data']['user']:
                return data['data']['user']['result']

    return {}


if __name__ == "__main__":
    print(asyncio.run(scrape_profile("https://x.com/Scrapfly_dev")))