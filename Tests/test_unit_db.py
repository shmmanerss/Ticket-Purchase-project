import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import sqlite3
DB_PATH = "ticket_complete_project/tickets.db"

def test_db_connection():
    conn = sqlite3.connect(DB_PATH)
    assert conn is not None
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert isinstance(tables, list)
def test_query_tables():
    import sqlite3
    DB_PATH = "ticket_complete_project/tickets.db"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "users" in tables or "tickets" in tables
