from flask import Flask, request, jsonify
import sqlite3
import os
import redis
import time

app = Flask(__name__)

# Redis client (for simulation)
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True)

# In-memory "users" DB (for demo) stored in sqlite file
DB_FILE = "/tmp/poc_users.db"

def init_db():
    import sqlite3
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, secret TEXT)")
        c.execute("INSERT INTO users(username, secret) VALUES ('alice', 'alice_secret')")
        c.execute("INSERT INTO users(username, secret) VALUES ('bob', 'bob_secret')")
        conn.commit()
        conn.close()

@app.route("/")
def index():
    return jsonify({"msg": "Vulnerable PoC API. Use endpoints /eval, /reflect, /search, /users"})

# Reflect endpoint (XSS-like vector)
@app.route("/reflect")
def reflect():
    q = request.args.get("q", "")
    # intentionally reflect user input
    return f"<html><body>you said: {q}</body></html>", 200, {'Content-Type': 'text/html'}

# Dangerous eval endpoint (DO NOT USE IN PRODUCTION)
@app.route("/eval")
def do_eval():
    expr = request.args.get("expr", "")
    try:
        # intentionally insecure eval for PoC
        result = eval(expr, {"__builtins__": {}})
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Search endpoint simulating SQL-like behavior (naive)
@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # intentionally vulnerable concatenated SQL (SQLi)
    sql = f"SELECT id, username FROM users WHERE username LIKE '%{q}%'"
    try:
        c.execute(sql)
        rows = c.fetchall()
        conn.close()
        return jsonify({"query": sql, "rows": rows})
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

# Expose users (for demo)
@app.route("/users")
def users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users")
    rows = c.fetchall()
    conn.close()
    return jsonify({"users": rows})

# Redis-backed counter (to show redis use)
@app.route("/visit")
def visit():
    count = r.incr("visits")
    return jsonify({"visits": int(count)})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
