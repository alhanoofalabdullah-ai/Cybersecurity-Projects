
## 3) `main.py`

```python
import json
import os
from datetime import datetime

RULES_FILE = "rules.json"
DEFAULT_POLICY = "DENY"


# =========================
# File Handling
# =========================
def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as file:
            return json.load(file)
    return []


def save_rules(rules):
    with open(RULES_FILE, "w") as file:
        json.dump(rules, file, indent=4)


rules = load_rules()


# =========================
# Utilities
# =========================
def generate_id():
    return max([rule["id"] for rule in rules], default=0) + 1


def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def validate_port(port):
    return 1 <= port <= 65535


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


# =========================
# Rule Management
# =========================
def add_rule():
    print("\n=== Add Firewall Rule ===")
    action = input("Action (ALLOW/DENY): ").strip().upper()
    source_ip = input("Source IP (or ANY): ").strip().upper()
    dest_ip = input("Destination IP (or ANY): ").strip().upper()
    protocol = input("Protocol (TCP/UDP/ANY): ").strip().upper()

    try:
        port_input = input("Port (1-65535 or ANY): ").strip().upper()
        port = "ANY" if port_input == "ANY" else int(port_input)
    except ValueError:
        print("❌ Invalid port.")
        return

    if action not in ["ALLOW", "DENY"]:
        print("❌ Invalid action.")
        return

    if source_ip != "ANY" and not validate_ip(source_ip):
        print("❌ Invalid source IP.")
        return

    if dest_ip != "ANY" and not validate_ip(dest_ip):
        print("❌ Invalid destination IP.")
        return

    if protocol not in ["TCP", "UDP", "ANY"]:
        print("❌ Invalid protocol.")
        return

    if port != "ANY" and not validate_port(port):
        print("❌ Invalid port range.")
        return

    rule = {
        "id": generate_id(),
        "action": action,
        "source_ip": source_ip,
        "dest_ip": dest_ip,
        "protocol": protocol,
        "port": port
    }

    rules.append(rule)
    save_rules(rules)
    log_event(f"Rule added: {rule}")


def view_rules():
    print("\n=== Firewall Rules ===")
    if not rules:
        print("No rules found.")
        return

    for rule in rules:
        print(
            f"ID: {rule['id']} | "
            f"ACTION: {rule['action']} | "
            f"SRC: {rule['source_ip']} | "
            f"DST: {rule['dest_ip']} | "
            f"PROTO: {rule['protocol']} | "
            f"PORT: {rule['port']}"
        )


def delete_rule():
    print("\n=== Delete Rule ===")
    try:
        rule_id = int(input("Enter rule ID: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    rule = next((r for r in rules if r["id"] == rule_id), None)

    if rule:
        rules.remove(rule)
        save_rules(rules)
        log_event(f"Rule deleted: {rule}")
    else:
        print("❌ Rule not found.")


# =========================
# Matching Logic
# =========================
def match_ip(rule_ip, packet_ip):
    return rule_ip == "ANY" or rule_ip == packet_ip


def match_protocol(rule_protocol, packet_protocol):
    return rule_protocol == "ANY" or rule_protocol == packet_protocol


def match_port(rule_port, packet_port):
    return rule_port == "ANY" or rule_port == packet_port


def evaluate_packet(packet):
    for rule in rules:
        if (
            match_ip(rule["source_ip"], packet["source_ip"]) and
            match_ip(rule["dest_ip"], packet["dest_ip"]) and
            match_protocol(rule["protocol"], packet["protocol"]) and
            match_port(rule["port"], packet["port"])
        ):
            return rule["action"], rule["id"]

    return DEFAULT_POLICY, None


# =========================
# Traffic Simulation
# =========================
def simulate_traffic():
    print("\n=== Simulate Traffic ===")
    source_ip = input("Source IP: ").strip()
    dest_ip = input("Destination IP: ").strip()
    protocol = input("Protocol (TCP/UDP): ").strip().upper()

    try:
        port = int(input("Port: ").strip())
    except ValueError:
        print("❌ Invalid port.")
        return

    if not validate_ip(source_ip):
        print("❌ Invalid source IP.")
        return

    if not validate_ip(dest_ip):
        print("❌ Invalid destination IP.")
        return

    if protocol not in ["TCP", "UDP"]:
        print("❌ Invalid protocol.")
        return

    if not validate_port(port):
        print("❌ Invalid port.")
        return

    packet = {
        "source_ip": source_ip,
        "dest_ip": dest_ip,
        "protocol": protocol,
        "port": port
    }

    action, rule_id = evaluate_packet(packet)

    if rule_id:
        log_event(f"Packet matched rule {rule_id}: {action}")
    else:
        log_event(f"Packet matched no rule: {action} by default policy")

    print("\n=== Result ===")
    print(f"Packet: {packet}")
    print(f"Decision: {action}")


# =========================
# Reports
# =========================
def show_summary():
    print("\n=== Firewall Summary ===")
    allow_count = sum(1 for r in rules if r["action"] == "ALLOW")
    deny_count = sum(1 for r in rules if r["action"] == "DENY")

    print(f"Total rules : {len(rules)}")
    print(f"ALLOW rules : {allow_count}")
    print(f"DENY rules  : {deny_count}")
    print(f"Default policy: {DEFAULT_POLICY}")


# =========================
# Menu
# =========================
def menu():
    while True:
        print("\n=== Firewall Rules Simulator Pro ===")
        print("1. Add Rule")
        print("2. View Rules")
        print("3. Delete Rule")
        print("4. Simulate Traffic")
        print("5. Show Summary")
        print("6. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_rule()
        elif choice == "2":
            view_rules()
        elif choice == "3":
            delete_rule()
        elif choice == "4":
            simulate_traffic()
        elif choice == "5":
            show_summary()
        elif choice == "6":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    menu()
