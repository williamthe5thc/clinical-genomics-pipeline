# SSH Remote Access Setup for WSL

**Secure remote access to your Clinical Genomics Pipeline from anywhere**

**📚 Quick Navigation:**
- [← Back to Utilities](../README.md) | [Installation Guide](../INSTALLATION_COMPLETE.md)
- **SSH Docs:** [Setup (This Guide)](#) | [Security Guide](SECURITY_GUIDE.md) | [Quick Reference](QUICK_REFERENCE.md)
- [Main Pipeline →](../../MAIN_README.md)

---

## Overview

This utility enables secure SSH access to your Clinical Genomics Pipeline running in WSL Ubuntu from remote locations. Whether you're at home, in the lab, or traveling, you can securely connect to your pipeline and run analyses remotely.

### Key Features

✅ **Automated Setup**: One-command installation of SSH server  
✅ **WSL1 & WSL2 Support**: Works with both WSL versions  
✅ **Port Forwarding**: Automatic Windows → WSL network configuration  
✅ **Security-Focused**: Best practices for secure remote access  
✅ **Auto-Start Scripts**: Optional boot-time SSH service startup  
✅ **Convenience Tools**: Quick scripts for common operations  

---

## Quick Start

### Step 1: Run Setup Script (5 minutes)

```bash
cd /mnt/d/Genome/UTILITIES/ssh_remote_access
bash setup_ssh_access.sh
```

This will:
- Install OpenSSH Server in WSL
- Configure SSH for port 2022
- Create Windows configuration scripts
- Set up convenience tools

### Step 2: Configure Windows Port Forwarding (1 minute)

**Open Windows PowerShell or Command Prompt as Administrator:**

```cmd
cd D:\Genome\UTILITIES\ssh_remote_access
.\setup_port_forwarding.bat
```

This configures Windows to forward external connections to your WSL instance.

### Step 3: Test Connection

**From the same Windows machine:**
```bash
ssh YOUR_WSL_USERNAME@localhost -p 2022
```

**From another computer on your network:**
```bash
ssh YOUR_WSL_USERNAME@YOUR_WINDOWS_IP -p 2022
```

**Success!** You should see your WSL prompt. 🎉

---

## Detailed Setup Guide

### Prerequisites

- Windows 10/11 with WSL Ubuntu 22.04+
- Administrator access to Windows
- Basic familiarity with command line

### Installation Steps

#### 1. Install SSH Server in WSL

The automated script handles everything:

```bash
cd /mnt/d/Genome/UTILITIES/ssh_remote_access
bash setup_ssh_access.sh
```

**What this does:**
- Updates system packages
- Installs openssh-server
- Configures SSH to listen on port 2022
- Enables password authentication
- Creates auto-start scripts
- Generates convenience tools

#### 2. Configure Windows Port Forwarding

**Why is this needed?**

WSL2 uses a virtualized network (NAT), meaning it has its own internal IP address that changes on every reboot. Windows port forwarding creates a bridge from your Windows network interface to WSL's internal network.

**Manual Configuration (PowerShell as Administrator):**

```powershell
# Get WSL IP address
wsl hostname -I

# Create port forwarding (replace WSL_IP with actual IP)
netsh interface portproxy add v4tov4 listenport=2022 listenaddress=0.0.0.0 connectport=2022 connectaddress=WSL_IP

# Add firewall rule
netsh advfirewall firewall add rule name="WSL SSH" dir=in action=allow protocol=TCP localport=2022

# Verify configuration
netsh interface portproxy show v4tov4
```

**Automated Script (Recommended):**

```cmd
cd D:\Genome\UTILITIES\ssh_remote_access
.\setup_port_forwarding.bat
```

This script:
- Automatically detects WSL IP
- Removes old port forwarding rules
- Creates new forwarding configuration
- Adds Windows Firewall exception
- Displays connection information

#### 3. Verify SSH is Running

```bash
# Check SSH service status
sudo service ssh status

# Or use convenience script
bash /mnt/d/Genome/UTILITIES/ssh_remote_access/show_connection_info.sh
```

Expected output:
```
SSH Status: Active: active (running)
```

---

## Connection Methods

### Method 1: Local Connection (Same Windows Machine)

```bash
# From WSL itself
ssh localhost -p 2022

# From Windows PowerShell/CMD
ssh YOUR_USERNAME@localhost -p 2022

# From Windows Terminal (WSL tab)
ssh YOUR_USERNAME@localhost -p 2022
```

### Method 2: Local Network Connection

**Find your Windows IP address:**

Windows PowerShell:
```powershell
ipconfig
```

Look for "IPv4 Address" under your active network adapter (Wi-Fi or Ethernet).

**Connect from another device on same network:**

```bash
# From another computer, laptop, or mobile device
ssh YOUR_USERNAME@192.168.1.XXX -p 2022

# Example
ssh bioinfo@192.168.1.100 -p 2022
```

### Method 3: Internet Connection (Requires Router Configuration)

⚠️ **Security Warning**: Only do this if you understand the security implications!

**Requirements:**
- Router admin access
- Static or dynamic DNS service (optional but recommended)

**Steps:**

1. **Find your public IP address:**
   ```
   Visit: https://whatismyipaddress.com/
   ```

2. **Configure router port forwarding:**
   - Log into your router admin panel
   - Navigate to Port Forwarding settings
   - Create new rule:
     - External Port: 2022 (or any port > 1024)
     - Internal Port: 2022
     - Internal IP: Your Windows computer's local IP
     - Protocol: TCP

3. **Connect from anywhere:**
   ```bash
   ssh YOUR_USERNAME@YOUR_PUBLIC_IP -p 2022
   ```

**Recommended**: Use Dynamic DNS service (DynDNS, No-IP) for stable hostname instead of IP address.

---

## Auto-Start Configuration

### Option 1: Windows Task Scheduler (Recommended)

This starts SSH automatically when Windows boots, even before you log in.

**Create Scheduled Task:**

1. Open Task Scheduler (search in Windows Start menu)
2. Click "Create Task" (not "Create Basic Task")
3. **General Tab:**
   - Name: "Start WSL SSH Server"
   - Description: "Auto-start SSH server in WSL for genomics pipeline"
   - Run whether user is logged on or not: ✓
   - Run with highest privileges: ✓

4. **Triggers Tab:**
   - New → Begin the task: At startup
   - OK

5. **Actions Tab:**
   - New → Action: Start a program
   - Program/script: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
   - Add arguments: `-ExecutionPolicy Bypass -File "D:\Genome\UTILITIES\ssh_remote_access\start_wsl_ssh.ps1"`
   - OK

6. **Conditions Tab:**
   - Uncheck "Start the task only if the computer is on AC power"

7. **Settings Tab:**
   - Allow task to be run on demand: ✓
   - Stop the task if it runs longer than: 3 days (or uncheck)

8. Click OK, enter your Windows password when prompted

**Test the task:**
```powershell
# Run manually to test
Get-ScheduledTask -TaskName "Start WSL SSH Server" | Start-ScheduledTask
```

### Option 2: Startup Script

**Create startup shortcut:**

1. Press `Win + R`, type `shell:startup`, press Enter
2. Right-click → New → Shortcut
3. Location: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "D:\Genome\UTILITIES\ssh_remote_access\start_wsl_ssh.ps1"`
4. Name: "WSL SSH Server"
5. Click Finish

**Note**: This only runs when you log into Windows.

### Option 3: Systemd (WSL with systemd support)

If your WSL has systemd enabled (Windows 11 or configured):

```bash
# Enable SSH to start automatically
sudo systemctl enable ssh

# Start SSH now
sudo systemctl start ssh

# Check status
sudo systemctl status ssh
```

---

## Security Best Practices

### 1. Use SSH Key Authentication (Highly Recommended)

**Generate SSH key pair on your client computer:**

```bash
# On your remote computer (laptop, home computer, etc.)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter for default location
# Enter passphrase (recommended) or press Enter for no passphrase
```

**Copy public key to WSL server:**

```bash
# From your remote computer
ssh-copy-id -p 2022 YOUR_USERNAME@YOUR_WINDOWS_IP

# Or manually:
cat ~/.ssh/id_ed25519.pub | ssh -p 2022 YOUR_USERNAME@YOUR_WINDOWS_IP "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Test key-based authentication:**

```bash
ssh -p 2022 YOUR_USERNAME@YOUR_WINDOWS_IP
# Should connect without password
```

**Disable password authentication (optional, after confirming keys work):**

```bash
# On WSL server
sudo nano /etc/ssh/sshd_config

# Change these lines:
PasswordAuthentication no
ChallengeResponseAuthentication no

# Restart SSH
sudo service ssh restart
```

### 2. Change Default Port

Using a non-standard port reduces automated attacks:

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Change Port line:
Port 2022  # Or any port > 1024 and < 65535

# Restart SSH
sudo service ssh restart

# Update Windows port forwarding accordingly
```

### 3. Use Fail2Ban (Optional)

Automatically ban IPs after failed login attempts:

```bash
# Install fail2ban
sudo apt-get install -y fail2ban

# Create custom configuration
sudo nano /etc/fail2ban/jail.local
```

Add:
```ini
[sshd]
enabled = true
port = 2022
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

```bash
# Start fail2ban
sudo service fail2ban start
```

### 4. Firewall Configuration

**Limit access to specific IP addresses (when possible):**

Windows Firewall (PowerShell as Administrator):
```powershell
# Allow only specific IP range
netsh advfirewall firewall add rule name="WSL SSH - Specific IPs" dir=in action=allow protocol=TCP localport=2022 remoteip=192.168.1.0/24
```

### 5. Regular Security Updates

```bash
# Update system regularly
sudo apt-get update && sudo apt-get upgrade -y

# Check for security updates
sudo apt-get upgrade --with-new-pkgs
```

### 6. Monitor Access Logs

```bash
# View recent SSH logins
sudo tail -f /var/log/auth.log | grep sshd

# See who's currently connected
who

# View login history
last -a
```

### 7. Strong Passwords

If using password authentication:
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Use password manager
- Never reuse passwords

**Change WSL password:**
```bash
passwd
```

---

## Troubleshooting

### Issue 1: Cannot Connect from Remote Computer

**Symptoms:**
```
ssh: connect to host X.X.X.X port 2022: Connection refused
```

**Solutions:**

1. **Check SSH is running:**
   ```bash
   sudo service ssh status
   # If not running:
   sudo service ssh start
   ```

2. **Verify port forwarding:**
   ```powershell
   # In Windows PowerShell as Admin
   netsh interface portproxy show v4tov4
   # Should show port 2022
   ```

3. **Check Windows Firewall:**
   ```powershell
   # List firewall rules
   netsh advfirewall firewall show rule name="WSL SSH"
   ```

4. **Verify WSL IP hasn't changed:**
   ```bash
   # In WSL
   hostname -I
   # Compare with port forwarding config, update if different
   ```

5. **Test from same machine first:**
   ```bash
   ssh localhost -p 2022
   # If this works, issue is with network/firewall
   ```

### Issue 2: WSL IP Changes After Reboot

**Symptom:** Connection works, then stops working after Windows restart.

**Solution:** WSL2's IP address changes on reboot. Run the port forwarding script again:

```cmd
cd D:\Genome\UTILITIES\ssh_remote_access
.\setup_port_forwarding.bat
```

**Permanent solution:** Set up Task Scheduler to run `start_wsl_ssh.ps1` at startup (see Auto-Start Configuration).

### Issue 3: Permission Denied (publickey)

**Symptoms:**
```
Permission denied (publickey,password).
```

**Solutions:**

1. **Check password authentication is enabled:**
   ```bash
   sudo grep PasswordAuthentication /etc/ssh/sshd_config
   # Should show: PasswordAuthentication yes
   ```

2. **Verify SSH key permissions (if using keys):**
   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

3. **Check SSH config syntax:**
   ```bash
   sudo sshd -t
   # Should show: "Syntax OK"
   ```

### Issue 4: Connection Resets or Hangs

**Solutions:**

1. **Increase SSH timeout:**
   ```bash
   # Edit SSH config
   sudo nano /etc/ssh/sshd_config
   
   # Add these lines:
   ClientAliveInterval 60
   ClientAliveCountMax 3
   
   sudo service ssh restart
   ```

2. **Check network stability:**
   ```bash
   # From remote computer
   ping YOUR_WINDOWS_IP
   # Should see consistent response times
   ```

### Issue 5: "No route to host" Error

**Solution:** This usually means firewall is blocking connection.

```powershell
# Windows PowerShell as Administrator
# Temporarily disable Windows Firewall for testing:
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Test connection
# If it works, re-enable firewall and add specific rule:
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
netsh advfirewall firewall add rule name="WSL SSH" dir=in action=allow protocol=TCP localport=2022
```

### Issue 6: SSH Service Won't Start

**Symptoms:**
```
Job for ssh.service failed because the control process exited with error code.
```

**Solutions:**

1. **Check for configuration errors:**
   ```bash
   sudo sshd -t
   # Fix any reported errors
   ```

2. **Check logs:**
   ```bash
   sudo journalctl -u ssh -n 50
   # Or
   sudo tail -50 /var/log/auth.log
   ```

3. **Check if port is already in use:**
   ```bash
   sudo netstat -tulpn | grep :2022
   # If another process is using port 2022, kill it or use different port
   ```

4. **Regenerate host keys:**
   ```bash
   sudo rm /etc/ssh/ssh_host_*
   sudo dpkg-reconfigure openssh-server
   sudo service ssh restart
   ```

---

## Convenience Scripts Reference

All scripts are located in `/mnt/d/Genome/UTILITIES/ssh_remote_access/`

### restart_ssh.sh
Restart SSH service and show status.
```bash
bash restart_ssh.sh
```

### test_ssh_connection.sh
Test SSH connection to local WSL instance.
```bash
bash test_ssh_connection.sh
```

### show_connection_info.sh
Display current network configuration and connection instructions.
```bash
bash show_connection_info.sh
```

### setup_port_forwarding.bat
Windows batch script to configure port forwarding (run as Administrator).
```cmd
.\setup_port_forwarding.bat
```

### start_wsl_ssh.ps1
PowerShell script for auto-starting WSL and SSH server.
```powershell
.\start_wsl_ssh.ps1
```

---

## Using SSH for Remote Pipeline Operations

### Basic Pipeline Operations

```bash
# Connect to your WSL instance
ssh -p 2022 user@your_windows_ip

# Navigate to pipeline
cd /mnt/d/Genome

# Run pipeline
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_001 8
```

### Running Long Analyses (Using Screen)

Long-running genomics analyses shouldn't be interrupted if SSH disconnects.

**Install screen:**
```bash
sudo apt-get install -y screen
```

**Use screen for pipeline:**
```bash
# Start new screen session
screen -S genomics_analysis

# Run your pipeline
cd /mnt/d/Genome
bash clinical_genomics_pipeline.sh single sample.vcf.gz SAMPLE_001 8

# Detach from screen: Press Ctrl+A, then D

# You can now safely disconnect SSH
```

**Reconnect later:**
```bash
# SSH back in
ssh -p 2022 user@your_windows_ip

# List screen sessions
screen -ls

# Reattach to session
screen -r genomics_analysis
```

**Screen quick reference:**
- `Ctrl+A` then `D` - Detach from screen
- `Ctrl+A` then `K` - Kill current screen
- `screen -ls` - List sessions
- `screen -r NAME` - Reattach to session
- `screen -S NAME` - Create named session

### File Transfer via SCP

**Download results from remote server:**
```bash
# From your local computer
scp -P 2022 -r user@your_windows_ip:/mnt/d/Genome/DATA/RESULTS/VCF_ANALYSIS ./results/
```

**Upload VCF to remote server:**
```bash
# From your local computer
scp -P 2022 sample.vcf.gz user@your_windows_ip:/mnt/d/Genome/DATA/downloaded_vcfs/
```

### VS Code Remote Development

**Connect VS Code to WSL via SSH:**

1. Install "Remote - SSH" extension in VS Code
2. Press F1 → "Remote-SSH: Connect to Host"
3. Enter: `user@your_windows_ip -p 2022`
4. Open folder: `/mnt/d/Genome`

Now you can edit scripts, review results, and run terminal commands remotely!

---

## Advanced Configuration

### Custom SSH Banner

Create a custom login message:

```bash
sudo nano /etc/motd
```

Add:
```
╔════════════════════════════════════════════════════════════════╗
║         Clinical Genomics Pipeline - Remote Access            ║
║                                                                ║
║  Location: /mnt/d/Genome                                      ║
║  Pipeline: clinical_genomics_pipeline.sh                      ║
║  Documentation: /mnt/d/Genome/MAIN_README.md                  ║
║                                                                ║
║  Quick Commands:                                              ║
║    cd /mnt/d/Genome                                          ║
║    bash clinical_genomics_pipeline.sh --help                 ║
║                                                                ║
║  Support: review DOCUMENTATION/ directory                     ║
╚════════════════════════════════════════════════════════════════╝
```

### Port Forwarding for Web Interfaces

If your pipeline generates web reports:

```bash
# Connect with local port forwarding
ssh -L 8080:localhost:8080 -p 2022 user@your_windows_ip

# Now access http://localhost:8080 on your local machine
# It will show content from WSL
```

### Persistent SSH Connections (SSH Multiplexing)

Reuse SSH connections to speed up subsequent connections:

Add to `~/.ssh/config` on your local machine:
```
Host genomics-pipeline
    HostName YOUR_WINDOWS_IP
    Port 2022
    User YOUR_USERNAME
    ControlMaster auto
    ControlPath ~/.ssh/control-%r@%h:%p
    ControlPersist 1h
```

Now simply use:
```bash
ssh genomics-pipeline
```

---

## Security Checklist

- [ ] Changed default SSH password to strong password
- [ ] Set up SSH key authentication
- [ ] Disabled password authentication (after testing keys)
- [ ] Changed SSH port from 22 to custom port
- [ ] Configured Windows Firewall rules
- [ ] Set up fail2ban (for internet-facing servers)
- [ ] Regular system updates configured
- [ ] Monitoring access logs periodically
- [ ] Documented authorized users and devices
- [ ] Backed up SSH keys securely
- [ ] Tested disaster recovery (locked out) procedures

---

## Network Diagrams

### WSL2 Network Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Internet                             │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────┐
│       Home Router     │                                 │
│                       ↓                                 │
│         Port Forwarding (optional)                      │
│         External: 2022 → Internal: Windows IP           │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────┐
│    Local Network      │                                 │
│                       ↓                                 │
│         ┌──────────────────────┐                        │
│         │   Windows Machine    │                        │
│         │  IP: 192.168.1.100  │                        │
│         │                      │                        │
│         │  ┌────────────────┐  │                        │
│         │  │  Port Proxy    │  │                        │
│         │  │  2022 → WSL    │  │                        │
│         │  └────────┬───────┘  │                        │
│         │           │          │                        │
│         │  ┌────────▼───────┐  │                        │
│         │  │      WSL2      │  │                        │
│         │  │ IP: 172.x.x.x  │  │                        │
│         │  │                │  │                        │
│         │  │  SSH Server    │  │                        │
│         │  │  Port 2022     │  │                        │
│         │  │                │  │                        │
│         │  │  /mnt/d/Genome │  │                        │
│         │  └────────────────┘  │                        │
│         └──────────────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

### Connection Flow

```
Remote Computer
      ↓
Internet (if applicable)
      ↓
Home Router (port forwarding)
      ↓
Windows Firewall (allow port 2022)
      ↓
Windows NetSH Port Proxy (2022 → WSL:2022)
      ↓
WSL Network Interface
      ↓
WSL SSH Server
      ↓
Clinical Genomics Pipeline
```

---

## FAQ

**Q: Do I need a static IP address?**

A: No, but it helps. Use dynamic DNS services (DynDNS, No-IP) for a stable hostname if your IP changes.

**Q: Can I use this over cellular/mobile hotspot?**

A: Yes, but carrier NAT may block incoming connections. VPN or reverse tunnel services (ngrok, Tailscale) are alternatives.

**Q: Is this secure enough for HIPAA/clinical data?**

A: SSH itself is secure, but compliance requires additional measures:
- Use SSH keys, not passwords
- Enable audit logging
- Configure VPN for additional layer
- Encrypt data at rest
- Follow institutional security policies

**Q: What if I forget my SSH password?**

A: Reset from Windows:
```cmd
wsl -u root passwd YOUR_USERNAME
```

**Q: Can multiple people connect simultaneously?**

A: Yes, SSH supports multiple concurrent sessions.

**Q: Does this work with all WSL distributions?**

A: Yes, this guide uses Ubuntu but works with Debian, openSUSE, etc. with minor modifications.

**Q: Will this slow down my Windows machine?**

A: SSH server uses minimal resources (~10-20 MB RAM). Pipeline processing uses the same resources whether local or remote.

**Q: Can I use this with WSL on a laptop?**

A: Yes! Just ensure:
- Laptop stays awake (adjust power settings)
- Network connection is stable
- Consider VPN when on public WiFi

**Q: What about file permissions when accessing remotely?**

A: File permissions are preserved. You access as your WSL user, so all file operations have the same permissions as local access.

---

## Resources

### Official Documentation
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [OpenSSH Manual](https://www.openssh.com/manual.html)
- [Windows Firewall Guide](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-firewall/)

### Additional Tools
- **Tailscale**: Easy VPN for secure remote access - https://tailscale.com/
- **ngrok**: Expose local server to internet - https://ngrok.com/
- **ZeroTier**: Virtual networking - https://www.zerotier.com/

### Security Resources
- [SSH Security Best Practices](https://www.ssh.com/academy/ssh/security)
- [fail2ban Documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)

---

## Support

**Location:** `/mnt/d/Genome/UTILITIES/ssh_remote_access/`

**Script Issues:** Review log files and re-run setup script

**Connection Problems:** See Troubleshooting section

**Security Concerns:** Review SECURITY_GUIDE.md (if available)

---

**Version:** 1.0  
**Last Updated:** September 2025  
**Maintainer:** Clinical Genomics Pipeline Team  

**Happy remote analyzing! 🧬🔐**
