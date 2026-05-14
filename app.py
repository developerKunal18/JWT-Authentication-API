from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "mysecretkey"

# ---------- Database ----------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

# ---------- Register ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (data["username"], data["password"])
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User registered"
    })

# ---------- Login ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        token = jwt.encode(
            {
                "username": data["username"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "token": token
        })

    return jsonify({
        "message": "Invalid credentials"
    }), 401

# ---------- Protected Route ----------
@app.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({
            "message": "Token missing"
        }), 401

    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return jsonify({
            "message": f"Welcome {decoded['username']}"
        })

    except:
        return jsonify({
            "message": "Invalid token"
        }), 401

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
