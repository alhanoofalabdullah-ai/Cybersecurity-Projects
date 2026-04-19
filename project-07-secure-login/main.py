
---

# 💻 4️⃣ main.py

```python
import json
import os
import hashlib
from datetime import datetime

USERS_FILE = "users.json"
LOG_FILE = "logs.txt"
MAX_ATTEMPTS = 3


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


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


users = load_users()


# =========================
# Security Functions
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def find_user(username):
    return next((u for u in users if u["username"] == username), None)


# =========================
# Registration
# =========================
def register():
    print("\n=== Register ===")
    username = input("Username: ")

    if find_user(username):
        print("❌ User already exists.")
        return

    password = input("Password: ")
    confirm = input("Confirm Password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    user = {
        "id": len(users) + 1,
        "username": username,
        "password": hash_password(password),
        "attempts": 0,
        "locked": False
    }

    users.append(user)
    save_users(users)

    log_event(f"User registered: {username}")
    print("✅ Registration successful.")


# =========================
# Login
# =========================
def login():
    print("\n=== Login ===")
    username = input("Username: ")
    password = input("Password: ")

    user = find_user(username)

    if not user:
        print("❌ User not found.")
        log_event(f"Login failed (user not found): {username}")
        return

    if user["locked"]:
        print("🔒 Account is locked.")
        log_event(f"Login attempt on locked account: {username}")
        return

    if user["password"] == hash_password(password):
        print("✅ Login successful.")
        user["attempts"] = 0
        save_users(users)
        log_event(f"Login success: {username}")
        user_session(username)
    else:
        user["attempts"] += 1
        print("❌ Incorrect password.")

        if user["attempts"] >= MAX_ATTEMPTS:
            user["locked"] = True
            print("🔒 Account locked due to multiple failed attempts.")
            log_event(f"Account locked: {username}")

        save_users(users)
        log_event(f"Login failed: {username}")


# =========================
# Session Simulation
# =========================
def user_session(username):
    while True:
        print(f"\nWelcome {username}")
        print("1. View Profile")
        print("2. Logout")

        choice = input("Choose: ")

        if choice == "1":
            print(f"User: {username}")
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("❌ Invalid option.")


# =========================
# Admin Tools
# =========================
def unlock_user():
    username = input("Enter username to unlock: ")
    user = find_user(username)

    if user:
        user["locked"] = False
        user["attempts"] = 0
        save_users(users)
        print("✅ Account unlocked.")
        log_event(f"Account unlocked: {username}")
    else:
        print("❌ User not found.")


def list_users():
    print("\n=== Users ===")
    for u in users:
        print(f"{u['username']} | Locked: {u['locked']} | Attempts: {u['attempts']}")


# =========================
# Menu
# =========================
def menu():
    while True:
        print("\n=== Secure Login System ===")
        print("1. Register")
        print("2. Login")
        print("3. Unlock User (Admin)")
        print("4. List Users")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            unlock_user()
        elif choice == "4":
            list_users()
        elif choice == "5":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    menu()
