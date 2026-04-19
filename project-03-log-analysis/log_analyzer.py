import re

def analyze_logs(file_path):
    suspicious_patterns = [
        "failed",
        "error",
        "unauthorized",
        "invalid",
        "denied"
    ]

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        print("\nAnalyzing logs...\n")

        for line in lines:
            for pattern in suspicious_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    print(f"[ALERT] {line.strip()}")
                    break

    except FileNotFoundError:
        print("Log file not found.")


def main():
    file_path = input("Enter log file path: ")
    analyze_logs(file_path)


if __name__ == "__main__":
    main()
