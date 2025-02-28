CREATE TABLE transactions (
    project TEXT NOT NULL,
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    amount NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    success BOOLEAN NOT NULL
);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);

-------------------------------------------------------

CREATE TABLE exchange_rates (
    currency_from TEXT NOT NULL,
    currency_to TEXT NOT NULL,
    exchange_rate NUMERIC NOT NULL,
    currency_date TIMESTAMP NOT NULL
);
CREATE INDEX idx_exchange_rates_date ON exchange_rates(currency_date);
CREATE INDEX idx_exchange_rates_from_date ON exchange_rates(currency_from, currency_date);

-------------------------------------------------------

CREATE TABLE analytics_sessions (
    session_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    events_count INT NOT NULL,
    transactions_sum NUMERIC DEFAULT 0,
    first_successful_transaction_time TIMESTAMP,
    first_successful_transaction_usd NUMERIC DEFAULT 0,
    last_activity_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL
);
CREATE INDEX idx_analytics_sessions_user_id ON analytics_sessions(user_id);
CREATE INDEX idx_analytics_sessions_created_at ON analytics_sessions(created_at);
