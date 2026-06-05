from src.billing.meter import track

async def on_event(event_name: str, payload: dict):
    user_id = payload.get("user_id", 0)

    if event_name == "send_message":
        track(user_id, "bot_limit")

    if event_name == "api_call":
        track(user_id, "api_limit")
