from fastapi import FastAPI
from src.core.bootstrap import bootstrap
from src.core.events.bus import emit_event

app = FastAPI(title="SaaS Core API")


@app.on_event("startup")
async def startup():
    await bootstrap()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/message")
async def send_message(chat_id: int, text: str):
    await emit_event("send_message", {
        "chat_id": chat_id,
        "text": text
    })

    return {"status": "queued"}
