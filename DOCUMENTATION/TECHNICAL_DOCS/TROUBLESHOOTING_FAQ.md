# Clinical Genomics Pipeline - Troubleshooting Guide & FAQ v4.1

**Comprehensive Solutions for Common Issues, Error Messages, and Frequently Asked Questions**

This guide provides solutions to common problems, detailed error explanations, and answers to frequently asked questions about the Clinical Genomics Pipeline system.

---

## 📋 Table of Contents

1. [Quick Diagnostic Commands](#quick-diagnostic-commands)
2. [Common Installation Issues](#common-installation-issues)
3. [Pipeline Execution Problems](#pipeline-execution-problems)
4. [VEP Annotation Issues](#vep-annotation-issues)
5. [Performance and Resource Issues](#performance-and-resource-issues)
6. [Database and File Issues](#database-and-file-issues)
7. [Results Interpretation Issues](#results-interpretation-issues)
8. [Frequently Asked Questions](#frequently-asked-questions)

---

## 🔍 Quick Diagnostic Commands

### **System Status Check**

```bash
#!/bin/bash
# Quick system diagnostic - run this first for any issues

echo "=== Clinical Genomics Pipeline Diagnostic ==="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Working Directory: $(pwd)"
echo

echo "=== System Resources ==="
echo "Available RAM: $(free -h | awk 'NR==2{printf "%.1fGB (%.1f%% used)", $3/1024, $3*100/$2}')"
echo "Available Disk: $(df -h /mnt/d/Genome | awk 'NR==2{print $4 " (" $5 " used)"}')"
echo "CPU Cores: $(nproc)"
echo

echo "=== Essential Tools ==="
for tool in conda python bcftools vep bgzip tabix; do
    if command -v $tool &> /dev/null; then
        version=$(case $tool in
            conda) conda --version ;;
            python) python --version ;;
            bcftools) bcftools --version | head -1 ;;
            vep) vep --help 2>&1 | head -1 | grep -o "ensembl-vep.*" ;;
            *) $tool --version 2>&1 | head -1 ;;
        esac)
        echo "✅ $tool: $version"
    else
        echo "❌ $tool: NOT FOUND"
    fi
done
echo

echo "=== Directory Structure ==="
for dir in PIPELINES COMPONENTS databases DATA; do
    if [ -d "/mnt/d/Genome/$dir" ]; then
        size=$(du -sh "/mnt/d/Genome/$dir" 2>/dev/null | cut -f1)
        echo "✅ $dir: $size"
    else
        echo "❌ $dir: MISSING"
    fi
done
echo

echo "=== Recent Pipeline Logs ==="
if [ -f "/mnt/d/Genome/DATA/LOGS/master_pipeline.log" ]; then
    echo "Last 5 log entries:"
    tail -5 /mnt/d/Genome/DATA/LOGS/master_pipeline.log
else
    echo "❌ No pipeline logs found"
fi
echo

echo "=== Environment Check ==="
echo "CONDA_DEFAULT_ENV: ${CONDA_DEFAULT_ENV:-NOT SET}"
echo "PATH includes VEP: $(echo $PATH | grep -o ensembl-vep || echo "NO")"
echo "Base directory accessible: $([ -w /mnt/d/Genome ] && echo "YES" || echo "NO")"
```

### **Pipeline Status Check**

```bash
# Check if pipeline is currently running
ps aux | grep -E "(clinical_genomics_pipeline|vep|python.*comprehensive)" | grep -v grep

# Check for stuck processes
ps aux | awk '$8 ~ /D/ {print "Stuck process:", $2, $11}' | head -5

# Check system load
uptime
iostat -x 1 2 | tail -1  # Disk I/O
```

### **Quick File Validation**

```bash
# Validate essential files
echo "=== File Validation ==="

# Check main pipeline
if [ -x "/mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh" ]; then
    echo "✅ Main pipeline executable"
else
    echo "❌ Main pipeline missing or not executable"
fi

# Check databases
echo "Database sizes:"
du -sh /mnt/d/Genome/databases/*/ 2>/dev/null | sort -hr

# Check recent results
echo "Recent results:"
find /mnt/d/Genome/DATA/RESULTS -name "SAMPLE_ANALYSIS_SUMMARY.md" -mtime -7 | head -3
```

---

## 🛠️ Common Installation Issues

### **Issue 1: Conda Installation Fails**

**Symptoms:**
- `conda: command not found`
- Permission denied errors during conda install
- Environment creation fails

**Solution 1 - Fix PATH:**
```bash
# Add conda to PATH manually
export PATH="$HOME/miniconda3/bin:$PATH"
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
conda --version
```

**Solution 2 - Reinstall Conda:**
```bash
# Remove old installation
rm -rf $HOME/miniconda3

# Download and install fresh
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
$HOME/miniconda3/bin/conda init
source ~/.bashrc
```

**Solution 3 - Use System Package Manager:**
```bash
# Ubuntu/Debian alternative
sudo apt update
sudo apt install python3-pip python3-pandas python3-numpy
pip3 install cyvcf2 pyyaml
```

### **Issue 2: VEP Installation Problems**

**Symptoms:**
- `perl: command not found`
- CPAN module installation fails
- Cache download errors

**Solution 1 - Install Perl Dependencies:**
```bash
# Ubuntu/Debian
sudo apt install perl perl-modules build-essential

# CentOS/RHEL
sudo yum install perl perl-devel perl-CPAN

# Install required CPAN modules
sudo cpan install Archive::Zip DBI DBD::mysql
```

**Solution 2 - Alternative VEP Installation:**
```bash
# Use conda instead
conda install -c bioconda ensembl-vep

# Or use Docker
docker pull ensemblorg/ensembl-vep:latest
```

**Solution 3 - Manual Cache Installation:**
```bash
cd /mnt/d/Genome/databases/vep_cache
wget http://ftp.ensembl.org/pub/release-114/variation/indexed_vep_cache/homo_sapiens_vep_114_GRCh38.tar.gz
tar -xzf homo_sapiens_vep_114_GRCh38.tar.gz
rm homo_sapiens_vep_114_GRCh38.tar.gz
```

### **Issue 3: Database Download Failures**

**Symptoms:**
- `wget: connection timeout`
- Partial file downloads
- Disk space errors during download

**Solution 1 - Resume Interrupted Downloads:**
```bash
# Resume wget downloads
wget -c <URL>

# Check partial downloads
ls -la *.tmp *.part
```

**Solution 2 - Use Alternative Download Methods:**
```bash
# Use curl instead of wget
curl -L -O -C - <URL>

# Use aria2 for parallel downloads
aria2c -x 4 -s 4 <URL>

# Use rsync for FTP sources
rsync -avz --progress rsync://ftp.site/path/file .
```

**Solution 3 - Download Individual Files:**
```bash
# Download gnomAD one chromosome at a time
for chr in 1 2 3; do
    wget -c "https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1/exomes/gnomad.exomes.v4.1.sites.chr${chr}.vcf.bgz"
    echo "Completed chromosome $chr"
    sleep 10  # Brief pause between downloads
done
```

### **Issue 4: Permission and Ownership Problems**

**Symptoms:**
- `Permission denied` errors
- Cannot write to directories
- Cannot execute scripts

**Solution:**
```bash
# Fix ownership of entire Genome directory
sudo chown -R $(whoami):$(whoami) /mnt/d/Genome

# Fix permissions
chmod -R 755 /mnt/d/Genome
chmod +x /mnt/d/Genome/PIPELINES/VCF_PIPELINE/*.sh
chmod +x /mnt/d/Genome/COMPONENTS/ANNOTATION/*.sh

# Verify permissions
ls -la /mnt/d/Genome/PIPELINES/VCF_PIPELINE/
```

---

## ⚙️ Pipeline Execution Problems

### **Issue 1: Pipeline Fails at Startup**

**Error Messages:**
- `bash: clinical_genomics_pipeline.sh: command not found`
- `No such file or directory`
- `Pipeline scripts verification failed`

**Diagnosis:**
```bash
# Check if you're in the right directory
pwd
ls -la PIPELINES/VCF_PIPELINE/

# Check if script exists and is executable
ls -la PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh
```

**Solution:**
```bash
# Navigate to correct directory
cd /mnt/d/Genome

# Make script executable
chmod +x PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh

# Run with full path
bash /mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh --help
```

### **Issue 2: VCF Preprocessing Fails**

**Error Messages:**
- `ERROR: Input VCF not found`
- `VCF preprocessing failed`
- `DRAGEN header issues detected`

**Diagnosis:**
```bash
# Check input file exists and is readable
ls -la input.vcf.gz
file input.vcf.gz

# Check VCF format
bcftools view input.vcf.gz | head -20
```

**Solution 1 - File Path Issues:**
```bash
# Use absolute path
bash clinical_genomics_pipeline.sh single \
    /full/path/to/input.vcf.gz \
    SAMPLE_ID 8

# Or ensure relative path is correct
ls -la DATA/INPUTS/raw_vcfs/input.vcf.gz
```

**Solution 2 - VCF Format Issues:**
```bash
# Fix VCF format if needed
bcftools sort input.vcf > input_sorted.vcf
bgzip input_sorted.vcf
tabix -p vcf input_sorted.vcf.gz

# Validate VCF
bcftools stats input_sorted.vcf.gz > validation_stats.txt
```

**Solution 3 - DRAGEN-Specific Issues:**
```bash
# The pipeline should automatically fix DRAGEN issues
# If it fails, check the preprocessing log:
cat DATA/LOGS/maximum_quality_processing_SAMPLE_ID.log

# Manual DRAGEN header fix if needed:
zcat input.vcf.gz | sed 's/ReatPosRankSum/ReadPosRankSum/g' | bgzip > fixed_input.vcf.gz
```

### **Issue 3: Pipeline Hangs or Stalls**

**Symptoms:**
- Pipeline stops responding
- No progress for >30 minutes
- High CPU usage but no output

**Diagnosis:**
```bash
# Check what's running
ps aux | grep -E "(vep|python|bcftools)" | grep -v grep

# Check system resources
htop
iotop -o  # Check disk I/O

# Check if waiting for user input
ps aux | awk '$8 ~ /S\+/ {print $2, $11}' | head -10
```

**Solution 1 - Kill and Restart:**
```bash
# Find pipeline processes
pgrep -f "clinical_genomics_pipeline"

# Kill gracefully
pkill -f "clinical_genomics_pipeline"
pkill -f "vep"

# Wait and force kill if needed
sleep 30
pkill -9 -f "clinical_genomics_pipeline"

# Clean up temporary files
rm -rf DATA/PROCESSED/vcf_processed/*_temp*
```

**Solution 2 - Reduce Resource Usage:**
```bash
# Restart with fewer threads
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_ID 4

# Monitor progress
tail -f DATA/LOGS/master_pipeline.log
```

### **Issue 4: Memory Issues**

**Error Messages:**
- `Killed` (process terminated by system)
- `Cannot allocate memory`
- `Out of memory`

**Diagnosis:**
```bash
# Check memory usage
free -h
cat /proc/meminfo | grep Available

# Check for memory leaks
ps aux --sort=-%mem | head -10
```

**Solution 1 - Increase Swap:**
```bash
# Check current swap
swapon --show

# Create swap file if needed
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Solution 2 - Reduce Memory Usage:**
```bash
# Reduce VEP buffer size in the annotation script
# Edit COMPONENTS/ANNOTATION/vep_clinical_annotation.sh
# Change: --buffer_size 50000
# To: --buffer_size 25000

# Use fewer parallel processes
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_ID 2
```

---

## 🧬 VEP Annotation Issues

### **Issue 1: VEP Plugin Warnings**

**Common Warnings:**
```
WARNING: Plugin 'dbNSFP' went wrong: Can't locate...
WARNING: Plugin 'SpliceAI' went wrong: Authentication required
WARNING: Plugin 'CADD' went wrong: File not found
```

**Understanding Plugin Warnings:**
- **These are typically NON-CRITICAL**
- Core VEP annotation continues without plugins
- Pipeline performance is not significantly affected

**Solution 1 - Ignore Non-Critical Warnings:**
```bash
# Check if core annotation worked
grep "VEP" DATA/LOGS/master_pipeline.log
ls -la vep_annotation/*_comprehensive.vcf.gz

# Verify variants were annotated
bcftools view vep_annotation/SAMPLE_comprehensive.vcf.gz | grep "CSQ=" | head -5
```

**Solution 2 - Fix dbNSFP Plugin (Optional):**
```bash
# Check dbNSFP files
ls -la databases/dbnsfp/

# Update plugin path in VEP annotation script
# Edit COMPONENTS/ANNOTATION/vep_clinical_annotation.sh
# Ensure correct path to dbNSFP files
```

**Solution 3 - Use Alternative Score Sources:**
```bash
# The pipeline gets scores from multiple sources:
# - REVEL from dbNSFP (if available)
# - CADD from local database
# - AlphaMissense from dedicated database
# Even with plugin failures, scores may still be available
```

### **Issue 2: Low Score Extraction**

**Symptoms:**
- Very few REVEL scores (expected: >50 for whole genome)
- AlphaMissense scores missing
- All pathogenicity scores showing 0.0

**Diagnosis:**
```bash
# Check VEP CSQ header
bcftools view -h vep_annotation/SAMPLE_comprehensive.vcf.gz | grep "ID=CSQ"

# Count variants with scores
zcat vep_annotation/SAMPLE_comprehensive.vcf.gz | grep -v "^#" | \
    grep -o "REVEL_score=[^;,|]*" | grep -v "REVEL_score=$" | wc -l
```

**Solution 1 - Check VEP Version:**
```bash
# Ensure VEP v114+
vep --help | head -1

# Update if needed
conda update ensembl-vep
```

**Solution 2 - Verify Database Integration:**
```bash
# Check if databases are properly linked
ls -la databases/dbnsfp/dbNSFP4.9a_variant.chr1.gz
ls -la databases/cadd/whole_genome_SNVs*.tsv.gz

# Test VEP with simple variant
echo -e "1\t43045751\t.\tC\tT\t.\t.\t." | \
    vep --cache --offline --format vcf --everything
```

**Solution 3 - Manual Score Addition:**
```bash
# If VEP plugins fail, scores can be added post-processing
# The enhanced gene analyzer handles multi-transcript parsing
# Check if scores are being extracted properly:
grep -A 10 -B 5 "enhanced.*parser" clinical_analysis/*_ENHANCED_ANALYSIS.html
```

### **Issue 3: VEP Cache Issues**

**Error Messages:**
- `Cache not found`
- `Species/assembly not found`
- `Database connection failed`

**Solution:**
```bash
# Check cache location
ls -la databases/vep_cache/homo_sapiens/

# Reinstall cache if corrupted
cd databases/vep_cache
rm -rf homo_sapiens
vep_install -a cf -s homo_sapiens -y GRCh38 -c $(pwd)

# Update cache path in scripts if needed
grep -r "vep_cache" COMPONENTS/ANNOTATION/
```

---

## 🚀 Performance and Resource Issues

### **Issue 1: Slow Processing Speed**

**Expected vs. Actual Times:**
- Whole genome: Should complete in 2-3 hours
- If taking >6 hours, optimization needed

**Diagnosis:**
```bash
# Check bottlenecks
iotop -o  # Disk I/O
htop      # CPU and memory usage
nethogs   # Network usage (for remote storage)

# Check processing stage
tail -f DATA/LOGS/master_pipeline.log | grep -E "(Step|COMPLETED|ERROR)"
```

**Solution 1 - Storage Optimization:**
```bash
# Move to faster storage if possible
# Check current I/O performance
dd if=/dev/zero of=/mnt/d/Genome/test_io bs=1G count=1 oflag=direct
rm /mnt/d/Genome/test_io

# Use local SSD if available
# Ensure databases are on fast storage
```

**Solution 2 - CPU Optimization:**
```bash
# Increase thread count for powerful systems
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_ID 16

# Check CPU utilization during VEP step
watch 'ps aux | grep vep'
```

**Solution 3 - Memory Optimization:**
```bash
# Increase VEP buffer size for more RAM
# Edit COMPONENTS/ANNOTATION/vep_clinical_annotation.sh
# Change: --buffer_size 50000
# To: --buffer_size 100000  # For systems with 128GB+ RAM
```

### **Issue 2: Disk Space Problems**

**Error Messages:**
- `No space left on device`
- `Disk quota exceeded`
- Pipeline fails during processing

**Quick Fix:**
```bash
# Check disk usage
df -h /mnt/d/Genome
du -sh /mnt/d/Genome/* | sort -hr

# Clean up temporary files
rm -rf DATA/PROCESSED/vcf_processed/*_temp*
rm -rf DATA/LOGS/*_old*

# Compress old results
find DATA/RESULTS -name "*.vcf" -mtime +30 -exec gzip {} \;
```

**Long-term Solution:**
```bash
# Monitor disk usage
cat > /mnt/d/Genome/monitor_disk.sh << 'EOF'
#!/bin/bash
USAGE=$(df /mnt/d/Genome | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $USAGE -gt 85 ]; then
    echo "WARNING: Disk usage at ${USAGE}%" | mail -s "Disk Space Alert" admin@example.com
fi
EOF

# Add to crontab for daily monitoring
chmod +x /mnt/d/Genome/monitor_disk.sh
(crontab -l; echo "0 9 * * * /mnt/d/Genome/monitor_disk.sh") | crontab -
```

### **Issue 3: Network Issues (Remote Storage)**

**Symptoms:**
- Slow database access
- Intermittent connection errors
- Timeouts during annotation

**Solution:**
```bash
# Test network connectivity
ping -c 5 ftp.ensembl.org
wget --spider http://ftp.ensembl.org/pub/current_variation/

# Use local database copies
# Ensure all databases are downloaded locally
ls -la databases/*/

# Check for NFS/network mounts
mount | grep "/mnt/d/Genome"
```

---

## 📁 Database and File Issues

### **Issue 1: Corrupted Database Files**

**Symptoms:**
- Segmentation faults during annotation
- Inconsistent results
- `Database error` messages

**Diagnosis:**
```bash
# Check file integrity
md5sum databases/clinvar/clinvar_current.vcf.gz
md5sum databases/gnomad/gnomad.exomes.v4.1.sites.chr1.vcf.bgz

# Test database access
bcftools view databases/clinvar/clinvar_current.vcf.gz | head -10
```

**Solution:**
```bash
# Re-download corrupted files
cd databases/clinvar
mv clinvar_current.vcf.gz clinvar_current.vcf.gz.backup
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_$(date +%Y%m01).vcf.gz
ln -sf clinvar_$(date +%Y%m01).vcf.gz clinvar_current.vcf.gz

# Rebuild indices
tabix -p vcf clinvar_current.vcf.gz
```

### **Issue 2: Assembly Mismatch**

**Error Messages:**
- `Chromosome not found in reference`
- `Assembly version mismatch`
- `Coordinate system error`

**Diagnosis:**
```bash
# Check VCF assembly
bcftools view -h input.vcf.gz | grep "##reference"

# Check reference genome
head -1 databases/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa
```

**Solution:**
```bash
# This pipeline ONLY supports GRCh38
# If input is GRCh37/hg19, you need to:
# 1. Convert to GRCh38 using liftOver
# 2. Use a GRCh37-compatible pipeline

# Quick check for assembly:
bcftools view input.vcf.gz | head -100 | grep -o "^[0-9]*\s" | head -5
# Should show: 1, 2, 3... (not chr1, chr2, chr3...)
```

### **Issue 3: File Format Issues**

**Common Problems:**
- Non-standard VCF headers
- Missing required fields
- Encoding issues

**Solution:**
```bash
# Validate VCF format
bcftools view input.vcf.gz 2>&1 | head -20

# Fix common VCF issues
bcftools norm -f databases/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz \
    input.vcf.gz -o fixed_input.vcf.gz

# Check encoding
file input.vcf.gz
zcat input.vcf.gz | head -1 | od -c  # Check for BOM or strange characters
```

---

## 📊 Results Interpretation Issues

### **Issue 1: No Clinical Variants Found**

**Symptoms:**
- Empty results files
- "0 clinically significant variants"
- No variants in known disease genes

**Diagnosis:**
```bash
# Check total variant count
zcat vep_annotation/SAMPLE_comprehensive.vcf.gz | grep -v "^#" | wc -l

# Check if genes are being matched
grep -c "Gene.*:" clinical_analysis/SAMPLE_ENHANCED_VARIANTS.csv

# Check gene panel
python3 -c "
from COMPONENTS.CLASSIFICATION.gene_panels_database import ALL_COMPREHENSIVE_GENES
print(f'Total genes in panel: {len(ALL_COMPREHENSIVE_GENES)}')
print('Sample genes:', list(ALL_COMPREHENSIVE_GENES)[:10])
"
```

**Possible Causes and Solutions:**

**Cause 1 - Wrong File Type:**
```bash
# Check if this is exome vs. genome data
# Exome should have ~20,000-50,000 variants
# Genome should have 4-6 million variants

variant_count=$(zcat vep_annotation/SAMPLE_comprehensive.vcf.gz | grep -v "^#" | wc -l)
echo "Variant count: $variant_count"

if [ $variant_count -lt 10000 ]; then
    echo "WARNING: Very low variant count - check input file"
fi
```

**Cause 2 - Gene Symbol Mismatch:**
```bash
# Check if gene symbols are being extracted
bcftools query -f '%INFO/CSQ\n' vep_annotation/SAMPLE_comprehensive.vcf.gz | \
    head -10 | cut -d'|' -f4 | head -10

# Should show gene symbols like: BRCA1, TP53, etc.
```

**Cause 3 - Quality Filtering Too Strict:**
```bash
# Check if variants are being filtered out
bcftools view -i 'QUAL>=10' vep_annotation/SAMPLE_comprehensive.vcf.gz | \
    grep -v "^#" | wc -l

# Compare with original count
```

### **Issue 2: Unexpected Results**

**Symptoms:**
- Known pathogenic variant not flagged
- Benign variant classified as pathogenic
- Scores don't match expectations

**Investigation Steps:**
```bash
# Look up specific variant
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%INFO/CSQ\n' \
    vep_annotation/SAMPLE_comprehensive.vcf.gz | \
    grep "43045751"  # Example position

# Check ClinVar for comparison
# Visit: https://www.ncbi.nlm.nih.gov/clinvar/
# Search for variant: chr17:41245466 G>A (example)

# Check if variant is in results
grep -i "brca1\|41245466" clinical_analysis/SAMPLE_ENHANCED_VARIANTS.csv
```

### **Issue 3: Score Discrepancies**

**Problem:** Pipeline scores don't match online calculators

**Explanation:**
```bash
# Different databases and versions can give different scores
# Check which versions the pipeline uses:
grep -A 5 -B 5 "Database.*version" SAMPLE_ANALYSIS_SUMMARY.md

# Common discrepancies:
# 1. REVEL: Different versions (0.6 vs current)
# 2. CADD: v1.6 vs v1.7
# 3. AlphaMissense: Different transcript annotations
# 4. ClinVar: Monthly updates change classifications
```

**Verification:**
```bash
# Extract exact scores for a variant
pos="43045751"
bcftools query -f '%CHROM\t%POS\t%INFO/CSQ\n' \
    vep_annotation/SAMPLE_comprehensive.vcf.gz | \
    grep $pos | cut -f3 | tr ',' '\n' | head -1

# Parse the CSQ field to see individual annotations
```

---

## ❓ Frequently Asked Questions

### **General Usage Questions**

**Q: How long should the pipeline take to run?**
A: 
- **Whole Genome (4-6M variants):** 2-3 hours on recommended hardware
- **Whole Exome (20-50K variants):** 20-40 minutes
- **Targeted Panel (1-5K variants):** 5-15 minutes

Factors affecting speed: CPU cores, RAM, storage type, network speed (for remote databases)

**Q: What assembly should my VCF use?**
A: **GRCh38/hg38 ONLY**. This pipeline does not support GRCh37/hg19. If your data is GRCh37, you need to use liftOver to convert to GRCh38 first.

**Q: Can I run multiple samples simultaneously?**
A: 
- **Single sample mode:** Recommended for most users
- **Multiple samples:** Run sequentially to avoid resource conflicts
- **High-end systems (128GB+ RAM):** Can run 2-3 samples in parallel

**Q: What file formats are supported?**
A: 
- **Input:** VCF 4.2+ (compressed .vcf.gz or uncompressed .vcf)
- **Variant Callers:** DRAGEN (preferred), GATK, Illumina, others
- **Output:** VCF, CSV, HTML, JSON formats

### **Clinical Usage Questions**

**Q: Can I use these results for clinical diagnosis?**
A: **NO**. This pipeline provides research-grade analysis for clinical guidance only. All findings require:
- CLIA laboratory confirmation
- Clinical genetics professional interpretation  
- Correlation with patient phenotype
- Appropriate genetic counseling

**Q: What genes are included in the analysis?**
A: 626+ genes across 22 medical specialties:
- ACMG SF v3.3 genes (84 genes)
- Specialty-specific clinical genes
- Research-relevant genes
- See `gene_panels_database.py` for complete list

**Q: How often should I update the databases?**
A: 
- **ClinVar:** Monthly (essential for clinical accuracy)
- **VEP Cache:** Quarterly
- **gnomAD:** Stable, annual major releases
- **CADD/dbNSFP:** Major releases every 1-2 years

**Q: What do the clinical significance scores mean?**
A: 
- **>150:** Highest priority for clinical validation
- **100-150:** High priority, strong evidence
- **50-99:** Moderate priority, consider phenotype
- **20-49:** Lower priority, research interest
- **<20:** Minimal clinical significance

### **Technical Questions**

**Q: Why do I get VEP plugin warnings?**
A: Plugin warnings are usually **non-critical**. The core VEP annotation continues and provides essential information. Plugin warnings are often due to:
- Authentication requirements (SpliceAI)
- File path issues (dbNSFP)
- Version incompatibilities

The enhanced multi-transcript parser can extract scores even with plugin failures.

**Q: Can I customize the gene panels?**
A: Yes, edit `COMPONENTS/CLASSIFICATION/gene_panels_database.py`:
```python
# Add custom specialty
COMPREHENSIVE_GENE_PANELS['CUSTOM_SPECIALTY'] = {
    'GENE1', 'GENE2', 'GENE3'
}

# Update the comprehensive gene set
ALL_COMPREHENSIVE_GENES.update(COMPREHENSIVE_GENE_PANELS['CUSTOM_SPECIALTY'])
```

**Q: How do I update just one database?**
A: Examples:
```bash
# Update only ClinVar
cd databases/clinvar
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_$(date +%Y%m01).vcf.gz

# Update only VEP cache
vep_install -a cf -s homo_sapiens -y GRCh38 -c databases/vep_cache
```

**Q: What if I have limited disk space?**
A: Minimum requirements:
- Start with essential databases: Reference (1GB), VEP cache (20GB), ClinVar (200MB)
- Add gnomAD gradually: Start with chr1-22 (150GB), add X,Y later
- Skip large optional databases initially: CADD (80GB), dbNSFP (70GB)

**Q: Can I run this on cloud computing?**
A: Yes, considerations:
- Use instance with 64GB+ RAM
- Attach fast SSD storage (1TB+)
- Pre-download databases to avoid egress charges
- Consider spot instances for cost savings
- Ensure GRCh38 assembly compatibility

### **Performance Questions**

**Q: My pipeline is running slowly. How can I optimize it?**
A: Optimization checklist:
1. **Storage:** Use SSD instead of HDD (10x faster)
2. **CPU:** Increase thread count: `bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE 16`
3. **Memory:** Increase VEP buffer size for systems with >64GB RAM
4. **Network:** Ensure databases are local, not remote
5. **System:** Close other applications, check for competing processes

**Q: How much RAM do I really need?**
A: 
- **Minimum:** 32GB (may swap to disk)
- **Recommended:** 64GB (optimal performance)
- **High-throughput:** 128GB+ (parallel processing)
- **Memory usage peaks during VEP annotation (~8-16GB per sample)**

### **Troubleshooting Questions**

**Q: The pipeline fails with "Killed" - what does this mean?**
A: "Killed" usually means the system ran out of memory (OOM killer). Solutions:
1. Add swap space: `sudo fallocate -l 32G /swapfile`
2. Reduce thread count: Use 4 instead of 8 threads
3. Process smaller VCF subsets
4. Increase system RAM

**Q: How do I restart a failed pipeline?**
A: The pipeline is designed to be restartable:
1. **Clean up:** Remove temporary files in `DATA/PROCESSED/vcf_processed/`
2. **Check logs:** Review `DATA/LOGS/master_pipeline.log` for error location  
3. **Restart:** Use same command - pipeline will recreate missing files

**Q: What if I get different results on the same sample?**
A: Check for:
1. **Database updates:** ClinVar changes monthly
2. **Pipeline version:** Different versions may give different results
3. **System differences:** Different VEP/database versions
4. **Input differences:** Ensure exact same VCF file

---

## 📞 Getting Additional Help

### **Log File Analysis**

**Priority order for troubleshooting:**
1. **Main pipeline log:** `DATA/LOGS/master_pipeline.log`
2. **VCF processing log:** `DATA/LOGS/maximum_quality_processing_SAMPLE_ID.log`
3. **Quality control log:** `DATA/LOGS/quality_control_SAMPLE_ID.log`
4. **VEP warnings:** `vep_annotation/SAMPLE_comprehensive_warnings.txt`

### **Community Resources**

**Documentation:**
- Technical Reference: `DOCUMENTATION/TECHNICAL_DOCS/TECHNICAL_REFERENCE.md`
- User Manual: `DOCUMENTATION/USER_GUIDES/USER_MANUAL.md`
- Clinical Guidelines: `DOCUMENTATION/TECHNICAL_DOCS/CLINICAL_GUIDELINES.md`

**External Resources:**
- **VEP Documentation:** https://ensembl.org/info/docs/tools/vep/
- **ACMG Guidelines:** https://www.acmg.net/
- **ClinVar:** https://www.ncbi.nlm.nih.gov/clinvar/
- **gnomAD:** https://gnomad.broadinstitute.org/

### **Creating Effective Bug Reports**

**Include in bug reports:**
1. **System information:** Output of diagnostic script above
2. **Exact command used:** Full command line
3. **Error messages:** Complete error text, not paraphrased
4. **Log files:** Relevant sections from log files
5. **Input file info:** File size, format, source
6. **Expected vs. actual behavior:** What you expected vs. what happened

### **Emergency Troubleshooting**

**If pipeline is completely broken:**
```bash
# 1. Save current state
cp -r DATA/LOGS DATA/LOGS_backup_$(date +%Y%m%d)

# 2. Reset to known good state
cd /mnt/d/Genome
git status  # If using version control
ls -la PIPELINES/VCF_PIPELINE/

# 3. Test with minimal example
echo -e "1\t43045751\t.\tC\tT\t999\tPASS\t.\tGT\t0/1" > test_minimal.vcf
bgzip test_minimal.vcf
bash clinical_genomics_pipeline.sh single test_minimal.vcf.gz TEST_MINIMAL 2

# 4. Check if basic functionality works
ls -la DATA/RESULTS/VCF_ANALYSIS/individuals/TEST_MINIMAL/
```

---

**Troubleshooting Guide Version:** 1.0  
**Pipeline Version:** v4.1  
**Last Updated:** September 2025  

*This troubleshooting guide provides comprehensive solutions for common issues with the Clinical Genomics Pipeline. For issues not covered here, consult the technical documentation or create a detailed bug report following the guidelines above.*