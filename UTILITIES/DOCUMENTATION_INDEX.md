# Clinical Genomics Pipeline - Complete Documentation Index

**Quick access to all documentation across the pipeline**

**Last Updated:** September 29, 2025

---

## 📚 Main Documentation

| Document | Description | Location |
|----------|-------------|----------|
| **[Main Pipeline README](../MAIN_README.md)** | Core pipeline documentation and overview | `/mnt/d/Genome/MAIN_README.md` |
| **[Utilities Overview](README.md)** | Utilities suite main guide | `/mnt/d/Genome/UTILITIES/README.md` |
| **[Installation Complete](INSTALLATION_COMPLETE.md)** | Getting started with utilities | `/mnt/d/Genome/UTILITIES/INSTALLATION_COMPLETE.md` |

---

## 🧰 Utility Documentation

### VCF Downloader 📥

| Document | Description | Location |
|----------|-------------|----------|
| **[VCF Downloader Guide](vcf_downloader/README.md)** | Complete user manual | `/mnt/d/Genome/UTILITIES/vcf_downloader/README.md` |
| **[Download Script](vcf_downloader/vcf_downloader.py)** | Python download tool | `/mnt/d/Genome/UTILITIES/vcf_downloader/vcf_downloader.py` |
| **[Example Template](vcf_downloader/example_download_list.csv)** | CSV template file | `/mnt/d/Genome/UTILITIES/vcf_downloader/example_download_list.csv` |

**Quick Start:**
```bash
cd /mnt/d/Genome/UTILITIES/vcf_downloader
python vcf_downloader.py --help
```

---

### SSH Remote Access 🔐

| Document | Description | Location |
|----------|-------------|----------|
| **[Setup Guide](ssh_remote_access/README.md)** | Complete installation and setup | `/mnt/d/Genome/UTILITIES/ssh_remote_access/README.md` |
| **[Security Guide](ssh_remote_access/SECURITY_GUIDE.md)** | Security best practices and hardening | `/mnt/d/Genome/UTILITIES/ssh_remote_access/SECURITY_GUIDE.md` |
| **[Quick Reference](ssh_remote_access/QUICK_REFERENCE.md)** | Command cheat sheet | `/mnt/d/Genome/UTILITIES/ssh_remote_access/QUICK_REFERENCE.md` |

**Quick Start:**
```bash
cd /mnt/d/Genome/UTILITIES/ssh_remote_access
bash setup_ssh_access.sh
```

---

### Email Notifications 📧

| Document | Description | Location |
|----------|-------------|----------|
| **[Email Notifications Guide](../EMAIL_NOTIFICATIONS_README.md)** | Setup and configuration | `/mnt/d/Genome/EMAIL_NOTIFICATIONS_README.md` |

**Quick Start:**
```bash
cd /mnt/d/Genome/UTILITIES/email_notifications
bash setup_email_notifications.sh
```

---

## 🛠️ Helper Scripts

### Verification and Setup

| Script | Purpose | Command |
|--------|---------|---------|
| **[verify_utilities.sh](verify_utilities.sh)** | Verify utilities installation | `bash verify_utilities.sh` |
| **[quick_start.sh](quick_start.sh)** | Interactive setup wizard | `bash quick_start.sh` |
| **[make_executable.sh](make_executable.sh)** | Set script permissions | `bash make_executable.sh` |

### VCF Downloader

| Script | Purpose | Command |
|--------|---------|---------|
| **[vcf_downloader.py](vcf_downloader/vcf_downloader.py)** | Main download tool | `python vcf_downloader.py --help` |

### SSH Remote Access

| Script | Purpose | Command |
|--------|---------|---------|
| **[setup_ssh_access.sh](ssh_remote_access/setup_ssh_access.sh)** | Automated SSH setup | `bash setup_ssh_access.sh` |
| **[restart_ssh.sh](ssh_remote_access/restart_ssh.sh)** | Restart SSH service | `bash restart_ssh.sh` |
| **[test_ssh_connection.sh](ssh_remote_access/test_ssh_connection.sh)** | Test SSH connection | `bash test_ssh_connection.sh` |
| **[show_connection_info.sh](ssh_remote_access/show_connection_info.sh)** | Display connection info | `bash show_connection_info.sh` |
| **[setup_port_forwarding.bat](ssh_remote_access/setup_port_forwarding.bat)** | Windows port forwarding | Run as Admin in Windows |
| **[start_wsl_ssh.ps1](ssh_remote_access/start_wsl_ssh.ps1)** | Auto-start script | PowerShell auto-start |

---

## 📖 Documentation by Topic

### Getting Started

1. **New User Setup:**
   - [Main Pipeline README](../MAIN_README.md)
   - [Utilities Installation Guide](INSTALLATION_COMPLETE.md)
   - [Quick Start Wizard](quick_start.sh)

2. **Verification:**
   - [Verify Utilities](verify_utilities.sh)
   - Test each utility individually

### Common Tasks

#### Downloading VCF Files

1. [VCF Downloader README](vcf_downloader/README.md)
   - [Single File Download](vcf_downloader/README.md#example-1-download-single-vcf)
   - [Batch Excel Download](vcf_downloader/README.md#example-2-batch-download-from-excel)
   - [Troubleshooting](vcf_downloader/README.md#troubleshooting)

#### Remote Access

1. [SSH Setup Guide](ssh_remote_access/README.md)
   - [Quick Start](ssh_remote_access/README.md#quick-start)
   - [Detailed Setup](ssh_remote_access/README.md#detailed-setup-guide)
   - [Connection Methods](ssh_remote_access/README.md#connection-methods)

2. [SSH Security](ssh_remote_access/SECURITY_GUIDE.md)
   - [Security Levels](ssh_remote_access/SECURITY_GUIDE.md#security-levels)
   - [Hardening Steps](ssh_remote_access/SECURITY_GUIDE.md#hardening-steps)
   - [Monitoring](ssh_remote_access/SECURITY_GUIDE.md#monitoring-and-auditing)

3. [SSH Quick Reference](ssh_remote_access/QUICK_REFERENCE.md)
   - [Connection Commands](ssh_remote_access/QUICK_REFERENCE.md#connection-commands)
   - [File Transfer](ssh_remote_access/QUICK_REFERENCE.md#file-transfer)
   - [Troubleshooting](ssh_remote_access/QUICK_REFERENCE.md#troubleshooting-commands)

#### Running Pipeline

1. [Main Pipeline Guide](../MAIN_README.md#-quick-start-guide)
2. [Email Notifications](../EMAIL_NOTIFICATIONS_README.md)
3. [Remote Execution via SSH](ssh_remote_access/README.md#using-ssh-for-remote-pipeline-operations)

---

## 🔒 Security Documentation

| Topic | Document | Section |
|-------|----------|---------|
| **Threat Model** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [Security Threat Model](ssh_remote_access/SECURITY_GUIDE.md#security-threat-model) |
| **SSH Keys** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [SSH Key Auth](ssh_remote_access/SECURITY_GUIDE.md#1-ssh-key-authentication-setup) |
| **fail2ban** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [fail2ban Config](ssh_remote_access/SECURITY_GUIDE.md#2-install-and-configure-fail2ban) |
| **Firewall** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [Firewall Config](ssh_remote_access/SECURITY_GUIDE.md#4-firewall-configuration) |
| **2FA** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [Two-Factor Auth](ssh_remote_access/SECURITY_GUIDE.md#5-two-factor-authentication-2fa) |
| **Monitoring** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [Monitoring](ssh_remote_access/SECURITY_GUIDE.md#monitoring-and-auditing) |
| **HIPAA** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [HIPAA Compliance](ssh_remote_access/SECURITY_GUIDE.md#hipaa-requirements) |
| **Checklist** | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [Security Checklist](ssh_remote_access/SECURITY_GUIDE.md#security-checklist) |

---

## 🆘 Troubleshooting Resources

### By Utility

#### VCF Downloader Issues
- [VCF Downloader Troubleshooting](vcf_downloader/README.md#troubleshooting)
- Common issues: Excel loading, download timeouts, SSL errors

#### SSH Access Issues
- [SSH Setup Troubleshooting](ssh_remote_access/README.md#troubleshooting)
- [SSH Quick Reference - Diagnostics](ssh_remote_access/QUICK_REFERENCE.md#troubleshooting-commands)
- Common issues: Connection refused, port forwarding, authentication

#### General Utilities
- [Utilities README - Troubleshooting](README.md#troubleshooting)
- [Installation Guide - Troubleshooting](INSTALLATION_COMPLETE.md#troubleshooting)

### By Problem Type

| Problem | Documentation | Section |
|---------|---------------|---------|
| **Cannot connect to SSH** | [SSH Setup](ssh_remote_access/README.md) | [Issue 1](ssh_remote_access/README.md#issue-1-cannot-connect-from-remote-computer) |
| **WSL IP changed** | [SSH Setup](ssh_remote_access/README.md) | [Issue 2](ssh_remote_access/README.md#issue-2-wsl-ip-changes-after-reboot) |
| **Permission denied** | [SSH Setup](ssh_remote_access/README.md) | [Issue 3](ssh_remote_access/README.md#issue-3-permission-denied-publickey) |
| **SSH won't start** | [SSH Setup](ssh_remote_access/README.md) | [Issue 6](ssh_remote_access/README.md#issue-6-ssh-service-wont-start) |
| **Download fails** | [VCF Downloader](vcf_downloader/README.md) | [Troubleshooting](vcf_downloader/README.md#troubleshooting) |
| **Excel not loading** | [VCF Downloader](vcf_downloader/README.md) | [Troubleshooting](vcf_downloader/README.md#issue-excel-file-not-loading) |

---

## 📊 Quick Command Reference

### Verification
```bash
cd /mnt/d/Genome/UTILITIES
bash verify_utilities.sh
```

### VCF Downloader
```bash
# Help
python vcf_downloader/vcf_downloader.py --help

# Download single file
python vcf_downloader/vcf_downloader.py --url URL

# Download from Excel
python vcf_downloader/vcf_downloader.py --excel file.xlsx
```

### SSH Remote Access
```bash
# Setup
bash ssh_remote_access/setup_ssh_access.sh

# Connect
ssh USERNAME@HOST -p 2022

# Show info
bash ssh_remote_access/show_connection_info.sh

# Test connection
bash ssh_remote_access/test_ssh_connection.sh

# Restart service
bash ssh_remote_access/restart_ssh.sh
```

### Email Notifications
```bash
# Setup
bash email_notifications/setup_email_notifications.sh

# Test
bash email_notifications/test_email_integration.sh
```

---

## 🔗 External Resources

### Official Documentation
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [OpenSSH Manual](https://www.openssh.com/manual.html)
- [Python Requests Library](https://requests.readthedocs.io/)

### Security Resources
- [SSH Security Best Practices](https://www.ssh.com/academy/ssh/security)
- [fail2ban Documentation](https://www.fail2ban.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Additional Tools
- [Tailscale VPN](https://tailscale.com/)
- [ngrok Tunneling](https://ngrok.com/)
- [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)

---

## 📝 Document Status

| Document | Status | Last Updated | Version |
|----------|--------|--------------|---------|
| Main README | ✅ Current | Sept 2025 | 1.0 |
| VCF Downloader | ✅ Current | Sept 2025 | 1.0 |
| SSH Setup | ✅ Current | Sept 2025 | 1.0 |
| SSH Security | ✅ Current | Sept 2025 | 1.0 |
| SSH Quick Ref | ✅ Current | Sept 2025 | 1.0 |
| Installation | ✅ Current | Sept 2025 | 1.0 |

---

## 🎯 Next Steps

**New users start here:**
1. Read [Main Pipeline README](../MAIN_README.md)
2. Review [Utilities Overview](README.md)
3. Follow [Installation Guide](INSTALLATION_COMPLETE.md)
4. Run [Quick Start Wizard](quick_start.sh)

**Need specific help?**
- **Download files:** [VCF Downloader Guide](vcf_downloader/README.md)
- **Remote access:** [SSH Setup Guide](ssh_remote_access/README.md)
- **Security:** [Security Best Practices](ssh_remote_access/SECURITY_GUIDE.md)
- **Quick commands:** [SSH Quick Reference](ssh_remote_access/QUICK_REFERENCE.md)

---

**Version:** 1.0  
**Maintained by:** Clinical Genomics Pipeline Team  
**Last Updated:** September 29, 2025

**Navigate back:** [← Utilities Main](README.md) | [← Main Pipeline](../MAIN_README.md)
