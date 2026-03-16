import sqlite3
from datetime import datetime, timedelta
import os

DB_PATH = "ops.db"

INCIDENT_TYPES = [
    "TradeBreak",
    "LateReport",
    "LimitBreach",
    "SystemOutage",
    "PricingError",
]

DESKS = [
    "Equities",
    "Macro",
    "Credit",
    "Derivatives",
]

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open("schema.sql", "r") as f:
        cur.executescript(f.read())

    conn.commit()
    conn.close()

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # clear existing rows for easy re-seeding while you iterate
    cur.execute("DELETE FROM incidents")

    now = datetime.utcnow()

    rows = []
    for i in range(20):
        desk = DESKS[i % len(DESKS)]
        itype = INCIDENT_TYPES[i % len(INCIDENT_TYPES)]
        amount = 10_000 + i * 5_000
        status = "open" if i % 3 != 0 else "closed"
        created_at = (now - timedelta(hours=i * 3)).isoformat(timespec="seconds")
        rows.append((desk, itype, amount, status, created_at))

    cur.executemany(
        """
        INSERT INTO incidents (desk, type, amount, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        rows,
    )

    conn.commit()
    conn.close()
    print(f"Seeded {len(rows)} incidents into {DB_PATH}")

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("Creating database...")
        create_db()
    seed_data()
