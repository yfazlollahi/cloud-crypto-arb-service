from app.exchanges import get_nobitex_price, get_wallex_price
from app.notifier import send_telegram_message
from datetime import datetime
from app.metrics import SCHEDULER_RUNS, ARBITRAGE_FOUND, PRICE_GAP
from app.database import insert_price, init_db

init_db()

async def check_arbitrage(threshold_ratio: float = 0.001):
    SCHEDULER_RUNS.inc()

    p_n = await get_nobitex_price()  # Nobitex price in Rial
    p_w_dollar = await get_wallex_price()  # Wallex price in USD

    if p_n is None or p_w_dollar is None:
        print("[WARN] Skipping arbitrage check because one price is None.")
        return

    # Convert Wallex to Rial
    p_w = p_w_dollar * p_n

    spread = p_w - p_n
    avg_price = (p_n + p_w) / 2
    ratio = abs(spread) / avg_price

    print(f"Nobitex: {p_n:.2f} IRR | Wallex: {p_w:.2f} IRR | Spread: {spread:.2f} | Ratio: {ratio:.4f}")

    insert_price("nobitex", p_n)
    insert_price("wallex", p_w)

    if ratio >= threshold_ratio:
        # Record Prometheus metrics
        ARBITRAGE_FOUND.inc()
        PRICE_GAP.labels("USDT-USDC").observe(abs(spread))

        direction = "Buy Nobitex / Sell Wallex" if spread > 0 else "Buy Wallex / Sell Nobitex"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build Telegram message
        message = (
            f"*Arbitrage Opportunity Detected!*\n\n"
            f"Pair: USDT/USDC\n"
            f"Time: {timestamp}\n"
            f"Nobitex: {p_n:,.0f} IRR\n"
            f"Wallex: {p_w:,.0f} IRR\n"
            f"Spread: {spread:,.0f} IRR\n"
            f"Difference: {ratio*100:.2f}%\n"
            f"Direction: {direction}"
        )

        await send_telegram_message(message)
