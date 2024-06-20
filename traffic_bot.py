import asyncio
import logging
import random
from itertools import cycle
from fake_useragent import UserAgent
import aiohttp
from pyppeteer import launch

# Configure logging
logging.basicConfig(level=logging.INFO)

async def fetch_proxies_from_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    proxies = []
                    text = await response.text()
                    for line in text.split('\n'):
                        proxy_data = line.strip().split(':')
                        if len(proxy_data) == 2:
                            proxies.append((proxy_data[0], proxy_data[1]))
                    return proxies
                else:
                    logging.error(f"Failed to fetch proxies from {url}: HTTP {response.status}")
                    return []
    except Exception as e:
        logging.error(f"Failed to fetch proxies from {url}: {e}")
        return []

async def get_random_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except Exception as e:
        logging.warning(f"Failed to generate a random user agent: {e}")
        fallback_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        return random.choice(fallback_user_agents)

def get_random_referer():
    referers = [
        "https://www.facebook.com",
        "https://twitter.com",
        "https://www.youtube.com",
        "https://www.tiktok.com",
        "https://www.pinterest.com",
        "https://www.google.com",
        "https://www.bing.com"
    ]
    return random.choice(referers)

async def visit_url_with_pyppeteer(url, proxy, user_agent, referer):
    try:
        proxy_string = f"{proxy[0]}:{proxy[1]}"
        browser = await launch(args=[f'--proxy-server={proxy_string}', '--headless'])
        page = await browser.newPage()
        await page.setUserAgent(user_agent)
        await page.goto(url, {'referer': referer})

        # Simulate user interaction by scrolling
        for _ in range(random.randint(2, 3)):
            await page.keyboard.press('PageDown')
            await asyncio.sleep(random.uniform(0.5, 2))

        for _ in range(random.randint(2, 3)):
            await page.keyboard.press('PageUp')
            await asyncio.sleep(random.uniform(0.5, 2))

        logging.info(f"Visited {url} successfully with proxy {proxy[0]}:{proxy[1]} and referer: {referer}")
        await browser.close()
        return True
    except Exception as e:
        logging.error(f"Failed to visit URL with proxy {proxy[0]}:{proxy[1]}: {e}")
        return False

async def main():
    url = "https://www.highrevenuenetwork.com/iaqgtx69y1?key=14a1e46999747270c942f2634ef5306a"
    num_traffic = 10
    proxy_type = "http"

    if proxy_type.lower() == 'socks5':
        proxy_url = 'https://info.proxy.abcproxy.com/extractProxyIp?regions=us&num=500&protocol=socks5&return_type=txt&lh=1&mode=1'
    elif proxy_type.lower() == 'socks4':
        proxy_url = 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt'
    elif proxy_type.lower() == 'http':
        proxy_url = 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt'
    else:
        logging.error("Invalid proxy type. Please choose from 'socks5', 'socks4', or 'http'.")
        return

    while True:
        # Fetch proxies
        proxies = await fetch_proxies_from_url(proxy_url)
        if not proxies:
            logging.error("No proxies available. Exiting.")
            return

        proxy_pool = cycle(proxies)
        success_count = 0

        for i in range(num_traffic):
            user_agent = await get_random_user_agent()
            proxy = next(proxy_pool)
            referer = get_random_referer()  # Get a random referer for each visit
            try:
                success = await visit_url_with_pyppeteer(url, proxy, user_agent, referer)
                if success:
                    success_count += 1
                    logging.info(f"[{i+1}/{num_traffic}] Visit successful using Pyppeteer")
                else:
                    logging.info(f"[{i+1}/{num_traffic}] Visit failed using Pyppeteer")
            except Exception as e:
                logging.error(f"Failed to visit URL: {e}")
            # Pause between visits
            await asyncio.sleep(random.randint(10, 20))

        logging.info(f"Total successful visits: {success_count}")

if __name__ == "__main__":
    asyncio.run(main())
