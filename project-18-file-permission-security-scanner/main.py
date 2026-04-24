import os
import stat


def check_permissions(folder):
    risky_files = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                permissions = os.stat(file_path).st_mode

                if permissions & stat.S_IWOTH:
                    risky_files.append(file_path)

            except Exception as e:
                print(f"Error checking {file_path}: {e}")

    return risky_files


def main():
    folder = input("Enter folder path to scan: ").strip()

    if not os.path.exists(folder):
        print("Folder not found.")
        return

    print("\nScanning file permissions...\n")

    risky_files = check_permissions(folder)

    if risky_files:
        print("⚠ Risky file permissions detected:\n")
        for file in risky_files:
            print(f"- {file}")
    else:
        print("✓ No dangerous permissions found.")


if __name__ == "__main__":
    main()
