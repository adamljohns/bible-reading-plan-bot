-- Watchman's Bible Reading Plan — Backend Database Schema
-- SQLite3 | Created: 2026-03-06

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT DEFAULT '',
    tier TEXT NOT NULL CHECK(tier IN ('basic','amplified','deep')),
    config_json TEXT NOT NULL,         -- Full intake answers as JSON
    start_date DATE NOT NULL,          -- When their plan starts
    start_mode TEXT NOT NULL DEFAULT 'beginning',  -- 'beginning' or 'concurrent'
    delivery_method TEXT NOT NULL DEFAULT 'email',  -- 'email', 'telegram', 'pdf'
    telegram_handle TEXT DEFAULT '',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS readings_sent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    plan_day INTEGER NOT NULL,          -- Day 1-365 of chronological plan
    calendar_date DATE NOT NULL,        -- Actual date the reading was sent
    passages TEXT NOT NULL,             -- JSON array of passage refs
    delivered INTEGER DEFAULT 0,        -- 1 = successfully sent
    delivery_error TEXT DEFAULT '',
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schedule (
    plan_day INTEGER PRIMARY KEY,       -- Day 1-365
    month_day TEXT NOT NULL,            -- "January 1", "March 7", etc.
    passages_json TEXT NOT NULL         -- JSON array: ["Genesis 1-2", "Psalm 1"]
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    plan_day INTEGER,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for daily cron lookup
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active, delivery_method);
CREATE INDEX IF NOT EXISTS idx_readings_user_day ON readings_sent(user_id, plan_day);
