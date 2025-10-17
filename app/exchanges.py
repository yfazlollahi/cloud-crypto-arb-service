import httpx
import os
from dotenv import load_dotenv

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
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                NOBITEX_URL,
                headers={"User-Agent": "TraderBot/ArbService"}
            )
            r.raise_for_status()
            data = r.json()
            return float(data["stats"]["usdt-rls"]["latest"])
    except Exception as e:
        print(f"[ERROR] Failed to fetch from Nobitex: {e}")
        return None

async def get_wallex_price():
    """
    Get the latest USDC/USDT price from Wallex using API key.
    """
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
            return price
    except Exception as e:
        print(f"[ERROR] Failed to fetch from Wallex: {e}")
        return None
