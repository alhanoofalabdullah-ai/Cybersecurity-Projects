#!/bin/bash

# =========================
# Security Audit Script
# =========================

echo "Checking system security..."

# Check firewall status
echo "\nFirewall Status:"
sudo ufw status

# Check if root login is disabled in SSH configuration
echo "\nSSH Root Login Configuration:"
grep PermitRootLogin /etc/ssh/sshd_config

# Check permissions of sensitive files
echo "\nSensitive File Permissions:"
ls -l /etc/shadow
ls -l /etc/passwd

# Display currently running services (top 10)
echo "\nRunning Services:"
systemctl list-units --type=service --state=running | head -10
