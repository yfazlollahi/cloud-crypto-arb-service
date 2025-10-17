from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.arbitrage import check_arbitrage

def start_scheduler():
    scheduler = AsyncIOScheduler()
    # Run the check_arbitrage function every 15 seconds
    scheduler.add_job(check_arbitrage, "interval", seconds=15)
    scheduler.start()
