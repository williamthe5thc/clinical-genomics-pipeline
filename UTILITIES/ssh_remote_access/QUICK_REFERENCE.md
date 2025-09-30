# SSH Quick Reference Card

**Fast reference for common SSH operations with the Clinical Genomics Pipeline**

**📚 Quick Navigation:**
- [← Back to Utilities](../README.md) | [Installation Guide](../INSTALLATION_COMPLETE.md)
- **SSH Docs:** [Setup Guide](README.md) | [Security Guide](SECURITY_GUIDE.md) | [Quick Reference (This Guide)](#)
- [Main Pipeline →](../../MAIN_README.md)

---

## Quick Start Commands

### First Time Setup

```bash
# 1. Run setup script
cd /mnt/d/Genome/UTILITIES/ssh_remote_access
bash setup_ssh_access.sh

# 2. Configure Windows (as Administrator)
cd D:\Genome\UTILITIES\ssh_remote_access
.\setup_port_forwarding.bat

# 3. Test connection
ssh YOUR_USERNAME@localhost -p 2022
```

---

## Connection Commands

### Local Connection (Same Machine)

```bash
# From WSL to WSL
ssh localhost -p 2022

# From Windows PowerShell to WSL
ssh YOUR_USERNAME@localhost -p 2022
```

### Local Network Connection

```bash
# Find your Windows IP first
ipconfig  # On Windows

# Connect from another device
ssh YOUR_USERNAME@192.168.1.XXX -p 2022
```

### With SSH Key

```bash
# Connect using specific key
ssh -i ~/.ssh/id_ed25519 -p 2022 user@server

# Connect and forward port
ssh -L 8080:localhost:8080 -p 2022 user@server
```

---

## SSH Key Management

### Generate New Key

```bash
# Ed25519 (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"

# RSA (if compatibility needed)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### Copy Key to Server

```bash
# Automatic
ssh-copy-id -p 2022 user@server

# Manual
cat ~/.ssh/id_ed25519.pub | ssh -p 2022 user@server \
    "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Test Key Authentication

```bash
ssh -p 2022 user@server
# Should connect without password
```

---

## Service Management

### SSH Service Control

```bash
# Start SSH
sudo service ssh start

# Stop SSH
sudo service ssh stop

# Restart SSH
sudo service ssh restart

# Check status
sudo service ssh status

# Reload config (without disconnecting users)
sudo service ssh reload
```

### Auto-Start on Boot

```bash
# Using systemd (if available)
sudo systemctl enable ssh
sudo systemctl start ssh
```

---

## Configuration

### Edit SSH Config

```bash
# Edit server config
sudo nano /etc/ssh/sshd_config

# Test configuration
sudo sshd -t

# Apply changes
sudo service ssh restart
```

### Client SSH Config

```bash
# Edit client config
nano ~/.ssh/config

# Example entry:
Host genomics
    HostName YOUR_SERVER_IP
    Port 2022
    User YOUR_USERNAME
    IdentityFile ~/.ssh/id_ed25519

# Then connect with:
ssh genomics
```

---

## File Transfer

### SCP (Secure Copy)

```bash
# Upload file to server
scp -P 2022 file.vcf.gz user@server:/mnt/d/Genome/DATA/

# Download file from server
scp -P 2022 user@server:/path/to/file.vcf.gz ./

# Upload directory
scp -P 2022 -r ./directory user@server:/path/

# Download directory
scp -P 2022 -r user@server:/path/directory ./
```

### SFTP (Interactive Transfer)

```bash
# Connect with SFTP
sftp -P 2022 user@server

# SFTP commands:
ls              # List remote files
lls             # List local files
cd /path        # Change remote directory
lcd /path       # Change local directory
get file        # Download file
put file        # Upload file
mget *.vcf.gz   # Download multiple files
mput *.vcf.gz   # Upload multiple files
exit            # Exit SFTP
```

---

## Long-Running Sessions

### Using Screen

```bash
# Start new screen session
screen -S genomics

# Detach from screen: Ctrl+A then D

# List sessions
screen -ls

# Reattach to session
screen -r genomics

# Kill session
screen -X -S genomics quit
```

### Using tmux

```bash
# Start new tmux session
tmux new -s genomics

# Detach: Ctrl+B then D

# List sessions
tmux ls

# Reattach
tmux attach -t genomics

# Kill session
tmux kill-session -t genomics
```

---

## Port Forwarding

### Local Port Forwarding

```bash
# Forward local port 8080 to remote localhost:8080
ssh -L 8080:localhost:8080 -p 2022 user@server

# Access remote web interface at http://localhost:8080
```

### Remote Port Forwarding

```bash
# Forward remote port 9090 to local localhost:9090
ssh -R 9090:localhost:9090 -p 2022 user@server
```

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
# Create SOCKS proxy on local port 1080
ssh -D 1080 -p 2022 user@server
```

---

## Pipeline Operations

### Run Pipeline Remotely

```bash
# Connect to server
ssh -p 2022 user@server

# Navigate to pipeline
cd /mnt/d/Genome

# Run in screen session
screen -S analysis
bash clinical_genomics_pipeline.sh single sample.vcf.gz SAMPLE_001 8

# Detach: Ctrl+A then D
# Disconnect SSH safely
```

### Check Pipeline Status

```bash
# Reconnect
ssh -p 2022 user@server

# Reattach to screen
screen -r analysis

# Or check process directly
ps aux | grep clinical_genomics_pipeline
```

### Download Results

```bash
# From local computer
scp -P 2022 -r user@server:/mnt/d/Genome/DATA/RESULTS/VCF_ANALYSIS/individuals/SAMPLE_001/ ./results/
```

---

## Troubleshooting Commands

### Check SSH Status

```bash
# Service status
sudo service ssh status

# Check if listening
sudo netstat -tulpn | grep :2022

# Check WSL IP
hostname -I
```

### Test Connection

```bash
# Test from WSL to itself
ssh -v -p 2022 localhost

# Check SSH logs
sudo tail -f /var/log/auth.log

# View recent connections
sudo grep "Accepted\|Failed" /var/log/auth.log | tail -20
```

### Port Forwarding Check (Windows)

```powershell
# View port forwarding rules
netsh interface portproxy show v4tov4

# View firewall rules
netsh advfirewall firewall show rule name="WSL SSH"
```

### Common Fixes

```bash
# Regenerate host keys
sudo rm /etc/ssh/ssh_host_*
sudo dpkg-reconfigure openssh-server
sudo service ssh restart

# Fix permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# Reset known_hosts (if host key changed)
ssh-keygen -R [hostname]
```

---

## Security Commands

### fail2ban Management

```bash
# Check status
sudo fail2ban-client status sshd

# Show banned IPs
sudo fail2ban-client get sshd banned

# Unban IP
sudo fail2ban-client set sshd unbanip IP_ADDRESS

# Restart fail2ban
sudo service fail2ban restart
```

### Monitor Access

```bash
# Who's currently logged in
who
w

# Recent logins
last -a

# Failed login attempts
sudo grep "Failed password" /var/log/auth.log | tail -20

# Successful logins today
sudo grep "Accepted password" /var/log/auth.log | grep "$(date +%b\ %d)"
```

### Firewall (ufw)

```bash
# Status
sudo ufw status verbose

# Allow SSH
sudo ufw allow 2022/tcp

# Allow from specific IP
sudo ufw allow from 192.168.1.100 to any port 2022

# Delete rule
sudo ufw delete allow 2022/tcp

# Enable/disable
sudo ufw enable
sudo ufw disable
```

---

## Windows Port Forwarding (PowerShell)

### Setup Port Forwarding

```powershell
# Get WSL IP
wsl hostname -I

# Add port forwarding (as Administrator)
netsh interface portproxy add v4tov4 listenport=2022 listenaddress=0.0.0.0 connectport=2022 connectaddress=WSL_IP

# View rules
netsh interface portproxy show v4tov4

# Delete rule
netsh interface portproxy delete v4tov4 listenport=2022 listenaddress=0.0.0.0
```

### Firewall Rules

```powershell
# Add rule (as Administrator)
netsh advfirewall firewall add rule name="WSL SSH" dir=in action=allow protocol=TCP localport=2022

# View rule
netsh advfirewall firewall show rule name="WSL SSH"

# Delete rule
netsh advfirewall firewall delete rule name="WSL SSH"
```

---

## Convenience Scripts

```bash
# All scripts in: /mnt/d/Genome/UTILITIES/ssh_remote_access/

# Restart SSH
bash restart_ssh.sh

# Test connection
bash test_ssh_connection.sh

# Show connection info
bash show_connection_info.sh
```

---

## Common Scenarios

### Scenario: Access Pipeline from Home

```bash
# 1. Ensure SSH is running on work computer
# 2. Get work computer's public IP (https://whatismyipaddress.com)
# 3. Configure router port forwarding (2022 → work computer)
# 4. Connect from home
ssh -p 2022 user@WORK_PUBLIC_IP
```

### Scenario: Run Long Analysis Remotely

```bash
# Connect
ssh -p 2022 user@server

# Start screen
screen -S myanalysis

# Run pipeline
cd /mnt/d/Genome
bash clinical_genomics_pipeline.sh single sample.vcf.gz SAMPLE_001 8

# Detach: Ctrl+A, D
# Disconnect: exit

# Later, reconnect and check
ssh -p 2022 user@server
screen -r myanalysis
```

### Scenario: Copy Results Back

```bash
# From local computer
scp -P 2022 -r user@server:/mnt/d/Genome/DATA/RESULTS/VCF_ANALYSIS/individuals/SAMPLE_001/ ./

# Or use rsync for resumable transfer
rsync -avz -e "ssh -p 2022" user@server:/mnt/d/Genome/DATA/RESULTS/ ./results/
```

### Scenario: Locked Out Recovery

```cmd
REM From Windows Command Prompt
wsl -u root

# Reset password
passwd YOUR_USERNAME

# Or re-enable password auth
nano /etc/ssh/sshd_config
# Set: PasswordAuthentication yes
service ssh restart
```

---

## VS Code Remote Development

### Connect VS Code to Remote WSL

1. Install "Remote - SSH" extension
2. Press `F1` → "Remote-SSH: Connect to Host"
3. Enter: `user@server_ip -p 2022`
4. Open folder: `/mnt/d/Genome`

### VS Code SSH Config

```bash
# Edit: ~/.ssh/config
Host genomics-pipeline
    HostName YOUR_SERVER_IP
    Port 2022
    User YOUR_USERNAME
    IdentityFile ~/.ssh/id_ed25519
```

Then in VS Code: Connect to "genomics-pipeline"

---

## Performance Tips

```bash
# Keep connections alive
# Add to ~/.ssh/config:
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Speed up connections with multiplexing
Host genomics
    ControlMaster auto
    ControlPath ~/.ssh/control-%r@%h:%p
    ControlPersist 1h

# Compress data transfer
ssh -C -p 2022 user@server

# Disable strict host checking for local network
Host 192.168.*.*
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
```

---

## Emergency Reference

### Critical Commands

```bash
# Stop all SSH connections immediately
sudo pkill -u YOUR_USERNAME

# Restart SSH service
sudo service ssh restart

# Check if port is blocked
telnet SERVER_IP 2022

# View active connections
sudo netstat -tnpa | grep :2022
```

### Get Help

```bash
# SSH command help
man ssh

# SSHD config help
man sshd_config

# SCP help
man scp

# Check this guide
cat /mnt/d/Genome/UTILITIES/ssh_remote_access/README.md
```

---

## Quick Diagnostic Script

```bash
#!/bin/bash
# Save as: diagnose_ssh.sh

echo "=== SSH Diagnostic Report ==="
echo ""
echo "SSH Service Status:"
sudo service ssh status | grep Active
echo ""
echo "WSL IP Address:"
hostname -I
echo ""
echo "Listening Ports:"
sudo netstat -tulpn | grep :2022
echo ""
echo "Recent Connections:"
sudo grep "Accepted\|Failed" /var/log/auth.log | tail -5
echo ""
echo "Port Forwarding (run in Windows PowerShell):"
echo "  netsh interface portproxy show v4tov4"
```

---

**Print this page for quick reference!**

**Location:** `/mnt/d/Genome/UTILITIES/ssh_remote_access/QUICK_REFERENCE.md`

**Last Updated:** September 2025
