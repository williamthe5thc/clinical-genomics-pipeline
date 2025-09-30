# Email Notification System for Clinical Genomics Pipeline

## Overview

Enterprise-grade email notification system that alerts you when your long-running genomics analyses complete or fail. No more babysitting 3-hour VEP runs!

**Status:** ✅ Fully Integrated  
**Location:** `/mnt/d/Genome/UTILITIES/email_notifications/`  
**Pipeline Integration:** Automatic - no code changes needed

---

## Features

### 🎯 **Comprehensive Notification Coverage**
- ✅ **VEP Annotation Completion** (~3 hours) - Get notified when annotation finishes
- ✅ **Pipeline Completion** - Know when all analysis steps are done
- ✅ **Failure Alerts at ANY Point** - Immediate notification if Step 1, 2, 3, or 4 fails
- ✅ **Exception Handling** - Catches and reports all pipeline errors

### 📧 **Rich Email Content**
- **Beautiful HTML Formatting:** Professional emails with status indicators, colors, and structured layout
- **Processing Metrics:** Duration (e.g., "176m 47s"), file sizes (e.g., "1.2G"), variant counts (e.g., "4,737,881 variants")
- **Next Steps Guidance:** What to do after completion or how to troubleshoot failures
- **Log File References:** Direct paths to logs for debugging
- **Plain Text Fallback:** Works with all email clients

### 💪 **Fail-Safe Design**
- **Non-Critical:** Email failures never interrupt your scientific processing
- **Resilient:** Pipeline continues even if email service is down
- **Safe Defaults:** All email functions have default values to prevent crashes

---

## Quick Setup (5 Minutes)

### Step 1: Run Setup Script

```bash
cd /mnt/d/Genome/UTILITIES/email_notifications
bash setup_email_notifications.sh
```

This interactive script will:
1. Ask for your email address
2. Ask for your email password (App Password for Gmail)
3. Create `email_config.json` with your settings
4. Send a test email to verify everything works

### Step 2: Gmail Setup (Recommended)

**Why Gmail?** Most reliable SMTP service, easy setup, free.

**Setup Steps:**
1. Go to https://myaccount.google.com/security
2. Enable **2-Factor Authentication** (required for App Passwords)
3. Click **App Passwords** (may need to search for it)
4. Select **Mail** and **Other (custom name)**
5. Enter "Clinical Genomics Pipeline"
6. **Copy the 16-character password** (looks like: `xxxx xxxx xxxx xxxx`)
7. Use this App Password in the setup script (not your regular Gmail password)

**Important:** Do NOT use your regular Gmail password - it won't work. You MUST use an App Password.

### Step 3: Test Email System

```bash
bash test_email_integration.sh
```

This will send test emails for both success and failure scenarios. Check your inbox (and spam folder) to verify they arrive.

### Step 4: Run Your Pipeline

```bash
# Your existing commands work exactly the same!
bash /mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_001 8

# Or run VEP directly
bash /mnt/d/Genome/COMPONENTS/ANNOTATION/vep_clinical_annotation.sh input.vcf.gz output.vcf.gz SAMPLE_001 8
```

**That's it!** Emails will be sent automatically at key points.

---

## What You'll Receive

### ✅ Success Email - VEP Annotation Completed

**When:** After VEP annotation finishes (~3 hours for whole genome)

**Subject:** `✅ VEP Annotation Completed - SAMPLE_001`

**Contains:**
- ⏱️ Processing duration: "176m 47s"
- 📊 Metrics:
  - File size: "1.2G"
  - Variant count: "4,737,881 variants"
  - Output format: "VCF"
- 📁 Output file location
- 🧬 Pipeline info: Version, databases used, assembly
- 📈 Next steps: "Multi-specialty analysis will begin automatically"
- 📅 Timestamp: When email was generated

**Example:**
```
✅ Clinical Genomics Pipeline
VEP Annotation COMPLETED SUCCESSFULLY

Sample ID: CS335A_TEST
Processing Time: 176m 47s
Started: Sun Sep 28 15:23:51 MDT 2025
Completed: Sun Sep 28 18:20:38 MDT 2025

4,737,881 Variants | 1.2G File Size | VCF Output Format

Output File: CS335A_TEST_comprehensive.vcf.gz
Pipeline Stage: VEP v114.2

🧬 Pipeline Information
System: Clinical Genomics Pipeline v114.2
Location: /mnt/d/Genome (WSL Ubuntu 22.04)
Assembly: GRCh38
Databases: gnomAD v4.1, ClinVar September 2025
Next Steps: Multi-specialty analysis will begin automatically
```

### ✅ Success Email - Full Pipeline Completed

**When:** After all 4 steps finish (VCF preprocessing, VEP annotation, clinical analysis, reports)

**Subject:** `✅ VEP Annotation Completed - SAMPLE_001`

**Contains:**
- Total pipeline duration
- Final variant count
- Results directory location
- Summary of all steps

### ❌ Failure Email - Any Pipeline Failure

**When:** ANY step fails (Step 1, 2, 3, or 4) or exception occurs

**Subject:** `❌ VEP Annotation Failed - SAMPLE_001`

**Contains:**
- 🚨 Error message and details
- 📁 Log file locations for debugging
- 🔍 Failed step identification
- 💡 Troubleshooting guidance
- ⏱️ Time when failure occurred

**Example:**
```
❌ Clinical Genomics Pipeline
VEP Annotation FAILED

Sample ID: CS335A_TEST
Processing Time: 45m 12s
Started: Sun Sep 28 15:23:51 MDT 2025
Failed: Sun Sep 28 16:09:03 MDT 2025

🚨 Error Details:
Step 2 - VEP annotation failed. Check VEP logs: /mnt/d/Genome/DATA/LOGS/vep_annotation.log

Action Required:
1. Check log files in /mnt/d/Genome/DATA/LOGS/
2. Review VEP configuration and input files
3. Restart pipeline after resolving issues
```

---

## Configuration Files

### `email_config.json`
Your email settings (created by setup script):

```json
{
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email_user": "your_email@gmail.com",
    "email_password": "your_16_char_app_password",
    "recipient_email": "your_email@gmail.com",
    "sender_name": "Clinical Genomics Pipeline",
    "enable_notifications": true
}
```

**Security Note:** This file contains your email password. Keep it secure:
- Don't commit to Git (already in .gitignore)
- Use App Password, not your main password
- Restrict file permissions: `chmod 600 email_config.json`

### `email_config_template.json`
Template for reference (safe to commit to version control)

---

## Advanced Configuration

### Using Different Email Providers

**Outlook/Hotmail:**
```json
{
    "smtp_server": "smtp-mail.outlook.com",
    "smtp_port": 587,
    "email_user": "your_email@outlook.com",
    "email_password": "your_password"
}
```

**Yahoo:**
```json
{
    "smtp_server": "smtp.mail.yahoo.com",
    "smtp_port": 587,
    "email_user": "your_email@yahoo.com",
    "email_password": "your_app_password"
}
```

**Custom SMTP Server:**
```json
{
    "smtp_server": "mail.yourcompany.com",
    "smtp_port": 587,
    "email_user": "your_email@yourcompany.com",
    "email_password": "your_password"
}
```

### Disable Notifications Temporarily

**Option 1 - Edit config file:**
```json
{
    "enable_notifications": false
}
```

**Option 2 - Edit pipeline scripts:**
```bash
EMAIL_ENABLED=false
```

### Send Notifications to Multiple Recipients

Currently supports one recipient. To notify multiple people:
1. Set up email forwarding in your email provider
2. Or create a mailing list/group email address

---

## Integration Details

### Files in This Directory

- **`pipeline_notifier.py`** - Main Python script that sends emails
- **`email_config.json`** - Your email configuration (not in Git)
- **`email_config_template.json`** - Template for reference
- **`setup_email_notifications.sh`** - Interactive setup script
- **`test_email_integration.sh`** - Test email system
- **`integration_guide.sh`** - Code snippets for manual integration
- **`README.md`** - This file

### How It Works

**1. Pipeline Scripts Include Email Functions:**

Both main pipeline scripts have been updated:
- `/mnt/d/Genome/COMPONENTS/ANNOTATION/vep_clinical_annotation.sh` (VEP script)
- `/mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh` (Main pipeline)

**2. Notifications Sent at Key Points:**

**Success Notifications:**
- After VEP annotation completes successfully
- After full pipeline completes successfully

**Failure Notifications:**
- Step 1 (VCF preprocessing) fails
- Step 2 (VEP annotation) fails
- Step 3 (Clinical analysis) fails
- Any uncaught exception or error

**3. Email Function Design:**

```bash
send_email_notification "notification_type" "sample_id" "start_time" "end_time" \
                       "output_file" "file_size" "variant_count" "error_message"
```

All parameters have safe defaults - missing parameters won't crash the pipeline.

**4. Non-Critical Execution:**

```bash
python3 "${EMAIL_NOTIFIER}" --type "vep_completion" ... || {
    log_warning "Email notification failed (non-critical)"
}
```

The `|| true` pattern ensures pipeline continues even if email fails.

---

## Troubleshooting

### Common Issues

**❌ Email not received:**
1. **Check spam/junk folder** - first time emails often go to spam
2. **Verify App Password** - must use 16-char App Password for Gmail, not regular password
3. **Check 2FA enabled** - Gmail requires 2-factor authentication for App Passwords
4. **Test manually:** `bash test_email_integration.sh`

**❌ "Authentication failed" error:**
- **Gmail:** Must use App Password, not regular password
- **Other providers:** Check if SMTP username is full email or just username
- **Security:** Some providers require "less secure app access" to be enabled

**❌ "Connection refused" error:**
- Check SMTP server and port are correct
- Verify firewall isn't blocking port 587
- Try port 465 (SSL) or 25 (alternative)

**❌ "$8: unbound variable" error:**
- Already fixed! Email function parameters now have safe defaults
- Update your scripts if you have old versions

**❌ Pipeline continues without email:**
- This is by design (non-critical)
- Check logs: `tail -f /mnt/d/Genome/DATA/LOGS/master_pipeline.log`
- Email issues won't interrupt your genomics analysis

### Debug Mode

Check what's happening with emails:

```bash
# View pipeline logs
tail -f /mnt/d/Genome/DATA/LOGS/master_pipeline.log

# Test email manually
python3 pipeline_notifier.py \
  --type vep_completion \
  --sample-id TEST \
  --start-time "$(date)" \
  --variant-count 1000000 \
  --config email_config.json
```

### Reconfigure Email

Run setup again to change settings:

```bash
bash setup_email_notifications.sh
```

---

## Example Workflow

### Your Complete Workflow with Email Notifications

**1. Setup (one-time, 5 minutes):**
```bash
cd /mnt/d/Genome/UTILITIES/email_notifications
bash setup_email_notifications.sh
bash test_email_integration.sh  # Verify it works
```

**2. Run your pipeline (normal usage, unchanged):**
```bash
cd /mnt/d/Genome
bash PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh single \
  DATA/INPUTS/raw_vcfs/patient.vcf.gz \
  PATIENT_001 8
```

**3. Walk away! ☕**
- Go get coffee
- Work on other tasks
- Take a lunch break
- No need to check progress

**4. Get VEP email (~3 hours later):**
```
Subject: ✅ VEP Annotation Completed - PATIENT_001
Processing Time: 176m 47s
Variants: 4,737,881 variants
File Size: 1.2G
```

**5. Get final email (when everything completes):**
```
Subject: ✅ VEP Annotation Completed - PATIENT_001
Total Time: 3h 45m
Results: /mnt/d/Genome/DATA/RESULTS/VCF_ANALYSIS/individuals/PATIENT_001/
```

**6. Review results using paths from email**

**7. If anything fails:**
```
Subject: ❌ VEP Annotation Failed - PATIENT_001
Error: Step 2 - VEP annotation failed
Logs: /mnt/d/Genome/DATA/LOGS/vep_annotation.log
```

---

## Security & Privacy

### Data Privacy
- **Only sample IDs sent** - No genomic data in emails
- **Local configuration** - Email credentials stored locally only
- **No external dependencies** - Uses standard Python libraries
- **Research-grade system** - Not for production clinical use

### Credentials Security
- **App Passwords:** Use Gmail App Passwords (revocable, limited scope)
- **File Permissions:** Set `chmod 600 email_config.json`
- **Git Ignored:** Config file already excluded from version control
- **Local Only:** Credentials never leave your system

### Best Practices
1. Use App Passwords instead of account passwords
2. Create a dedicated Gmail account for pipeline notifications
3. Don't share your `email_config.json` file
4. Revoke App Password if compromised (easy in Gmail settings)
5. Use strong, unique App Password

---

## Performance Impact

- **Overhead:** <5 seconds per email notification
- **Processing:** No delay in scientific computing
- **Network:** Minimal bandwidth usage
- **Memory:** Negligible impact
- **Total Impact:** ~10 seconds across entire 3-hour pipeline

---

## Support

### Getting Help

**Configuration Issues:**
```bash
# Re-run setup
bash setup_email_notifications.sh

# Test system
bash test_email_integration.sh

# Check logs
tail -f /mnt/d/Genome/DATA/LOGS/master_pipeline.log
```

**Email Provider Help:**
- **Gmail:** https://support.google.com/accounts/answer/185833
- **Outlook:** https://support.microsoft.com/en-us/office/pop-imap-and-smtp-settings
- **Yahoo:** https://help.yahoo.com/kb/SLN4075.html

### Additional Resources

- Main README: `/mnt/d/Genome/MAIN_README.md`
- Pipeline logs: `/mnt/d/Genome/DATA/LOGS/`
- Setup script: `setup_email_notifications.sh` (run anytime)
- Test script: `test_email_integration.sh` (verify setup)

---

## Future Enhancements

Potential future additions:
- Multiple recipient support
- SMS/text notifications
- Slack/Teams integration
- Custom notification templates
- Progress updates (not just completion)
- Batch processing summaries

---

**Version:** 1.0  
**Status:** Production Ready  
**Last Updated:** September 2025  
**Compatibility:** Clinical Genomics Pipeline v4.1+

*Enjoy hands-free genomics analysis with enterprise-grade notifications!*
