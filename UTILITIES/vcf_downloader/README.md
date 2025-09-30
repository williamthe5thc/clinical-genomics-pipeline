# VCF Downloader Utility

**Automated VCF file download system for the Clinical Genomics Pipeline**

**📚 Quick Navigation:**
- [← Back to Utilities](../README.md) | [Installation Guide](../INSTALLATION_COMPLETE.md)
- **Other Utilities:** [SSH Remote Access](../ssh_remote_access/README.md) | [Email Notifications](../../EMAIL_NOTIFICATIONS_README.md)
- [Main Pipeline →](../../MAIN_README.md)

---

## Overview

The VCF Downloader is a Python utility that simplifies downloading VCF files from remote URLs, with special support for batch downloads from Excel spreadsheets. This is particularly useful when working with large genomics datasets hosted on external servers.

---

## Features

✅ **Single URL Downloads**
- Download individual VCF files from any URL
- Custom filename support
- Progress tracking with speed and ETA

✅ **Batch Excel Processing**
- Process Excel files with multiple download links
- Automatic organization and naming
- Support for custom filename columns

✅ **Robust Download Management**
- Resume support for interrupted downloads
- SSL certificate verification (optional)
- Duplicate file detection and handling
- Comprehensive error logging

✅ **VCF Integrity Verification**
- Optional post-download validation
- Checks VCF header format
- Supports both gzipped and uncompressed files

✅ **Progress Tracking**
- Real-time download progress
- Speed monitoring (MB/s)
- Estimated time remaining
- Total download statistics

---

## Installation

### Requirements

```bash
# Install required Python packages
pip install requests pandas openpyxl

# Or use the existing environment
conda activate clinical_genomics
pip install requests pandas openpyxl
```

### Verify Installation

```bash
cd /mnt/d/Genome/UTILITIES/vcf_downloader
python vcf_downloader.py --help
```

---

## Quick Start

### Example 1: Download Single VCF

```bash
# Basic download
python vcf_downloader.py --url https://example.com/sample.vcf.gz

# With custom filename
python vcf_downloader.py \
    --url https://example.com/sample.vcf.gz \
    --filename patient_001.vcf.gz

# With integrity verification
python vcf_downloader.py \
    --url https://example.com/sample.vcf.gz \
    --verify-integrity
```

### Example 2: Batch Download from Excel

**Excel File Format (download_list.xlsx):**

| url                                      | filename          |
|------------------------------------------|-------------------|
| https://example.com/sample1.vcf.gz      | patient_001.vcf.gz|
| https://example.com/sample2.vcf.gz      | patient_002.vcf.gz|
| https://example.com/sample3.vcf.gz      | patient_003.vcf.gz|

**Download Command:**

```bash
# Using default 'url' column
python vcf_downloader.py --excel download_list.xlsx

# With custom column names
python vcf_downloader.py \
    --excel download_list.xlsx \
    --url-column download_url \
    --filename-column sample_name

# Specify sheet and verify
python vcf_downloader.py \
    --excel download_list.xlsx \
    --sheet "Sample Links" \
    --verify-integrity
```

### Example 3: Custom Output Directory

```bash
# Specify custom download location
python vcf_downloader.py \
    --url https://example.com/sample.vcf.gz \
    --output-dir /mnt/d/custom/vcf/location
```

---

## Command-Line Options

### Required Arguments (choose one)

| Option | Description |
|--------|-------------|
| `--url URL` | Single URL to download |
| `--excel FILE` | Excel file containing multiple URLs |

### Optional Arguments

| Option | Description | Default |
|--------|-------------|---------|
| `--filename NAME` | Custom filename for single download | (auto-detected) |
| `--output-dir PATH` | Download destination directory | `/mnt/d/Genome/DATA/downloaded_vcfs` |
| `--url-column NAME` | Excel column containing URLs | `url` |
| `--filename-column NAME` | Excel column for custom filenames | (none) |
| `--sheet NAME` | Excel sheet name or index | `0` (first sheet) |
| `--verify-integrity` | Verify VCF files after download | (disabled) |
| `--no-ssl-verify` | Disable SSL certificate checks | (enabled) |

---

## Excel File Guidelines

### Basic Format

```
Column A: url (required)
Column B: filename (optional)
```

### Example Excel Structure

**Sheet 1: Patient Samples**

| url | filename | notes |
|-----|----------|-------|
| https://data.server.com/vcfs/WGS001.vcf.gz | patient_cardiac_001.vcf.gz | CDLS suspected |
| https://data.server.com/vcfs/WGS002.vcf.gz | patient_cardiac_002.vcf.gz | Family member |

**Usage:**
```bash
python vcf_downloader.py \
    --excel samples.xlsx \
    --sheet "Patient Samples" \
    --filename-column filename
```

### Column Name Flexibility

The tool supports various column naming conventions:
- `url`, `URL`, `link`, `download_link`
- `filename`, `sample_name`, `sample_id`

Specify with `--url-column` and `--filename-column` flags.

---

## Output and Logs

### Default Output Location

```
/mnt/d/Genome/DATA/downloaded_vcfs/
├── patient_001.vcf.gz
├── patient_002.vcf.gz
└── ...
```

### Log Files

```
/mnt/d/Genome/UTILITIES/vcf_downloader/download_log.txt
```

**Log contents:**
- Download start/completion times
- File sizes and transfer speeds
- Error messages and stack traces
- Verification results

---

## Integration with Pipeline

### After Single Download

```bash
# 1. Download VCF
python vcf_downloader.py --url https://example.com/sample.vcf.gz

# 2. Run pipeline on downloaded file
bash clinical_genomics_pipeline.sh single \
    /mnt/d/Genome/DATA/downloaded_vcfs/sample.vcf.gz \
    SAMPLE_001 8
```

### After Batch Download

```bash
# 1. Download multiple VCFs
python vcf_downloader.py --excel download_list.xlsx

# 2. Batch process all downloaded files
bash clinical_genomics_pipeline.sh batch \
    /mnt/d/Genome/DATA/downloaded_vcfs/ \
    8
```

---

## Common Use Cases

### Use Case 1: Research Collaboration

Download VCFs shared by collaborators:

```bash
# Collaborator sends Excel with links to their server
python vcf_downloader.py \
    --excel collaborator_samples.xlsx \
    --verify-integrity
```

### Use Case 2: Public Database Access

Download from public genomics databases:

```bash
# Download from 1000 Genomes, gnomAD, etc.
python vcf_downloader.py \
    --url https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/sample.vcf.gz
```

### Use Case 3: Clinical Sample Processing

Batch download patient VCFs:

```bash
# Clinical lab shares secure links
python vcf_downloader.py \
    --excel clinical_batch_2025_09.xlsx \
    --url-column secure_download_url \
    --filename-column patient_id \
    --verify-integrity
```

---

## Troubleshooting

### Issue: SSL Certificate Error

**Symptom:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```bash
# Only for trusted sources!
python vcf_downloader.py \
    --url https://internal-server.com/sample.vcf.gz \
    --no-ssl-verify
```

### Issue: Excel Column Not Found

**Symptom:**
```
Column 'url' not found in Excel file
```

**Solution:**
```bash
# Check available columns first
# Then specify correct column name
python vcf_downloader.py \
    --excel file.xlsx \
    --url-column "Download Link"
```

### Issue: Download Timeout

**Symptom:**
```
Connection timeout after 300 seconds
```

**Solution:**
- Check network connection
- Try downloading directly with browser to verify URL
- Server may be rate-limiting requests

### Issue: File Already Exists

**Behavior:**
- Downloader prompts: "Overwrite filename? (y/n)"
- Enter `y` to replace, `n` to skip

**Automated Solution:**
```bash
# Delete old files first
rm /mnt/d/Genome/DATA/downloaded_vcfs/*
python vcf_downloader.py --excel download_list.xlsx
```

---

## Advanced Features

### Resuming Failed Downloads

The downloader automatically handles partial downloads:

1. If download fails midway, simply rerun the same command
2. Already completed files will be skipped
3. Failed files can be retried individually

### Custom Download Locations

Organize downloads by project:

```bash
# Create project-specific directories
python vcf_downloader.py \
    --excel cdls_patients.xlsx \
    --output-dir /mnt/d/Genome/DATA/projects/cdls_2025/vcfs

python vcf_downloader.py \
    --excel cardiac_patients.xlsx \
    --output-dir /mnt/d/Genome/DATA/projects/cardiac_2025/vcfs
```

### Batch Processing Workflow

Complete automation example:

```bash
#!/bin/bash
# download_and_process.sh

# Step 1: Download VCFs
echo "Downloading VCF files..."
python /mnt/d/Genome/UTILITIES/vcf_downloader/vcf_downloader.py \
    --excel sample_list.xlsx \
    --verify-integrity

# Step 2: Wait for user confirmation
read -p "Press enter to start pipeline processing..."

# Step 3: Process all downloaded files
echo "Starting pipeline processing..."
bash /mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh batch \
    /mnt/d/Genome/DATA/downloaded_vcfs/ \
    8

echo "Complete!"
```

---

## Performance Tips

1. **Network Speed**: Downloads limited by your internet connection
2. **Multiple Files**: Downloads process sequentially with 1-second pause between
3. **Large Files**: Expect ~10-30 minutes for whole genome VCFs (10-50 GB each)
4. **Parallel Downloads**: Not currently supported (prevents server overload)

---

## Security Considerations

⚠️ **Important Security Notes:**

1. **Trusted Sources Only**: Only download from trusted, verified sources
2. **SSL Verification**: Keep enabled unless absolutely necessary
3. **File Validation**: Always use `--verify-integrity` for clinical data
4. **Access Control**: Ensure download directory has appropriate permissions
5. **Audit Trail**: Review `download_log.txt` regularly

---

## Support and Updates

**Location:** `/mnt/d/Genome/UTILITIES/vcf_downloader/`

**Documentation:** This README

**Log Files:** `download_log.txt`

**Version:** 1.0 (September 2025)

**Maintainer:** Clinical Genomics Pipeline Team

---

## Example Complete Workflow

```bash
# 1. Create Excel file with sample URLs
cat > samples.xlsx
# (Add URLs and sample names)

# 2. Download all VCFs
cd /mnt/d/Genome/UTILITIES/vcf_downloader
python vcf_downloader.py \
    --excel samples.xlsx \
    --verify-integrity

# 3. Review download log
cat download_log.txt

# 4. Process downloaded samples
cd /mnt/d/Genome
bash clinical_genomics_pipeline.sh batch \
    DATA/downloaded_vcfs/ \
    8

# 5. Review results
ls -lh DATA/RESULTS/VCF_ANALYSIS/individuals/
```

---

**Happy downloading! 🧬**
