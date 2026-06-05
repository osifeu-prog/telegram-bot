from dataclasses import dataclass

@dataclass
class Plan:
    name: str
    api_limit: int
    bot_limit: int
    worker_limit: int


PLANS = {
    "free": Plan("free", 20, 50, 10),
    "pro": Plan("pro", 500, 2000, 200),
    "business": Plan("business", 10000, 50000, 5000),
}
