import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import sqlite3
DB_PATH = "ticket_complete_project/tickets.db"

def test_invalid_sql_raises():
    conn = sqlite3.connect(DB_PATH)
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("INVALID SQL")
def test_insert_invalid_table():
    import sqlite3
    import pytest
    DB_PATH = "ticket_complete_project/tickets.db"
    conn = sqlite3.connect(DB_PATH)
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("INSERT INTO non_existing_table VALUES (1)")
