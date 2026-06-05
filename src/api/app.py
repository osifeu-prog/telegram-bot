from fastapi import FastAPI
from src.core.bootstrap import bootstrap

app = FastAPI(title="Telegram Bot Enterprise")

@app.on_event("startup")
async def startup():
    await bootstrap()

@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/health")
def health():
    return {"status": "ok"}
