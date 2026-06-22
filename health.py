from fastapi import FastAPI
import time

app = FastAPI()
start = time.time()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime": time.time() - start
    }
