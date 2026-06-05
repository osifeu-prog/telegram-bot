import json
from src.queue.client import publish


async def emit_event(event_type: str, payload: dict):
    await publish("events", json.dumps({
        "type": event_type,
        "payload": payload
    }))
