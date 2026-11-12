"""SQLite idempotency keys for repeatable command processing."""
import hashlib,json,sqlite3
def initialize(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS commands (request_key TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, response TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS counters (name TEXT PRIMARY KEY, value INTEGER NOT NULL)")
def increment(conn,key,name,amount=1):
    if not key or not name or type(amount) is not int or amount<=0: raise ValueError("invalid command")
    payload=json.dumps([name,amount],separators=(",",":"))
    fingerprint=hashlib.sha256(payload.encode()).hexdigest()
    with conn:
        row=conn.execute("SELECT fingerprint,response FROM commands WHERE request_key=?",(key,)).fetchone()
        if row:
            if row[0]!=fingerprint: raise ValueError("idempotency key reused with different payload")
            return json.loads(row[1])
        conn.execute("INSERT INTO counters(name,value) VALUES(?,?) ON CONFLICT(name) DO UPDATE SET value=value+excluded.value",(name,amount))
        total=conn.execute("SELECT value FROM counters WHERE name=?",(name,)).fetchone()[0]
        response={"name":name,"value":total}
        conn.execute("INSERT INTO commands VALUES(?,?,?)",(key,fingerprint,json.dumps(response)))
        return response
if __name__=="__main__":
    c=sqlite3.connect(":memory:");initialize(c);print(increment(c,"request-1","views"))
