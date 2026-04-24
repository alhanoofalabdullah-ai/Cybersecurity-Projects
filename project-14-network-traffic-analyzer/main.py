import os


def load_file_lines(filename):
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def main():
    traffic_logs = load_file_lines("traffic_logs.txt")
    suspicious_ips = load_file_lines("suspicious_ips.txt")

    if not traffic_logs:
        print("No traffic logs found.")
        return

    print("\nAnalyzing network traffic...\n")

    detected = []

    for log in traffic_logs:
        for ip in suspicious_ips:
            if ip in log:
                detected.append(ip)

    if detected:
        print("⚠ Suspicious IP activity detected:\n")
        for ip in set(detected):
            print(f"- {ip}")
    else:
        print("✓ No suspicious IP activity found.")


if __name__ == "__main__":
    main()
