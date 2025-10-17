import httpx
import os
import time
from dotenv import load_dotenv

from app.metrics import REQUEST_COUNT, RESPONSE_TIME

# Load .env file
load_dotenv()

# Read API key from .env
WALLEX_API_KEY = os.getenv("WALLEX_API_KEY")

# URLs
NOBITEX_URL = "https://apiv2.nobitex.ir/market/stats?srcCurrency=usdt&dstCurrency=rls"
WALLEX_TRADES_URL = "https://api.wallex.ir/v1/trades?symbol=USDCUSDT"

async def get_nobitex_price():
    """
    Get the latest price of USDT/IRT from Nobitex (public endpoint, no API key required).
    """
    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                NOBITEX_URL,
                headers={"User-Agent": "TraderBot/ArbService"}
            )
            r.raise_for_status()
            data = r.json()
            price = float(data["stats"]["usdt-rls"]["latest"])

            # Record metrics for success
            REQUEST_COUNT.labels("nobitex", "success").inc()
            RESPONSE_TIME.labels("nobitex").observe(time.time() - start_time)

            return price

    except Exception as e:
        # Record metrics for failure
        REQUEST_COUNT.labels("nobitex", "failure").inc()
        RESPONSE_TIME.labels("nobitex").observe(time.time() - start_time)

        print(f"[ERROR] Failed to fetch from Nobitex: {e}")
        return None

async def get_wallex_price():
    """
    Get the latest USDC/USDT price from Wallex using API key.
    """
    start_time = time.time()
    try:
        headers = {
            "x-api-key": WALLEX_API_KEY,
            "User-Agent": "TraderBot/ArbService"
        }
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(WALLEX_TRADES_URL, headers=headers)
            r.raise_for_status()
            data = r.json()

            latest_trade = data["result"]["latestTrades"][0]
            price = float(latest_trade["price"])

            # Record metrics for success
            REQUEST_COUNT.labels("wallex", "success").inc()
            RESPONSE_TIME.labels("wallex").observe(time.time() - start_time)

            return price

    except Exception as e:
        # Record metrics for failure
        REQUEST_COUNT.labels("wallex", "failure").inc()
        RESPONSE_TIME.labels("wallex").observe(time.time() - start_time)

        print(f"[ERROR] Failed to fetch from Wallex: {e}")
        return None
