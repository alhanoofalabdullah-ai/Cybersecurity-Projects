import os


def load_lines(filename):
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]


def main():
    headers = load_lines("email_headers.txt")
    suspicious_domains = load_lines("suspicious_domains.txt")

    if not headers:
        print("No email headers found.")
        return

    print("\nAnalyzing email headers...\n")

    detected_domains = []

    for header in headers:
        for domain in suspicious_domains:
            if domain in header:
                detected_domains.append(domain)

    if detected_domains:
        print("Suspicious sender domains detected:\n")
        for domain in set(detected_domains):
            print(f"- {domain}")
    else:
        print("No suspicious domains found.")

    print("\nEmail header analysis completed.")


if __name__ == "__main__":
    main()
