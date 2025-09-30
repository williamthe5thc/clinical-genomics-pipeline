# Clinical Genomics Pipeline - Utilities Suite

**Quality-of-life tools for enhanced pipeline operations**

**📚 Quick Navigation:**
- [Installation Guide](INSTALLATION_COMPLETE.md)
- [VCF Downloader](vcf_downloader/README.md)
- [SSH Remote Access](ssh_remote_access/README.md) | [Security Guide](ssh_remote_access/SECURITY_GUIDE.md) | [Quick Reference](ssh_remote_access/QUICK_REFERENCE.md)
- [Main Pipeline Documentation](../MAIN_README.md)

---

## Overview

This directory contains utility tools that enhance the Clinical Genomics Pipeline with additional functionality for remote access, file management, and workflow automation.

### Available Utilities

| Utility | Purpose | Documentation | Status |
|---------|---------|---------------|--------|
| **[VCF Downloader](vcf_downloader/README.md)** | Download VCF files from URLs or Excel spreadsheets | [Full Guide →](vcf_downloader/README.md) | ✅ Ready |
| **[SSH Remote Access](ssh_remote_access/README.md)** | Configure secure remote access to WSL pipeline | [Setup →](ssh_remote_access/README.md) \| [Security →](ssh_remote_access/SECURITY_GUIDE.md) | ✅ Ready |
| **[Email Notifications](../EMAIL_NOTIFICATIONS_README.md)** | Pipeline completion email alerts | [Setup Guide →](../EMAIL_NOTIFICATIONS_README.md) | ✅ Ready |

---

## 1. VCF Downloader

**Automated VCF file download system**

📖 **[Full Documentation →](vcf_downloader/README.md)**

### What It Does
- Downloads VCF files from remote URLs
- Processes Excel spreadsheets with multiple download links
- Progress tracking with speed and ETA
- Integrity verification
- Automatic file organization

### Quick Start

```bash
# Download single VCF
python vcf_downloader/vcf_downloader.py --url https://example.com/sample.vcf.gz

# Download from Excel file
python vcf_downloader/vcf_downloader.py --excel download_list.xlsx

# With integrity verification
python vcf_downloader/vcf_downloader.py --excel download_list.xlsx --verify-integrity
```

### Resources
- 📖 [Complete User Guide](vcf_downloader/README.md)
- 📝 [Example Template](vcf_downloader/example_download_list.csv)
- 💻 [Script Source](vcf_downloader/vcf_downloader.py)

### Use Cases
- Download samples from collaborators
- Batch download from public databases
- Clinical sample processing pipelines
- Research data acquisition

---

## 2. SSH Remote Access

**Secure remote access to your genomics pipeline**

📖 **[Full Documentation →](ssh_remote_access/README.md)**

### What It Does
- Configures OpenSSH server in WSL
- Sets up Windows port forwarding
- Creates auto-start scripts
- Implements security best practices
- Enables remote pipeline operations

### Quick Start

```bash
# Run automated setup
cd ssh_remote_access
bash setup_ssh_access.sh

# Then configure Windows (as Administrator)
cd D:\Genome\UTILITIES\ssh_remote_access
.\setup_port_forwarding.bat

# Connect remotely
ssh YOUR_USERNAME@YOUR_WINDOWS_IP -p 2022
```

### Resources
- 📖 [Complete Setup Guide](ssh_remote_access/README.md)
- 🔒 [Security Best Practices](ssh_remote_access/SECURITY_GUIDE.md)
- ⚡ [Command Quick Reference](ssh_remote_access/QUICK_REFERENCE.md)
- 📝 [Setup Script](ssh_remote_access/setup_ssh_access.sh)

### Use Cases
- Access pipeline from home/lab/travel
- Remote monitoring of long analyses
- Collaborative research access
- Emergency pipeline operations

---

## 3. Email Notifications

**Automated pipeline completion alerts**

📖 **[Full Documentation →](../EMAIL_NOTIFICATIONS_README.md)**

### What It Does
- Sends email when VEP annotation completes (~3 hours)
- Notifies on pipeline success/failure
- Provides processing statistics
- Non-blocking operation (doesn't interrupt pipeline)

### Quick Start

```bash
cd email_notifications
bash setup_email_notifications.sh

# Test configuration
bash test_email_integration.sh

# Run pipeline normally - notifications automatic!
```

### Resources
- 📖 [Setup Guide](../EMAIL_NOTIFICATIONS_README.md)
- ⚙️ Configuration: `email_notifications/email_config.json`

### Use Cases
- Monitor long-running whole genome analyses
- Multi-sample batch processing alerts
- Overnight/weekend pipeline runs
- Remote collaboration notifications

---

## Complete Workflow Examples

### Example 1: Remote Batch Processing

```bash
# Step 1: Download VCFs (from local or remote computer)
python vcf_downloader/vcf_downloader.py \
    --excel sample_list.xlsx \
    --verify-integrity

# Step 2: Connect via SSH (if remote)
ssh -p 2022 user@pipeline_server

# Step 3: Start batch processing in screen
screen -S batch_analysis
cd /mnt/d/Genome
bash clinical_genomics_pipeline.sh batch DATA/downloaded_vcfs/ 8

# Step 4: Detach and monitor via email
# Press Ctrl+A then D
# Receive email notifications as each sample completes
```

### Example 2: Collaborative Research

```bash
# Researcher 1: Uploads samples
scp -P 2022 *.vcf.gz user@server:/mnt/d/Genome/DATA/downloaded_vcfs/

# Researcher 2: Processes samples remotely
ssh -p 2022 user@server
cd /mnt/d/Genome
bash clinical_genomics_pipeline.sh batch DATA/downloaded_vcfs/ 8

# Both: Receive email notifications
# Both: Download results when complete
scp -P 2022 -r user@server:/mnt/d/Genome/DATA/RESULTS/ ./
```

### Example 3: Clinical Lab Workflow

```bash
# 1. Receive Excel file from sequencing facility
#    with download links for patient VCFs

# 2. Automated download
python vcf_downloader/vcf_downloader.py \
    --excel clinical_batch_2025_09.xlsx \
    --url-column download_url \
    --filename-column patient_id \
    --verify-integrity

# 3. Remote processing (from home if needed)
ssh -p 2022 clinician@lab_server
screen -S clinical_batch
bash clinical_genomics_pipeline.sh batch DATA/downloaded_vcfs/ 8
# Detach and go home

# 4. Receive email when complete
# 5. Review results next morning
ssh -p 2022 clinician@lab_server
screen -r clinical_batch
cd DATA/RESULTS/VCF_ANALYSIS/individuals/
```

**💡 See more examples:** [Installation Guide - Complete Workflows](INSTALLATION_COMPLETE.md#complete-workflow-example)

---

## Installation & Setup

**📚 [Complete Installation Guide →](INSTALLATION_COMPLETE.md)**

### Prerequisites

All utilities require:
- WSL Ubuntu 22.04+ 
- Python 3.8+
- Internet connection (for downloads/remote access)

### Quick Setup (10-15 minutes)

```bash
cd /mnt/d/Genome/UTILITIES

# 1. Install Python dependencies
pip install requests pandas openpyxl

# 2. Setup VCF Downloader
cd vcf_downloader
python vcf_downloader.py --help  # Verify installation

# 3. Setup SSH Remote Access (optional)
cd ../ssh_remote_access
bash setup_ssh_access.sh
# Then run Windows setup: .\setup_port_forwarding.bat

# 4. Setup Email Notifications (if not already done)
cd ../email_notifications
bash setup_email_notifications.sh
bash test_email_integration.sh

# Done!
```

**📖 Detailed Setup Instructions:** [INSTALLATION_COMPLETE.md](INSTALLATION_COMPLETE.md)

---

## Directory Structure

```
UTILITIES/
├── README.md                          # This file
├── INSTALLATION_COMPLETE.md           # Getting started guide
├── quick_start.sh                     # Interactive setup wizard
├── verify_utilities.sh                # System verification
│
├── vcf_downloader/
│   ├── README.md                      # VCF Downloader documentation
│   ├── vcf_downloader.py              # Main download script
│   ├── download_log.txt               # Download history (generated)
│   └── example_download_list.csv      # Template file
│
├── ssh_remote_access/
│   ├── README.md                      # SSH setup guide
│   ├── SECURITY_GUIDE.md              # Security best practices
│   ├── QUICK_REFERENCE.md             # Command reference card
│   ├── setup_ssh_access.sh            # Automated setup script
│   ├── setup_port_forwarding.bat      # Windows port forwarding
│   ├── start_wsl_ssh.ps1              # Auto-start script
│   ├── restart_ssh.sh                 # Service restart
│   ├── test_ssh_connection.sh         # Connection test
│   └── show_connection_info.sh        # Display config info
│
└── email_notifications/
    ├── email_config.json              # Email configuration
    ├── pipeline_notifier.py           # Notification system
    ├── setup_email_notifications.sh   # Setup wizard
    └── test_email_integration.sh      # Test script
```

---

## Troubleshooting

### VCF Downloader Issues

**Problem:** Excel file not loading
```bash
# Install pandas with Excel support
pip install pandas openpyxl xlrd
```

**Problem:** Download timeout
- Check internet connection
- Verify URL is accessible
- Try downloading with browser first

**📖 More help:** [VCF Downloader README](vcf_downloader/README.md#troubleshooting)

### SSH Access Issues

**Problem:** Cannot connect remotely
```bash
# Check SSH is running
sudo service ssh status

# Verify port forwarding
netsh interface portproxy show v4tov4  # Windows PowerShell

# Check firewall
sudo ufw status  # WSL
```

**Problem:** Connection refused
- Verify Windows firewall allows port 2022
- Check WSL IP hasn't changed (rerun setup_port_forwarding.bat)
- Test local connection first: `ssh localhost -p 2022`

**📖 More help:** 
- [SSH Setup Guide](ssh_remote_access/README.md#troubleshooting)
- [Quick Reference Card](ssh_remote_access/QUICK_REFERENCE.md#troubleshooting-commands)

### Email Notification Issues

**Problem:** Emails not sending
```bash
# Test configuration
cd email_notifications
bash test_email_integration.sh

# Check logs
cat ~/.email_notifications_test.log
```

**Problem:** Gmail authentication failed
- Verify 2FA is enabled
- Use App Password, not regular password
- Check email/password in email_config.json

---

## Integration with Pipeline

All utilities are designed to work seamlessly with the main Clinical Genomics Pipeline:

**Main Pipeline:** [`/mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh`](../PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh)

**Documentation:** [Main Pipeline README](../MAIN_README.md)

### Utility Integration Points

1. **Before Pipeline:**
   - Use [VCF Downloader](vcf_downloader/README.md) to acquire input files
   - Setup [SSH Remote Access](ssh_remote_access/README.md) for remote work
   - Configure [Email Notifications](../EMAIL_NOTIFICATIONS_README.md)

2. **During Pipeline:**
   - Remote monitoring via [SSH](ssh_remote_access/README.md)
   - Email notifications at key steps
   - Screen/tmux for long runs ([SSH Quick Reference](ssh_remote_access/QUICK_REFERENCE.md#long-running-sessions))

3. **After Pipeline:**
   - Remote result access via [SSH/SCP](ssh_remote_access/QUICK_REFERENCE.md#file-transfer)
   - Email confirmation
   - Result download

---

## Security Considerations

### VCF Downloader
- Only download from trusted sources
- Verify SSL certificates (default)
- Use `--verify-integrity` for clinical data
- Review download_log.txt regularly

### SSH Remote Access
- Use SSH keys, not passwords
- Configure fail2ban for brute force protection
- Use VPN for internet access (recommended)
- Monitor access logs

**📖 Complete Security Guide:** [SSH Security Best Practices](ssh_remote_access/SECURITY_GUIDE.md)

### Email Notifications
- Use app passwords, not account passwords
- Secure email_config.json permissions
- Don't include PHI in email subjects/bodies
- Use encrypted email if available

---

## Support & Documentation

### Quick Access Links

| Resource | Link |
|----------|------|
| **Installation Guide** | [INSTALLATION_COMPLETE.md](INSTALLATION_COMPLETE.md) |
| **Main Pipeline** | [MAIN_README.md](../MAIN_README.md) |
| **VCF Downloader** | [vcf_downloader/README.md](vcf_downloader/README.md) |
| **SSH Setup** | [ssh_remote_access/README.md](ssh_remote_access/README.md) |
| **SSH Security** | [ssh_remote_access/SECURITY_GUIDE.md](ssh_remote_access/SECURITY_GUIDE.md) |
| **SSH Quick Ref** | [ssh_remote_access/QUICK_REFERENCE.md](ssh_remote_access/QUICK_REFERENCE.md) |
| **Email Setup** | [EMAIL_NOTIFICATIONS_README.md](../EMAIL_NOTIFICATIONS_README.md) |

### Quick Help Commands

```bash
# VCF Downloader help
python vcf_downloader/vcf_downloader.py --help

# SSH connection info
bash ssh_remote_access/show_connection_info.sh

# Verify all utilities
bash verify_utilities.sh

# Email test
bash email_notifications/test_email_integration.sh
```

### Log Files

```bash
# VCF downloads
cat vcf_downloader/download_log.txt

# SSH access
sudo tail -f /var/log/auth.log

# Email notifications
cat ~/.email_notifications_test.log
```

---

## Future Utilities (Roadmap)

Potential additions:
- [ ] **Database updater:** Automated gnomAD/ClinVar updates
- [ ] **Result archiver:** Compress and organize old results
- [ ] **Sample tracker:** Database of processed samples
- [ ] **Quality dashboard:** Web interface for QC metrics
- [ ] **Automated reporter:** Generate clinical reports automatically
- [ ] **Slack notifications:** Alternative to email
- [ ] **Cloud sync:** Backup to AWS/Azure/GCP

---

## Version History

**v1.0 (September 2025)**
- Initial release
- VCF Downloader utility
- SSH Remote Access system
- Email Notifications integration

---

## License & Usage

These utilities are part of the Clinical Genomics Pipeline and follow the same usage guidelines:

⚠️ **Research-Grade Analysis for Clinical Guidance Only**

- Computational predictions have limitations
- Clinical validation required
- Consult genetics professionals
- Not a replacement for CLIA testing

**Full Pipeline Documentation:** [MAIN_README.md](../MAIN_README.md)

---

**Utilities Suite Version:** 1.0  
**Last Updated:** September 2025  
**Maintained by:** Clinical Genomics Pipeline Team  

---

**Enhance your genomics workflow! 🧬🚀**

---

## Getting Started

**New to these utilities?** Start here:
1. 📖 [Read the Installation Guide](INSTALLATION_COMPLETE.md)
2. ✅ [Verify your setup](verify_utilities.sh)
3. 🚀 [Try the quick start wizard](quick_start.sh)
4. 📚 [Explore individual utility guides](#available-utilities)
