import socket

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            return True
        return False
    except Exception:
        return False

def main():
    target = input("Enter target IP or hostname: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

    for port in range(start_port, end_port + 1):
        if scan_port(target, port):
            print(f"Port {port} is OPEN")
        else:
            print(f"Port {port} is closed")

if __name__ == "__main__":
    main()
