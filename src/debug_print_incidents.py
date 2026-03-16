import sqlite3

conn = sqlite3.connect("ops.db")
cur = conn.cursor()

cur.execute("SELECT id, desk, type, amount, status, created_at FROM incidents ORDER BY created_at DESC")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
