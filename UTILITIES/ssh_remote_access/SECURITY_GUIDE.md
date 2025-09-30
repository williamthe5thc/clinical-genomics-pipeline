# SSH Security Guide

**Comprehensive security guidelines for remote access to Clinical Genomics Pipeline**

**📚 Quick Navigation:**
- [← Back to Utilities](../README.md) | [Installation Guide](../INSTALLATION_COMPLETE.md)
- **SSH Docs:** [Setup Guide](README.md) | [Security (This Guide)](#) | [Quick Reference](QUICK_REFERENCE.md)
- [Main Pipeline →](../../MAIN_README.md)

---

## Security Threat Model

### What We're Protecting

1. **Sensitive Genomic Data**: Patient VCFs, clinical reports, genetic information
2. **Computational Resources**: Pipeline infrastructure, databases
3. **System Integrity**: Preventing unauthorized modifications
4. **Network Security**: Protecting against network-based attacks

### Threat Scenarios

| Threat | Risk Level | Mitigation |
|--------|-----------|------------|
| Brute force password attacks | HIGH | SSH keys, fail2ban, non-standard port |
| Unauthorized access | HIGH | Strong authentication, firewall rules |
| Man-in-the-middle attacks | MEDIUM | SSH key fingerprint verification |
| Data interception | LOW | SSH encryption (built-in) |
| Insider threats | MEDIUM | Access logging, principle of least privilege |
| Zero-day exploits | LOW | Regular updates, security monitoring |

---

## Security Levels

Choose appropriate security level for your use case:

### Level 1: Basic Security (Local Network Only)
**Appropriate for:** Home network, trusted environment, single user

- ✓ Password authentication enabled
- ✓ Non-standard port (2022)
- ✓ Windows Firewall enabled
- ✓ Local network access only

### Level 2: Enhanced Security (Recommended)
**Appropriate for:** Multi-user environment, remote access, research data

- ✓ SSH key authentication required
- ✓ Password authentication disabled
- ✓ fail2ban configured
- ✓ Non-standard port
- ✓ Regular security updates
- ✓ Access logging enabled
- ✓ Limited IP ranges (when possible)

### Level 3: Clinical/Production Security (HIPAA/Compliance)
**Appropriate for:** Clinical data, production systems, regulated environments

- ✓ All Level 2 measures
- ✓ VPN required for external access
- ✓ Multi-factor authentication (2FA)
- ✓ Dedicated security monitoring
- ✓ Encrypted filesystem
- ✓ Audit trail for all access
- ✓ Regular security audits
- ✓ Disaster recovery plan
- ✓ Compliance documentation

---

## Hardening Steps

### 1. SSH Key Authentication Setup

**Why:** Password attacks are the #1 SSH security threat. Keys are cryptographically stronger.

**Setup SSH Keys:**

```bash
# On your LOCAL computer (laptop, home workstation)
ssh-keygen -t ed25519 -b 4096 -C "your_email@example.com"

# Ed25519 is faster and more secure than RSA
# Use passphrase for the key (REQUIRED for production)
```

**Copy to server:**

```bash
# Method 1: Using ssh-copy-id
ssh-copy-id -p 2022 username@your_server_ip

# Method 2: Manual copy
cat ~/.ssh/id_ed25519.pub | ssh -p 2022 username@server_ip \
    "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**Test key authentication:**

```bash
ssh -p 2022 username@server_ip
# Should not ask for password
```

**Disable password authentication:**

```bash
# On WSL server
sudo nano /etc/ssh/sshd_config

# Change these settings:
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM no
PermitRootLogin no
```

```bash
# Restart SSH
sudo service ssh restart

# IMPORTANT: Test in a separate terminal before closing existing connection!
# If locked out, you'll need to fix from Windows: wsl -u root
```

### 2. Install and Configure fail2ban

**Why:** Automatically block IPs after repeated failed login attempts.

```bash
# Install
sudo apt-get update
sudo apt-get install -y fail2ban

# Create configuration
sudo nano /etc/fail2ban/jail.local
```

**Configuration:**

```ini
[DEFAULT]
# Ban IPs for 1 hour after 3 failed attempts within 10 minutes
bantime = 3600
findtime = 600
maxretry = 3
destemail = your_email@example.com
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = 2022
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

```bash
# Start fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Check status
sudo fail2ban-client status sshd

# See banned IPs
sudo fail2ban-client get sshd banned
```

**Unban an IP (if you lock yourself out):**

```bash
sudo fail2ban-client set sshd unbanip YOUR_IP
```

### 3. Configure SSH Server Security

**Edit SSH configuration:**

```bash
sudo nano /etc/ssh/sshd_config
```

**Recommended settings:**

```bash
# Port and listening
Port 2022
ListenAddress 0.0.0.0

# Authentication
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
UsePAM no

# Protocol and encryption
Protocol 2

# Key types (only strong algorithms)
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# Ciphers (only strong ciphers)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256

# Session management
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 3
MaxSessions 10
LoginGraceTime 60

# Logging
LogLevel VERBOSE
SyslogFacility AUTH

# Access control
AllowUsers your_username  # Only allow specific users
# Or use: AllowGroups genomics
DenyUsers root admin      # Explicitly deny users

# X11 and forwarding
X11Forwarding yes
AllowTcpForwarding yes
AllowAgentForwarding yes
```

```bash
# Test configuration
sudo sshd -t

# If OK, restart
sudo service ssh restart
```

### 4. Firewall Configuration

**Windows Firewall (PowerShell as Administrator):**

```powershell
# Remove default rule
netsh advfirewall firewall delete rule name="WSL SSH"

# Add restrictive rule (specific IP range)
netsh advfirewall firewall add rule `
    name="WSL SSH - Restricted" `
    dir=in `
    action=allow `
    protocol=TCP `
    localport=2022 `
    remoteip=192.168.1.0/24

# Or allow specific IPs only
netsh advfirewall firewall add rule `
    name="WSL SSH - Specific IPs" `
    dir=in `
    action=allow `
    protocol=TCP `
    localport=2022 `
    remoteip=192.168.1.100,192.168.1.101
```

**WSL Firewall (ufw):**

```bash
# Install and enable ufw
sudo apt-get install -y ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH on custom port
sudo ufw allow 2022/tcp

# Allow from specific IP
sudo ufw allow from 192.168.1.100 to any port 2022

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose
```

### 5. Two-Factor Authentication (2FA)

**Install Google Authenticator:**

```bash
sudo apt-get install -y libpam-google-authenticator

# Run setup for your user
google-authenticator
```

**Answer the prompts:**
- Do you want authentication tokens to be time-based: Yes
- Scan QR code with Google Authenticator app
- Save emergency scratch codes securely
- Update .google_authenticator file: Yes
- Disallow multiple uses: Yes
- Rate limiting: Yes

**Configure PAM:**

```bash
sudo nano /etc/pam.d/sshd
```

Add at the top:
```
auth required pam_google_authenticator.so
```

**Configure SSH:**

```bash
sudo nano /etc/ssh/sshd_config
```

Add/modify:
```
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

```bash
# Restart SSH
sudo service ssh restart
```

**Test:** You'll now need both SSH key AND 2FA code to connect!

### 6. IP Whitelisting

**Allow only specific IPs to connect:**

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Add at end:
Match Address 192.168.1.100,192.168.1.101
    AllowUsers genomics_user
    
Match Address !192.168.1.0/24
    DenyUsers *
```

Or use TCP wrappers:

```bash
# /etc/hosts.allow
sshd: 192.168.1.100 192.168.1.101 : allow

# /etc/hosts.deny
sshd: ALL : deny
```

### 7. VPN for External Access

**Why:** Adds additional encryption and authentication layer.

**Recommended VPN solutions:**

1. **Tailscale** (easiest):
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   # Access via Tailscale IP instead of public IP
   ```

2. **WireGuard**:
   ```bash
   sudo apt-get install -y wireguard
   # Configure according to WireGuard docs
   ```

3. **OpenVPN**:
   ```bash
   sudo apt-get install -y openvpn
   # Import VPN configuration from provider
   ```

---

## Monitoring and Auditing

### 1. Access Logging

**Enable detailed logging:**

```bash
# SSH logs
sudo tail -f /var/log/auth.log | grep sshd

# Filter successful connections
sudo grep "Accepted" /var/log/auth.log

# Filter failed attempts
sudo grep "Failed" /var/log/auth.log

# Show last 20 login attempts
sudo tail -20 /var/log/auth.log
```

**Create monitoring script:**

```bash
cat > ~/monitor_ssh.sh << 'EOF'
#!/bin/bash
echo "=== SSH Connection Summary ==="
echo "Active connections:"
who
echo ""
echo "Recent successful logins:"
grep "Accepted" /var/log/auth.log | tail -10
echo ""
echo "Recent failed attempts:"
grep "Failed" /var/log/auth.log | tail -10
echo ""
echo "Unique IPs with failed attempts today:"
grep "Failed password" /var/log/auth.log | \
    grep "$(date +%b\ %d)" | \
    awk '{print $(NF-3)}' | sort | uniq -c | sort -rn
EOF

chmod +x ~/monitor_ssh.sh
```

### 2. Intrusion Detection

**Install AIDE (Advanced Intrusion Detection Environment):**

```bash
sudo apt-get install -y aide

# Initialize database
sudo aideinit

# Move database
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Run check
sudo aide --check

# Schedule daily checks
sudo crontab -e
# Add: 0 2 * * * /usr/bin/aide --check | mail -s "AIDE Report" your_email@example.com
```

### 3. Log Rotation

**Ensure logs don't fill disk:**

```bash
sudo nano /etc/logrotate.d/rsyslog
```

Verify:
```
/var/log/auth.log {
    rotate 12
    weekly
    missingok
    notifempty
    compress
    delaycompress
    sharedscripts
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```

### 4. Security Scanning

**Regular vulnerability scans:**

```bash
# Install Lynis
sudo apt-get install -y lynis

# Run security audit
sudo lynis audit system

# Review results
less /var/log/lynis.log
```

---

## Incident Response

### Suspected Unauthorized Access

1. **Immediately disconnect suspicious connections:**
   ```bash
   # See active connections
   who
   
   # Kill specific user session
   sudo pkill -u suspicious_username
   
   # Or kill specific SSH session
   sudo kill PID_NUMBER
   ```

2. **Block attacker IP:**
   ```bash
   # Temporarily block
   sudo ufw deny from ATTACKER_IP
   
   # Or use fail2ban
   sudo fail2ban-client set sshd banip ATTACKER_IP
   ```

3. **Review logs:**
   ```bash
   # Check auth logs
   sudo grep ATTACKER_IP /var/log/auth.log
   
   # Check for file modifications
   sudo find /mnt/d/Genome -type f -mtime -1
   ```

4. **Change passwords/keys:**
   ```bash
   # Change password
   passwd
   
   # Regenerate SSH keys
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new
   ```

5. **Document incident:**
   - Time of detection
   - Source IP
   - Activities observed
   - Actions taken
   - Follow-up required

### Locked Out Recovery

**If you lock yourself out:**

1. **From Windows Command Prompt:**
   ```cmd
   wsl -u root
   nano /etc/ssh/sshd_config
   # Re-enable PasswordAuthentication temporarily
   service ssh restart
   ```

2. **Reset user password:**
   ```cmd
   wsl -u root
   passwd YOUR_USERNAME
   ```

3. **Fix SSH permissions:**
   ```cmd
   wsl -u root
   chmod 700 /home/YOUR_USERNAME/.ssh
   chmod 600 /home/YOUR_USERNAME/.ssh/authorized_keys
   chown -R YOUR_USERNAME:YOUR_USERNAME /home/YOUR_USERNAME/.ssh
   ```

---

## Compliance Considerations

### HIPAA Requirements

If handling Protected Health Information (PHI):

- [ ] Encryption in transit (SSH provides this)
- [ ] Encryption at rest (configure filesystem encryption)
- [ ] Access controls (SSH keys, 2FA)
- [ ] Audit logs (enabled and retained)
- [ ] User authentication (strong passwords/keys)
- [ ] Automatic logoff (ClientAliveInterval)
- [ ] Unique user IDs (no shared accounts)
- [ ] Emergency access procedures (documented)
- [ ] Regular security reviews (scheduled)
- [ ] Business Associate Agreements (if applicable)

### General Best Practices

1. **Principle of Least Privilege:**
   - Create separate accounts for different users
   - Use `sudo` for administrative tasks
   - Don't run services as root

2. **Data Protection:**
   - Encrypt sensitive files with GPG
   - Use secure file transfer (SCP, SFTP)
   - Regular backups with encryption

3. **Network Segmentation:**
   - Use VPN for external access
   - Separate networks for production/development
   - DMZ for internet-facing services

4. **Security Updates:**
   - Enable automatic security updates
   - Test updates in development first
   - Document update procedures

---

## Security Checklist

### Initial Setup
- [ ] SSH server installed and configured
- [ ] Non-standard port configured (2022 or custom)
- [ ] Root login disabled
- [ ] Strong user passwords set
- [ ] SSH keys generated on client computers
- [ ] Password authentication disabled (after key setup)
- [ ] Windows Firewall configured
- [ ] WSL firewall (ufw) configured
- [ ] fail2ban installed and configured

### Enhanced Security
- [ ] Two-factor authentication configured
- [ ] IP whitelisting implemented
- [ ] VPN configured for external access
- [ ] Security monitoring tools installed (Lynis, AIDE)
- [ ] Log rotation configured
- [ ] Access logs being monitored
- [ ] Incident response plan documented

### Ongoing Maintenance
- [ ] Weekly log reviews
- [ ] Monthly security updates
- [ ] Quarterly security audits
- [ ] Annual penetration testing (production systems)
- [ ] Regular backup verification
- [ ] User access reviews
- [ ] Documentation updates

---

## Emergency Contacts

**Document your emergency contacts:**

- System Administrator: _________________
- Security Team: _________________
- IT Support: _________________
- Compliance Officer: _________________

**Emergency Procedures:**

1. Suspected breach: _________________
2. Service outage: _________________
3. Data loss: _________________

---

## Resources

- [SSH Security Best Practices](https://www.ssh.com/academy/ssh/security)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/)

---

**Version:** 1.0  
**Last Updated:** September 2025  
**Review Date:** March 2026  

**Stay secure! 🔒**
