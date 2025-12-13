CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE facts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    source VARCHAR(255),
    views INT DEFAULT 0,
    score INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE usage_stats (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255),
    method VARCHAR(10),
    status_code INT,
    api_key VARCHAR(255),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
