
---

# 💻 3️⃣ `audit.py`

```python
import os
import json
import hashlib

REPORT_FILE = "report.json"

# =========================
# Password Check
# =========================
def check_passwords():
    weak = []
    sample_passwords = ["123456", "password", "admin", "StrongPass123!"]

    for pwd in sample_passwords:
        if len(pwd) < 8 or pwd.islower() or pwd.isdigit():
            weak.append(pwd)

    return weak


# =========================
# Log Analysis
# =========================
def analyze_logs():
    suspicious = []
    log_lines = [
        "Login successful",
        "Failed login attempt",
        "Unauthorized access",
        "System OK"
    ]

    keywords = ["failed", "unauthorized"]

    for line in log_lines:
        for key in keywords:
            if key in line.lower():
                suspicious.append(line)

    return suspicious


# =========================
# File Integrity
# =========================
def check_files():
    results = {}
    files = ["audit.py"]

    for file in files:
        if os.path.exists(file):
            with open(file, "rb") as f:
                data = f.read()
                hash_value = hashlib.sha256(data).hexdigest()
                results[file] = hash_value
        else:
            results[file] = "missing"

    return results


# =========================
# Generate Report
# =========================
def generate_report():
    report = {
        "weak_passwords": check_passwords(),
        "suspicious_logs": analyze_logs(),
        "file_integrity": check_files()
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print("Audit report generated.")


# =========================
# Main
# =========================
if __name__ == "__main__":
    generate_report()
