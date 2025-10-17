from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting arbitrage service...")
    start_scheduler()
    yield
    print("Shutting down arbitrage service...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Arbitrage Service Running"}
