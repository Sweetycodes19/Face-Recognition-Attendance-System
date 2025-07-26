import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "attendance.db"

# ✅ Ensure the table exists first
def create_table_if_missing():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            time TEXT,
            date TEXT,
            admin TEXT
        )
    """)
    conn.commit()
    conn.close()

# ✅ Ensure correct structure and constraints
def ensure_correct_table():
    create_table_if_missing()  # 👈 Ensure it exists first

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if 'admin' column exists
    cursor.execute("PRAGMA table_info(attendance)")
    cols = [col[1] for col in cursor.fetchall()]

    if "admin" not in cols:
        cursor.execute("ALTER TABLE attendance ADD COLUMN admin TEXT")

    # Check if correct UNIQUE constraint is applied
    cursor.execute("PRAGMA index_list(attendance)")
    indexes = [index[1] for index in cursor.fetchall()]
    has_correct_unique = any("admin" in index and "unique" in index.lower() for index in indexes)

    if not has_correct_unique:
        # Rename old table
        cursor.execute("ALTER TABLE attendance RENAME TO attendance_old")

        # Create new table with correct UNIQUE constraint
        cursor.execute("""
            CREATE TABLE attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                time TEXT,
                date TEXT,
                admin TEXT,
                UNIQUE(name, date, admin)
            )
        """)

        # Copy existing data
        cursor.execute("""
            INSERT OR IGNORE INTO attendance (name, time, date, admin)
            SELECT name, time, date, admin FROM attendance_old
        """)

        cursor.execute("DROP TABLE attendance_old")

    conn.commit()
    conn.close()

# 🔄 Auto-call when importing
ensure_correct_table()

# ✅ Mark attendance (only if not already present)
def mark_attendance(name, admin="Unknown"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Check for existing entry
    cursor.execute("SELECT * FROM attendance WHERE name=? AND date=? AND admin=?", (name, date_str, admin))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO attendance (name, time, date, admin) VALUES (?, ?, ?, ?)",
            (name, time_str, date_str, admin)
        )
        conn.commit()

    conn.close()

# 📊 Return full DataFrame
def get_attendance_df():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    conn.close()
    return df
