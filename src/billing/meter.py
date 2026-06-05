from src.core.state import state

usage_store = {}

def track(user_id: int, key: str, amount: int = 1):
    if user_id not in usage_store:
        usage_store[user_id] = {}

    usage_store[user_id][key] = usage_store[user_id].get(key, 0) + amount


def get_usage(user_id: int):
    return usage_store.get(user_id, {})
