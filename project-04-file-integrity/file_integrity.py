import hashlib
import json
import os

BASELINE_FILE = "baseline.json"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None


def create_baseline(directory):
    baseline = {}

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hash = calculate_hash(path)
            if file_hash:
                baseline[path] = file_hash

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print("Baseline created successfully.")


def check_integrity():
    if not os.path.exists(BASELINE_FILE):
        print("Baseline not found. Create it first.")
        return

    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    for path, old_hash in baseline.items():
        if not os.path.exists(path):
            print(f"[DELETED] {path}")
            continue

        new_hash = calculate_hash(path)

        if new_hash != old_hash:
            print(f"[MODIFIED] {path}")


def main():
    print("1. Create baseline")
    print("2. Check integrity")

    choice = input("Select option: ")

    if choice == "1":
        directory = input("Enter directory to monitor: ")
        create_baseline(directory)

    elif choice == "2":
        check_integrity()


if __name__ == "__main__":
    main()
