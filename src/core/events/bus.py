from src.billing.hooks import on_event

async def emit_event(event_name: str, payload: dict):
    await on_event(event_name, payload)
