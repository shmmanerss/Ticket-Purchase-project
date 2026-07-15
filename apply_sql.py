import sqlite3
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
db_path  = BASE / "tickets.db"
sql_path = BASE / "init_events.sql"

conn = sqlite3.connect(db_path)
with open(sql_path, encoding="utf-8") as f:
    conn.executescript(f.read())
conn.commit()
conn.close()

print("✅ init_events.sql успешно применён")
