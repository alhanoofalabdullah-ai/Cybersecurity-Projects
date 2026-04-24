import os


def load_passwords():
    if not os.path.exists("leaked_passwords.txt"):
        return []

    with open("leaked_passwords.txt", "r") as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]


def main():
    leaked_passwords = load_passwords()

    password = input("Enter password to check: ").strip().lower()

    if not password:
        print("Password cannot be empty.")
        return

    print("\nChecking password security...\n")

    if password in leaked_passwords:
        print("⚠ Warning: This password exists in leaked password databases!")
        print("Please change it immediately.")
    else:
        print("✓ Password not found in leaked list.")
        print("This password appears safer.")


if __name__ == "__main__":
    main()
