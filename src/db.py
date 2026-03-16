import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any

DB_PATH = "ops.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def row_to_dict(row) -> Dict[str, Any]:
    return {
        "id": row[0],
        "desk": row[1],
        "type": row[2],
        "amount": row[3],
        "status": row[4],
        "created_at": row[5],
    }


def get_recent_open_incidents(hours: int = 24) -> List[Dict[str, Any]]:
    """
    Returns open incidents in the last `hours` hours, newest first.
    """
    conn = get_connection()
    cur = conn.cursor()

    cutoff = datetime.utcnow() - timedelta(hours=hours)
    cutoff_str = cutoff.isoformat(timespec="seconds")

    cur.execute(
        """
        SELECT id, desk, type, amount, status, created_at
        FROM incidents
        WHERE status = 'open' AND created_at >= ?
        ORDER BY created_at DESC
        """,
        (cutoff_str,),
    )

    rows = cur.fetchall()
    conn.close()

    return [row_to_dict(r) for r in rows]


if __name__ == "__main__":
    incidents = get_recent_open_incidents(24)
    print(f"Found {len(incidents)} open incidents in last 24h")
    for inc in incidents:
        print(inc)
