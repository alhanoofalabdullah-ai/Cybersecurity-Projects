import time

# كلمة المرور الصحيحة (simulation)
correct_password = "admin123"

def brute_force():
    attempts = 0
    wordlist = ["123456", "password", "admin", "admin123", "qwerty"]

    print("Starting brute force attack...\n")

    for password in wordlist:
        attempts += 1
        print(f"Trying: {password}")
        time.sleep(0.5)

        if password == correct_password:
            print(f"\n[SUCCESS] Password found: {password}")
            print(f"Attempts: {attempts}")
            return

    print("\n[FAILED] Password not found.")


def main():
    brute_force()


if __name__ == "__main__":
    main()
