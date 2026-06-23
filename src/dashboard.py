import os
from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import datetime

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SLH Admin Dashboard</title>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="30">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:#0a0a0a; color:#e0e0e0; font-family:'Segoe UI',sans-serif; }
        .header { background:#111; padding:20px 30px; border-bottom:1px solid #222; display:flex; justify-content:space-between; align-items:center; }
        .header h1 { color:#00d2ff; font-size:24px; }
        .header .status { color:#00ff88; font-size:13px; }
        .cards { display:flex; gap:20px; padding:30px; flex-wrap:wrap; }
        .card { background:#111; border:1px solid #222; border-radius:12px; padding:24px; min-width:200px; flex:1; }
        .card .label { color:#888; font-size:13px; margin-bottom:8px; }
        .card .value { color:#00d2ff; font-size:36px; font-weight:700; }
        .card .sub { color:#555; font-size:12px; margin-top:4px; }
        .table-wrap { padding:0 30px 30px; }
        .table-wrap h2 { color:#fff; margin-bottom:16px; font-size:18px; }
        table { width:100%; border-collapse:collapse; background:#111; border-radius:12px; overflow:hidden; }
        th { background:#1a1a1a; color:#888; font-size:12px; text-transform:uppercase; padding:12px 16px; text-align:left; }
        td { padding:12px 16px; border-bottom:1px solid #1a1a1a; font-size:14px; }
        tr:last-child td { border-bottom:none; }
        tr:hover td { background:#151515; }
        .badge { background:#00d2ff22; color:#00d2ff; padding:3px 10px; border-radius:20px; font-size:12px; }
        .time { color:#555; font-size:12px; text-align:right; padding:10px 30px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚡ SLH Admin Dashboard</h1>
        <div class="status">● LIVE — auto refresh 30s</div>
    </div>
    <div class="cards">
        <div class="card">
            <div class="label">Total Users</div>
            <div class="value">{{total}}</div>
            <div class="sub">registered in bot</div>
        </div>
        <div class="card">
            <div class="label">DB Status</div>
            <div class="value" style="color:#00ff88;font-size:24px;">ONLINE</div>
            <div class="sub">PostgreSQL Railway</div>
        </div>
        <div class="card">
            <div class="label">Bot Status</div>
            <div class="value" style="color:#00ff88;font-size:24px;">RUNNING</div>
            <div class="sub">Polling mode</div>
        </div>
        <div class="card">
            <div class="label">Last User</div>
            <div class="value" style="font-size:20px;color:#fff;">{{last_user}}</div>
            <div class="sub">most recent signup</div>
        </div>
    </div>
    <div class="table-wrap">
        <h2>👥 Users</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Telegram ID</th>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Email</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {{rows}}
            </tbody>
        </table>
    </div>
    <div class="time">Last updated: {{now}}</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    engine = create_async_engine(DATABASE_URL)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT id, telegram_id, name, age, email FROM users ORDER BY id DESC"))
            users = result.fetchall()
    finally:
        await engine.dispose()

    total = len(users)
    last_user = users[0][2] if users else "None"

    rows = ""
    for i, u in enumerate(users, 1):
        rows += f"""
        <tr>
            <td>{i}</td>
            <td><code>{u[1]}</code></td>
            <td>{u[2]}</td>
            <td>{u[3]}</td>
            <td>{u[4]}</td>
            <td><span class="badge">active</span></td>
        </tr>"""

    html = HTML.replace("{{total}}", str(total))
    html = html.replace("{{last_user}}", last_user)
    html = html.replace("{{rows}}", rows)
    html = html.replace("{{now}}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return html

@app.get("/api/stats")
async def stats():
    engine = create_async_engine(DATABASE_URL)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT COUNT(*) FROM users"))
            total = result.scalar()
    finally:
        await engine.dispose()
    return {"total_users": total, "status": "ok", "db": "postgresql"}

@app.get("/health")
async def health():
    return {"status": "healthy"}



