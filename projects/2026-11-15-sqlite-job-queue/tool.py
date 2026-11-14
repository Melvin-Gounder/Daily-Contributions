"""SQLite queue with lease-based at-least-once delivery."""
import json
import sqlite3
import time

def initialize(db):
    db.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY, payload TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'ready',
        lease_until REAL, attempts INTEGER NOT NULL DEFAULT 0)""")
    db.commit()

def enqueue(db, payload):
    with db:
        cursor=db.execute("INSERT INTO jobs(payload) VALUES(?)",(json.dumps(payload),))
        return cursor.lastrowid

def claim(db, now=None, lease_seconds=30):
    if lease_seconds <= 0: raise ValueError("lease must be positive")
    now = time.time() if now is None else now
    with db:
        row=db.execute("""SELECT id,payload FROM jobs
            WHERE state='ready' OR (state='leased' AND lease_until <= ?)
            ORDER BY id LIMIT 1""",(now,)).fetchone()
        if row is None: return None
        db.execute("""UPDATE jobs SET state='leased',lease_until=?,attempts=attempts+1
            WHERE id=?""",(now+lease_seconds,row[0]))
        return row[0],json.loads(row[1])

def acknowledge(db, job_id, now=None):
    now = time.time() if now is None else now
    with db:
        cursor=db.execute("""UPDATE jobs SET state='done',lease_until=NULL
            WHERE id=? AND state='leased' AND lease_until > ?""",(job_id,now))
        return cursor.rowcount == 1

if __name__ == "__main__":
    with sqlite3.connect(":memory:") as db:
        initialize(db)
        enqueue(db,{"task":"send report"})
        print(claim(db))
