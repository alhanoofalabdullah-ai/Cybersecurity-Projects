
---

# 💻 4️⃣ `app.py`

```python
from flask import Flask, request, jsonify
import hashlib
import json
import os
import uuid

app = Flask(__name__)

USERS_FILE = "users.json"
TOKENS_FILE = "tokens.json"


# =========================
# File Handling
# =========================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def load_tokens():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=4)


# =========================
# Security Helpers
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token():
    return str(uuid.uuid4())


def find_user(username):
    users = load_users()
    return next((u for u in users if u["username"] == username), None)


# =========================
# Routes
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing data"}), 400

    users = load_users()

    if any(u["username"] == data["username"] for u in users):
        return jsonify({"error": "User exists"}), 400

    user = {
        "id": len(users) + 1,
        "username": data["username"],
        "password": hash_password(data["password"])
    }

    users.append(user)
    save_users(users)

    return jsonify({"message": "User registered"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = find_user(data.get("username"))

    if not user or user["password"] != hash_password(data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    tokens = load_tokens()
    token = generate_token()
    tokens[token] = user["username"]
    save_tokens(tokens)

    return jsonify({"token": token})


@app.route("/secure-data", methods=["GET"])
def secure_data():
    token = request.headers.get("Authorization")

    tokens = load_tokens()

    if not token or token not in tokens:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({"data": "This is protected data"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
