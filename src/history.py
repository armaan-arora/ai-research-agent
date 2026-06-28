import sqlite3
import json
from datetime import datetime

DB_FILE = "research_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            overall_score INTEGER,
            report TEXT NOT NULL,
            evaluation TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_history():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT topic, timestamp, overall_score, report, evaluation 
        FROM history 
        ORDER BY id DESC 
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "topic": row[0],
            "timestamp": row[1],
            "overall_score": row[2],
            "report": row[3],
            "evaluation": json.loads(row[4]) if row[4] else {}
        })
    return history

def save_to_history(topic, report, evaluation):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (topic, timestamp, overall_score, report, evaluation)
        VALUES (?, ?, ?, ?, ?)
    """, (
        topic,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        evaluation.get("overall", 0),
        report,
        json.dumps(evaluation)
    ))
    conn.commit()
    conn.close()

def clear_history():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()