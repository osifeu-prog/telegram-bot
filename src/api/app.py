from fastapi import FastAPI
from src.core.bootstrap import bootstrap
from src.core.events.bus import emit_event
from src.billing.enforcer import check_limit

app = FastAPI(title="SaaS Core API")


@app.on_event("startup")
async def startup():
    await bootstrap()


@app.post("/message")
async def send_message(chat_id: int, text: str, user_id: int = 0, plan: str = "free"):

    allowed = check_limit(user_id, plan, "bot")

    if not allowed:
        return {"status": "blocked", "reason": "plan limit exceeded"}

    await emit_event("send_message", {
        "chat_id": chat_id,
        "text": text,
        "user_id": user_id
    })

    return {"status": "queued"}
