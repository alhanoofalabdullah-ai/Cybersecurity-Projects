import os


def load_lines(filename):
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]


def main():
    ssh_config = load_lines("ssh_config.txt")
    risky_settings = load_lines("risky_settings.txt")

    if not ssh_config:
        print("No SSH configuration found.")
        return

    print("\nScanning SSH configuration...\n")

    detected_risks = []

    for line in ssh_config:
        for risk in risky_settings:
            if risk in line:
                detected_risks.append(risk)

    if detected_risks:
        print("Risky SSH settings detected:\n")
        for risk in set(detected_risks):
            print(f"- {risk}")
    else:
        print("No risky SSH settings found.")

    print("\nSSH audit completed.")


if __name__ == "__main__":
    main()
