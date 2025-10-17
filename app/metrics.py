from prometheus_client import Counter, Histogram

# Counter for total requests to each exchange (success/failure)
REQUEST_COUNT = Counter(
    "exchange_requests_total",
    "Total number of requests to each exchange",
    ["exchange", "status"]
)

# Counter for total arbitrage opportunities found
ARBITRAGE_FOUND = Counter(
    "arbitrage_opportunities_total",
    "Total number of arbitrage opportunities found"
)

# Histogram for tracking the last observed price gap between exchanges
PRICE_GAP = Histogram(
    "last_price_gap",
    "Last price gap observed per pair",
    ["pair"]
)

# Histogram for tracking exchange response times
RESPONSE_TIME = Histogram(
    "exchange_response_time_seconds",
    "Response time per exchange",
    ["exchange"]
)

# Optional: Counter for number of arbitrage checks executed
SCHEDULER_RUNS = Counter(
    "arbitrage_checks_total",
    "Total number of arbitrage check executions"
)
