## File: D:\0\0.1\slh-telegram-bot\run_bot.py
Purpose: Entrypoint script to start the Telegram bot process; sets up environment, loads configuration, initializes logging, connects to Redis and DB, creates and runs the async event loop and the bot application.
Dependencies: asyncio; dotenv; logging; Redis client; DB driver (asyncpg or psycopg2); uvicorn.
Inputs: TELEGRAM_TOKEN, DATABASE_URL, REDIS_URL, LOG_LEVEL.
Outputs: running bot process, logs, DB/Redis connections.
Risk Level: High — lifecycle and graceful shutdown critical; mixing sync/async drivers is dangerous.

## File: D:\0\0.1\slh-telegram-bot\init_db.py
Purpose: Database initialization and migrations helper; creates required tables and seeds initial data.
Dependencies: asyncpg or psycopg2; dotenv; SQL scripts or ORM migrations.
Inputs: DATABASE_URL, migration scripts.
Outputs: created tables, seeded rows, migration logs.
Risk Level: High — destructive migrations can corrupt data; run with backups and snapshots.
## File: FullName                                                                                Length LastWriteTime       
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:18:56
## File: --------                                                                                ------ -------------       
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:00
## File: D:\0\0.1\slh-telegram-bot\src\create_tables.py                                             268 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:02
## File: D:\0\0.1\slh-telegram-bot\src\dashboard.py                                                5060 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:06
## File: D:\0\0.1\slh-telegram-bot\src\main.py                                                       47 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:10
## File: D:\0\0.1\slh-telegram-bot\src\router_loader.py                                             257 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:14
## File: D:\0\0.1\slh-telegram-bot\src\webhook_server.py                                           1163 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:19
## File: D:\0\0.1\slh-telegram-bot\src\webhook_server.py.bak                                        812 6/21/2026 1:18:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:22
## File: D:\0\0.1\slh-telegram-bot\src\__init__.py                                                    0 6/5/2026 12:20:16 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:25
## File: D:\0\0.1\slh-telegram-bot\src\bot\__init__.py                                                0 6/5/2026 12:20:16 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:19:29
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\database.py                                           662 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:13
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\fsm_storage.py                                        218 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:15
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\redis_client.py                                       286 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:18
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\__init__.py                                             0 6/5/2026 12:20:16 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:22
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\__pycache__\database.cpython-310.pyc                  676 6/21/2026 1:18:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:26
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\__pycache__\fsm_storage.cpython-310.pyc               394 6/21/2026 1:18:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:29
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\__pycache__\redis_client.cpython-310.pyc              686 6/21/2026 1:18:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:32
## File: D:\0\0.1\slh-telegram-bot\src\bot\db\__pycache__\__init__.cpython-310.pyc                  153 6/21/2026 1:18:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:36
## File: D:\0\0.1\slh-telegram-bot\src\bot\handlers\buttons_demo.py                                 541 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:40
## File: D:\0\0.1\slh-telegram-bot\src\bot\handlers\fsm_demo.py                                    1617 6/21/2026 1:21:07 PM
Purpose: <short description of file purpose>
Dependencies: <list dependencies, e.g., asyncio; dotenv; asyncpg; redis; etc.>
Inputs: <env vars, CLI flags, request payloads>
Outputs: <files, DB changes, API responses, logs>
Risk Level: <Low/Medium/High — note why>
Last Analyzed: 2026-06-21 16:27:44
