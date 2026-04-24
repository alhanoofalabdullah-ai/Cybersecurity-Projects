import os


def load_lines(filename):
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def main():
    logs = load_lines("security_logs.txt")
    keywords = load_lines("alert_keywords.txt")

    if not logs:
        print("No security logs found.")
        return

    print("\nScanning security logs...\n")

    alerts = []

    for log in logs:
        for keyword in keywords:
            if keyword.lower() in log.lower():
                alerts.append(log)

    if alerts:
        print("⚠ Security Alerts Detected:\n")
        for alert in alerts:
            print(f"- {alert}")
    else:
        print("✓ No suspicious activity found.")


if __name__ == "__main__":
    main()
