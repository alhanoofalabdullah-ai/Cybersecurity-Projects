#!/bin/bash

# =========================
# Linux Hardening Script
# =========================

echo "Starting Linux Hardening..."

# Update system packages to ensure latest security patches
echo "[*] Updating system..."
sudo apt update -y

# Disable insecure or unnecessary services (if installed)
echo "[*] Disabling unnecessary services..."
sudo systemctl disable telnet 2>/dev/null
sudo systemctl disable ftp 2>/dev/null

# Enable firewall (UFW) and configure default policies
echo "[*] Enabling firewall..."
sudo ufw enable
sudo ufw default deny incoming   # Block all incoming traffic
sudo ufw default allow outgoing  # Allow all outgoing traffic

# Secure SSH configuration by disabling root login
echo "[*] Securing SSH configuration..."
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Apply strict permissions to sensitive system files
echo "[*] Setting secure file permissions..."
sudo chmod 600 /etc/shadow   # Only root can read/write
sudo chmod 644 /etc/passwd   # Readable but protected

echo "Hardening completed successfully."
