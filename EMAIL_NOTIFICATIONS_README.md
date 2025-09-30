# Email Notifications for Clinical Genomics Pipeline

## 🎉 Setup Complete!

Your Clinical Genomics Pipeline now includes professional email notifications that will alert you when processing completes. No more babysitting 3-hour VEP runs!

## 📧 What You'll Receive

### VEP Annotation Complete Email
- **When:** After VEP annotation finishes (~3 hours for whole genome)
- **Contains:** Processing duration, file size, variant count, next steps
- **Subject:** "✅ VEP Annotation Completed - [SAMPLE_ID]"

### Pipeline Complete Email  
- **When:** After entire pipeline finishes (all 4 steps)
- **Contains:** Total processing time, results directory, summary
- **Subject:** "✅ VEP Annotation Completed - [SAMPLE_ID]" (using same template)

### Failure Notifications
- **When:** If VEP or pipeline fails
- **Contains:** Error details, log file locations, troubleshooting info
- **Subject:** "❌ VEP Annotation Failed - [SAMPLE_ID]"

## 🚀 How to Use

### Normal Pipeline Usage (No Changes Needed!)
```bash
# Your normal pipeline commands work exactly the same
bash /mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_001 8

# Or directly run VEP annotation
bash /mnt/d/Genome/COMPONENTS/ANNOTATION/vep_clinical_annotation.sh input.vcf.gz output.vcf.gz SAMPLE_001 8
```

### What Happens Automatically
1. **Pipeline starts** - normal processing begins
2. **VEP starts** - long processing phase begins (~3 hours)
3. **📧 VEP completes** - you get an email with results
4. **Clinical analysis** - remaining steps continue
5. **📧 Pipeline completes** - you get final completion email

## 🧪 Test the System

```bash
# Test email notifications
chmod +x /mnt/d/Genome/scripts/test_email_integration.sh
bash /mnt/d/Genome/scripts/test_email_integration.sh
```

## 🔧 Configuration

### Email Settings
- **Config file:** `/mnt/d/Genome/config/email_config.json`
- **Notifier script:** `/mnt/d/Genome/scripts/pipeline_notifier.py`

### Update Email Settings
```bash
# Re-run setup to change email settings
bash /mnt/d/Genome/scripts/setup_email_notifications.sh
```

### Disable Email Notifications
Edit your pipeline scripts and change:
```bash
EMAIL_ENABLED=false
```

## 📱 Email Format

### Beautiful HTML Email Includes:
- ✅ **Status indicator** with emojis
- ⏱️ **Processing duration** (e.g., "178m 51s")
- 📊 **Metrics:** file size, variant count
- 🧬 **Pipeline details:** version, databases used
- 📁 **Next steps** and recommendations
- 🎨 **Professional formatting** with colors and structure

### Plain Text Backup
- All emails include plain text version for older email clients
- Same information in structured text format

## 🛠️ Technical Details

### Scripts Updated
1. **VEP Script:** `/mnt/d/Genome/COMPONENTS/ANNOTATION/vep_clinical_annotation.sh`
   - Added email notification functions
   - Captures start/end times
   - Sends notifications on success/failure

2. **Main Pipeline:** `/mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh`
   - Added pipeline completion notifications
   - Tracks total processing time
   - Sends final summary email

### Non-Critical Design
- Email failures don't break your pipeline
- Processing continues even if email fails
- All email calls wrapped with `|| true` for safety

### Error Handling
- **VEP failures:** Automatic error email with log details
- **Network issues:** Email skipped, processing continues
- **Config issues:** Warnings logged, pipeline proceeds

## 📊 Performance Impact

- **Minimal overhead:** <5 seconds per notification
- **No processing delay:** Emails sent asynchronously
- **Fail-safe design:** Never interrupts scientific processing

## 🔒 Security & Privacy

- **Local configuration:** Email credentials stored locally only
- **No external dependencies:** Uses standard Python libraries
- **Research data protection:** Only sample IDs sent, no genomic data

## 📞 Support & Troubleshooting

### Common Issues

**Email not received:**
1. Check spam/junk folder
2. Verify Gmail App Password (not regular password)
3. Test with: `bash test_email_integration.sh`

**Gmail setup:**
1. Enable 2-factor authentication
2. Create App Password at: https://myaccount.google.com/security
3. Use 16-character App Password in config

**Configuration issues:**
```bash
# Re-run setup
bash /mnt/d/Genome/scripts/setup_email_notifications.sh

# Check logs
tail -f /mnt/d/Genome/DATA/LOGS/master_pipeline.log
```

### Log Files
- **Pipeline logs:** `/mnt/d/Genome/DATA/LOGS/master_pipeline.log`
- **VEP logs:** `/mnt/d/Genome/DATA/LOGS/vep_annotation.log`
- **Email debug:** Shown in pipeline logs

## 🎯 Example Usage Workflow

1. **Start your analysis:**
   ```bash
   cd /mnt/d/Genome
   bash PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh single input.vcf.gz PATIENT_123 8
   ```

2. **Walk away!** ☕ Go get coffee, lunch, or work on other things

3. **📧 Get VEP email** (~3 hours later):
   - "✅ VEP Annotation Completed - PATIENT_123"
   - Processing time: "178m 51s"
   - Variants: "4,737,881 variants"
   - File size: "1.2G"

4. **📧 Get final email** (when everything completes):
   - "✅ VEP Annotation Completed - PATIENT_123" 
   - Total time: "4h 15m"
   - Results location: organized directory structure

5. **Review results** using the provided file paths in emails

## 🚀 Ready to Go!

Your pipeline now includes enterprise-grade notifications. Enjoy the freedom to walk away from long-running genomics analyses while staying informed about progress and completion!

---
*Clinical Genomics Pipeline v4.1 with Email Notifications*
*Research-grade analysis for clinical guidance*
