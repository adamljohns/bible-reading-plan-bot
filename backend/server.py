#!/usr/bin/env python3
"""
Watchman's Bible Reading Plan — Backend API
Handles user registration, plan delivery, and profile management.

Runs on Mac Mini (always-on worker node).
Endpoints:
  POST /api/register   — Save intake form data
  GET  /api/profile     — Lookup profile by email
  POST /api/profile     — Update profile
  GET  /api/reading     — Get today's reading for a user
  GET  /api/health      — Health check
"""

import json
import sqlite3
import os
from datetime import datetime, date, timedelta
from pathlib import Path

try:
    from flask import Flask, request, jsonify
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("Flask not installed. Run: pip3 install flask")
    print("For now, this module provides the database functions only.")

DB_PATH = Path(__file__).parent / "watchman.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
SCHEDULE_PATH = Path(__file__).parent.parent / "schedule.json"


def get_db():
    """Get database connection, creating tables if needed."""
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    if not Path(DB_PATH).exists() or os.path.getsize(str(DB_PATH)) == 0:
        with open(SCHEMA_PATH) as f:
            db.executescript(f.read())
    return db


def init_db():
    """Initialize the database with schema."""
    db = sqlite3.connect(str(DB_PATH))
    with open(SCHEMA_PATH) as f:
        db.executescript(f.read())
    db.close()
    print(f"Database initialized at {DB_PATH}")


def load_schedule():
    """Load the Bible reading schedule from JSON."""
    if SCHEDULE_PATH.exists():
        with open(SCHEDULE_PATH) as f:
            return json.load(f)
    return {}


def register_user(email, first_name, last_name, tier, config, start_date,
                   start_mode='beginning', delivery_method='email', telegram_handle=''):
    """Register a new user or update existing."""
    db = get_db()
    try:
        db.execute("""
            INSERT INTO users (email, first_name, last_name, tier, config_json,
                              start_date, start_mode, delivery_method, telegram_handle)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                tier=excluded.tier,
                config_json=excluded.config_json,
                start_date=excluded.start_date,
                start_mode=excluded.start_mode,
                delivery_method=excluded.delivery_method,
                telegram_handle=excluded.telegram_handle,
                updated_at=CURRENT_TIMESTAMP
        """, (email, first_name, last_name, tier, json.dumps(config),
              start_date, start_mode, delivery_method, telegram_handle))
        db.commit()
        return {"status": "ok", "email": email}
    finally:
        db.close()


def get_user_by_email(email):
    """Lookup user profile by email."""
    db = get_db()
    try:
        row = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if row:
            return dict(row)
        return None
    finally:
        db.close()


def get_todays_reading(user_id, start_date_str, start_mode):
    """Calculate which day of the plan the user is on and return readings."""
    schedule = load_schedule()
    if not schedule:
        return {"error": "Schedule not loaded"}

    start = date.fromisoformat(start_date_str)
    today = date.today()
    days_elapsed = (today - start).days

    if start_mode == 'beginning':
        # Day 1 = January 1 readings, regardless of calendar
        plan_day = days_elapsed + 1
    else:
        # Concurrent: map to actual calendar position
        # January 1 = Day 1, so find current day of year
        plan_day = today.timetuple().tm_yday

    if plan_day < 1:
        return {"message": "Your plan hasn't started yet!", "starts": start_date_str}
    if plan_day > 365:
        plan_day = ((plan_day - 1) % 365) + 1  # Wrap around

    # Map plan_day to month/day key in schedule
    target_date = date(today.year, 1, 1) + timedelta(days=plan_day - 1)
    month_name = target_date.strftime("%B")
    day_num = target_date.day
    key = f"{month_name} {day_num}"

    readings = schedule.get(key, [])
    return {
        "plan_day": plan_day,
        "calendar_key": key,
        "readings": readings,
        "days_elapsed": days_elapsed
    }


def get_users_needing_readings():
    """Get all active users who need today's reading."""
    db = get_db()
    try:
        today = date.today().isoformat()
        rows = db.execute("""
            SELECT u.* FROM users u
            WHERE u.is_active = 1
            AND u.start_date <= ?
            AND NOT EXISTS (
                SELECT 1 FROM readings_sent rs
                WHERE rs.user_id = u.id AND rs.calendar_date = ?
            )
        """, (today, today)).fetchall()
        return [dict(r) for r in rows]
    finally:
        db.close()


def record_reading_sent(user_id, plan_day, calendar_date, passages, delivered=True, error=''):
    """Record that a reading was sent to a user."""
    db = get_db()
    try:
        db.execute("""
            INSERT INTO readings_sent (user_id, plan_day, calendar_date, passages, delivered, delivery_error)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, plan_day, calendar_date, json.dumps(passages), 1 if delivered else 0, error))
        db.commit()
    finally:
        db.close()


# ─── Flask API (if available) ────────────────────────────────────────

if HAS_FLASK:
    app = Flask(__name__)

    @app.route('/api/health')
    def health():
        return jsonify({"status": "ok", "service": "watchman-backend", "time": datetime.now().isoformat()})

    @app.route('/api/register', methods=['POST'])
    def api_register():
        data = request.json
        if not data or not data.get('email') or not data.get('firstName'):
            return jsonify({"error": "email and firstName required"}), 400

        result = register_user(
            email=data['email'],
            first_name=data['firstName'],
            last_name=data.get('lastName', ''),
            tier=data.get('tier', 'basic'),
            config=data,
            start_date=data.get('startDate', date.today().isoformat()),
            start_mode=data.get('startMode', 'beginning'),
            delivery_method=data.get('deliveryMethod', 'email'),
            telegram_handle=data.get('telegramHandle', '')
        )
        return jsonify(result)

    @app.route('/api/profile', methods=['GET'])
    def api_get_profile():
        email = request.args.get('email')
        if not email:
            return jsonify({"error": "email parameter required"}), 400
        user = get_user_by_email(email)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user)

    @app.route('/api/profile', methods=['POST'])
    def api_update_profile():
        data = request.json
        if not data or not data.get('email'):
            return jsonify({"error": "email required"}), 400
        result = register_user(
            email=data['email'],
            first_name=data.get('firstName', ''),
            last_name=data.get('lastName', ''),
            tier=data.get('tier', 'basic'),
            config=data,
            start_date=data.get('startDate', date.today().isoformat()),
            start_mode=data.get('startMode', 'beginning'),
            delivery_method=data.get('deliveryMethod', 'email'),
            telegram_handle=data.get('telegramHandle', '')
        )
        return jsonify(result)

    @app.route('/api/reading', methods=['GET'])
    def api_reading():
        email = request.args.get('email')
        if not email:
            return jsonify({"error": "email parameter required"}), 400
        user = get_user_by_email(email)
        if not user:
            return jsonify({"error": "User not found"}), 404
        reading = get_todays_reading(user['id'], user['start_date'], user['start_mode'])
        return jsonify(reading)


def main():
    """Initialize DB and optionally start Flask server."""
    init_db()
    if HAS_FLASK:
        print("Starting Watchman Backend on port 5000...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Database initialized. Install Flask to run the API server:")
        print("  pip3 install flask")


if __name__ == '__main__':
    main()
