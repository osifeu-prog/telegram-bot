CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price_usd NUMERIC(10,2),
    monthly_limit INTEGER,
    features JSONB
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    plan_id INTEGER,
    starts_at TIMESTAMP,
    expires_at TIMESTAMP,
    status TEXT
);

CREATE TABLE IF NOT EXISTS usage_logs (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    event_name TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
