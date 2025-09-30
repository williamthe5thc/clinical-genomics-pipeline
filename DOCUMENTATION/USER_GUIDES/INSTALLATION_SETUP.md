# Clinical Genomics Pipeline - Installation & Setup Guide v4.1

**Comprehensive Guide for Installing and Configuring the Clinical Genomics Pipeline System**

This guide provides step-by-step instructions for setting up the Clinical Genomics Pipeline for research-grade clinical variant interpretation across 626+ genes and 22 medical specialties.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Base System Setup](#base-system-setup)
4. [Software Installation](#software-installation)
5. [Database Installation](#database-installation)
6. [Pipeline Configuration](#pipeline-configuration)
7. [Validation Testing](#validation-testing)
8. [Troubleshooting Installation Issues](#troubleshooting-installation-issues)

---

## 💻 System Requirements

### **Hardware Requirements**

**Minimum Requirements:**
- **CPU:** 4+ cores (Intel/AMD x64 architecture)
- **RAM:** 32GB minimum (64GB strongly recommended)
- **Storage:** 1.5TB available space (1.1TB databases + 400GB processing)
- **Network:** 100Mbps for initial database downloads

**Recommended Configuration:**
- **CPU:** 8-16 cores, 2.5GHz+ base frequency
- **RAM:** 128GB+ for optimal performance
- **Storage:** NVMe SSD with 2TB+ capacity
- **Network:** 1Gbps+ for faster setup and updates

**Storage Breakdown:**
```
Total Required: ~1.1TB for databases + 500GB processing space
├── VEP Cache v114: ~20GB
├── gnomAD v4.1: ~184GB (24 chromosome files)
├── ClinVar: ~162MB (monthly updates)
├── CADD v1.6/1.7: ~82GB SNVs + 1.2GB InDels
├── dbNSFP v4.9a: ~73GB
├── Reference Genome: ~761MB
├── Processing Space: ~500GB (temporary files, results)
└── System Overhead: ~50GB
```

### **Software Requirements**

**Operating System:**
- ✅ **Ubuntu 22.04+ LTS** (Recommended)
- ✅ **CentOS 8+ / RHEL 8+**
- ✅ **WSL2 Ubuntu 22.04** (Windows subsystem)
- ❌ Windows native (not supported)
- ❌ macOS (limited support)

**Required Assembly:**
- ✅ **GRCh38/hg38 ONLY** (mandatory requirement)
- ❌ **GRCh37/hg19** (not supported)

---

## ✅ Pre-Installation Checklist

### **Environment Preparation**

**1. System Updates:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl wget git unzip

# CentOS/RHEL
sudo yum update -y
sudo yum groupinstall -y "Development Tools"
sudo yum install -y curl wget git unzip
```

**2. Create Installation Directory:**
```bash
# Create base directory (adjust path as needed)
sudo mkdir -p /mnt/d/Genome
sudo chown $(whoami):$(whoami) /mnt/d/Genome
cd /mnt/d/Genome
```

**3. Check Disk Space:**
```bash
# Verify available space (need 1.5TB+)
df -h /mnt/d/Genome
```

**4. Check Internet Connectivity:**
```bash
# Test download speeds (should be >10MB/s for reasonable install time)
wget --spider --server-response http://ftp.ensembl.org/pub/current_variation/indexed_vep_cache/
```

---

## 🔧 Base System Setup

### **Step 1: Install Conda/Miniconda**

**Download and Install Miniconda:**
```bash
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

# Add to PATH
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
conda --version
```

### **Step 2: Configure Conda Channels**

```bash
# Add bioconda channels in correct order
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

# Verify channel configuration
conda config --show channels
```

### **Step 3: Create Pipeline Environment**

```bash
# Create dedicated environment
conda create -n clinical_genomics_v41 python=3.9 -y
conda activate clinical_genomics_v41

# Verify environment
which python
python --version  # Should show 3.9.x
```

---

## 🛠️ Software Installation

### **Step 1: Install Core Bioinformatics Tools**

```bash
# Activate environment
conda activate clinical_genomics_v41

# Install core tools
conda install -y \
    bcftools=1.15 \
    htslib=1.15 \
    samtools=1.15 \
    bgzip \
    tabix

# Verify installations
bcftools --version
samtools --version
bgzip --version
tabix --version
```

### **Step 2: Install Python Dependencies**

```bash
# Install required Python packages
conda install -y \
    pandas=1.5.0 \
    numpy=1.21.0 \
    pyyaml=6.0 \
    pathlib

# Install cyvcf2 (high-performance VCF parsing)
pip install cyvcf2==0.30.18

# Verify Python packages
python -c "import pandas, numpy, cyvcf2, yaml; print('All packages installed successfully')"
```

### **Step 3: Install VEP (Variant Effect Predictor)**

**Download and Install VEP v114+:**
```bash
cd /mnt/d/Genome
mkdir -p vep_setup

# Download VEP
cd vep_setup
git clone https://github.com/Ensembl/ensembl-vep.git
cd ensembl-vep

# Install VEP
perl INSTALL.pl --AUTO a --SPECIES homo_sapiens --ASSEMBLY GRCh38 \
    --CACHEDIR /mnt/d/Genome/databases/vep_cache

# Test installation
./vep --help
```

**Configure VEP Environment:**
```bash
# Add VEP to PATH
echo 'export PATH="/mnt/d/Genome/vep_setup/ensembl-vep:$PATH"' >> ~/.bashrc
echo 'export PERL5LIB="/mnt/d/Genome/vep_setup/ensembl-vep:$PERL5LIB"' >> ~/.bashrc
source ~/.bashrc

# Verify VEP installation
vep --help | head -10
```

### **Step 4: Download Pipeline Code**

```bash
cd /mnt/d/Genome

# Create directory structure (based on your current system)
mkdir -p PIPELINES/VCF_PIPELINE
mkdir -p COMPONENTS/CLASSIFICATION
mkdir -p COMPONENTS/ANNOTATION
mkdir -p COMPONENTS/REPORTING
mkdir -p DATA/{INPUTS/raw_vcfs,PROCESSED/vcf_processed,RESULTS/VCF_ANALYSIS,LOGS}
mkdir -p databases/{reference,vep_cache,gnomad,clinvar,cadd,dbnsfp}

# Verify directory structure
ls -la
```

**Note:** Based on the system analysis, the pipeline code should already be present. If setting up on a new system, you would copy the files from the existing working system.

---

## 💾 Database Installation

### **Step 1: Reference Genome (GRCh38)**

```bash
cd /mnt/d/Genome/databases/reference

# Download GRCh38 primary assembly
wget http://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

# Create FASTA index
samtools faidx Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

# Verify download (should be ~761MB)
ls -lh Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz*
```

### **Step 2: VEP Cache v114**

```bash
cd /mnt/d/Genome/databases/vep_cache

# Download VEP cache (this may take 30-60 minutes)
vep_install -a cf -s homo_sapiens -y GRCh38 -c /mnt/d/Genome/databases/vep_cache

# Alternative manual download if vep_install fails
wget http://ftp.ensembl.org/pub/release-114/variation/indexed_vep_cache/homo_sapiens_vep_114_GRCh38.tar.gz
tar -xzf homo_sapiens_vep_114_GRCh38.tar.gz

# Verify installation (~20GB)
ls -lh /mnt/d/Genome/databases/vep_cache/
```

### **Step 3: gnomAD v4.1 (Population Frequencies)**

```bash
cd /mnt/d/Genome/databases/gnomad

# Create download script for all chromosomes
cat > download_gnomad.sh << 'EOF'
#!/bin/bash
BASE_URL="https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1/exomes"

for chr in {1..22} X Y; do
    echo "Downloading chromosome $chr..."
    wget -c "${BASE_URL}/gnomad.exomes.v4.1.sites.chr${chr}.vcf.bgz"
    wget -c "${BASE_URL}/gnomad.exomes.v4.1.sites.chr${chr}.vcf.bgz.tbi"
done
EOF

chmod +x download_gnomad.sh

# Execute download (WARNING: This is ~184GB and will take several hours)
# Consider running in screen/tmux session
./download_gnomad.sh

# Verify downloads
ls -lh *.vcf.bgz | wc -l  # Should show 24 files (chr1-22, X, Y)
```

### **Step 4: ClinVar (Clinical Significance)**

```bash
cd /mnt/d/Genome/databases/clinvar

# Download latest ClinVar
CURRENT_MONTH=$(date +%Y%m01)
wget "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_${CURRENT_MONTH}.vcf.gz"
wget "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_${CURRENT_MONTH}.vcf.gz.tbi"

# Create current symlinks
ln -sf "clinvar_${CURRENT_MONTH}.vcf.gz" clinvar_current.vcf.gz
ln -sf "clinvar_${CURRENT_MONTH}.vcf.gz.tbi" clinvar_current.vcf.gz.tbi

# Verify download (~162MB)
ls -lh clinvar_current.vcf.gz*
```

### **Step 5: CADD Scores (Pathogenicity Prediction)**

```bash
cd /mnt/d/Genome/databases/cadd

# Download CADD v1.7 scores (WARNING: Large files - 82GB total)
echo "Downloading CADD SNV scores (this will take several hours)..."
wget -c https://krishna.gs.washington.edu/download/CADD/v1.7/GRCh38/whole_genome_SNVs.tsv.gz
wget -c https://krishna.gs.washington.edu/download/CADD/v1.7/GRCh38/whole_genome_SNVs.tsv.gz.tbi

echo "Downloading CADD InDel scores..."
wget -c https://krishna.gs.washington.edu/download/CADD/v1.7/GRCh38/gnomad.genomes.InDels.tsv.gz
wget -c https://krishna.gs.washington.edu/download/CADD/v1.7/GRCh38/gnomad.genomes.InDels.tsv.gz.tbi

# Verify downloads
ls -lh *.tsv.gz*
```

### **Step 6: dbNSFP (Multiple Prediction Algorithms)**

```bash
cd /mnt/d/Genome/databases/dbnsfp

# Download dbNSFP v4.9a (73GB total)
echo "Downloading dbNSFP database (this will take several hours)..."

# Option 1: Download full database
wget -c https://sites.google.com/site/jpopgen/dbNSFP/dbNSFP4.9a.zip

# Extract and organize
unzip dbNSFP4.9a.zip
mv dbNSFP4.9a_variant.chr* .

# Option 2: Download individual chromosome files (recommended)
for chr in {1..22} X Y M; do
    echo "Downloading chromosome $chr..."
    wget -c "https://sites.google.com/site/jpopgen/dbNSFP/dbNSFP4.9a_variant.chr${chr}.gz"
done

# Verify downloads
ls -lh dbNSFP4.9a_variant.chr*.gz | wc -l  # Should show 25 files
```

### **Step 7: AlphaMissense (Structure-based Predictions)**

```bash
mkdir -p /mnt/d/Genome/databases/alphamissense
cd /mnt/d/Genome/databases/alphamissense

# Download AlphaMissense predictions for human
wget -c https://storage.googleapis.com/dm_alphamissense/AlphaMissense_hg38.tsv.gz

# Verify download (~614MB)
ls -lh AlphaMissense_hg38.tsv.gz
```

---

## ⚙️ Pipeline Configuration

### **Step 1: Configure Environment**

```bash
# Create environment activation script
cat > /mnt/d/Genome/activate_pipeline.sh << 'EOF'
#!/bin/bash
# Clinical Genomics Pipeline Environment Activation

# Activate conda environment
conda activate clinical_genomics_v41

# Set environment variables
export GENOME_BASE="/mnt/d/Genome"
export VEP_CACHE_DIR="$GENOME_BASE/databases/vep_cache"
export VEP_PLUGINS_DIR="$GENOME_BASE/vep_setup/plugins"
export REFERENCE_GENOME="$GENOME_BASE/databases/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"

# Add tools to PATH
export PATH="$GENOME_BASE/vep_setup/ensembl-vep:$PATH"
export PERL5LIB="$GENOME_BASE/vep_setup/ensembl-vep:$PERL5LIB"

echo "Clinical Genomics Pipeline environment activated"
echo "Base directory: $GENOME_BASE"
echo "VEP cache: $VEP_CACHE_DIR"
EOF

chmod +x /mnt/d/Genome/activate_pipeline.sh

# Test activation
source /mnt/d/Genome/activate_pipeline.sh
```

### **Step 2: Update Configuration Files**

```bash
# Update pipeline configuration
cd /mnt/d/Genome/PIPELINES/VCF_PIPELINE

# Verify configuration file exists and update paths if needed
cat VCF_pipeline_config.yaml | head -20

# The configuration should already be set correctly for /mnt/d/Genome
# If needed, update base directory paths in the configuration
```

### **Step 3: Verify File Permissions**

```bash
# Set appropriate permissions
cd /mnt/d/Genome

# Make scripts executable
chmod +x PIPELINES/VCF_PIPELINE/*.sh
chmod +x COMPONENTS/ANNOTATION/*.sh
chmod +x PIPELINES/VCF_PIPELINE/*.py
chmod +x COMPONENTS/CLASSIFICATION/*.py

# Set database permissions (read-only)
chmod -R 644 databases/
chmod +x databases/*/  # Directory execute permissions

# Verify permissions
ls -la PIPELINES/VCF_PIPELINE/
```

---

## ✅ Validation Testing

### **Step 1: System Validation**

```bash
# Activate environment
source /mnt/d/Genome/activate_pipeline.sh

# Check all dependencies
echo "=== Dependency Check ==="
conda --version
python --version
bcftools --version | head -1
vep --help | head -1
which tabix
which bgzip

echo "=== Database Check ==="
ls -la databases/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz*
ls -la databases/vep_cache/homo_sapiens/
ls -la databases/gnomad/*.vcf.bgz | wc -l
ls -la databases/clinvar/clinvar_current.vcf.gz*
ls -la databases/cadd/*.tsv.gz*
ls -la databases/dbnsfp/dbNSFP4.9a_variant.chr1.gz
```

### **Step 2: Pipeline Component Testing**

```bash
cd /mnt/d/Genome

# Test main pipeline help
bash PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh --help

# Test VCF processor help
python PIPELINES/VCF_PIPELINE/vcf_quality_processor.py --help

# Test gene analyzer
cd COMPONENTS/CLASSIFICATION
python comprehensive_gene_analyzer.py --help
```

### **Step 3: Create Test Data**

```bash
# Create a small test VCF for validation
mkdir -p /mnt/d/Genome/DATA/test_data
cd /mnt/d/Genome/DATA/test_data

# Create minimal test VCF
cat > test_sample.vcf << 'EOF'
##fileformat=VCFv4.2
##reference=file:///path/to/GRCh38.fa
##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE1
1	43045751	.	C	T	999	PASS	AC=1;AF=0.5	GT:DP	0/1:30
17	41245466	.	G	A	999	PASS	AC=1;AF=0.5	GT:DP	0/1:25
EOF

# Compress and index
bgzip test_sample.vcf
tabix -p vcf test_sample.vcf.gz

# Verify test file
bcftools view test_sample.vcf.gz
```

### **Step 4: Run Test Analysis**

```bash
cd /mnt/d/Genome

# Run pipeline on test sample
echo "Running test analysis..."
bash PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh single \
    DATA/test_data/test_sample.vcf.gz \
    TEST_INSTALL \
    4

# Check if test completed successfully
if [ -d "DATA/RESULTS/VCF_ANALYSIS/individuals/TEST_INSTALL" ]; then
    echo "✅ Test analysis completed successfully!"
    ls -la DATA/RESULTS/VCF_ANALYSIS/individuals/TEST_INSTALL/
else
    echo "❌ Test analysis failed - check logs"
    tail -20 DATA/LOGS/master_pipeline.log
fi
```

### **Step 5: Validation Checklist**

```bash
# Create validation report
cat > /mnt/d/Genome/INSTALLATION_VALIDATION.md << 'EOF'
# Clinical Genomics Pipeline Installation Validation

## System Requirements ✅
- [ ] CPU: 4+ cores available
- [ ] RAM: 32GB+ available  
- [ ] Storage: 1.5TB+ available
- [ ] OS: Ubuntu 22.04+ or compatible

## Software Installation ✅
- [ ] Conda/Miniconda installed
- [ ] clinical_genomics_v41 environment created
- [ ] bcftools/htslib installed
- [ ] VEP v114+ installed and configured
- [ ] Python dependencies installed

## Database Installation ✅
- [ ] Reference genome (GRCh38) downloaded
- [ ] VEP cache v114 installed
- [ ] gnomAD v4.1 downloaded (24 chromosome files)
- [ ] ClinVar current release downloaded
- [ ] CADD v1.7 scores downloaded
- [ ] dbNSFP v4.9a downloaded
- [ ] AlphaMissense downloaded

## Pipeline Configuration ✅
- [ ] Environment activation script created
- [ ] File permissions set correctly
- [ ] Configuration files updated
- [ ] Directory structure validated

## Functional Testing ✅
- [ ] Pipeline help displayed correctly
- [ ] Test VCF processed successfully
- [ ] Results generated in expected format
- [ ] No critical errors in logs

## Installation Date: $(date)
## Installation Status: READY FOR PRODUCTION
EOF

echo "Installation validation complete!"
cat /mnt/d/Genome/INSTALLATION_VALIDATION.md
```

---

## 🛠️ Troubleshooting Installation Issues

### **Common Installation Problems**

#### **Issue 1: Insufficient Disk Space**
```bash
# Check disk usage
df -h /mnt/d/Genome

# Solutions:
# 1. Free up space on target drive
# 2. Move to larger drive
# 3. Use different partition
# 4. Install databases selectively (start with essential ones)
```

#### **Issue 2: Conda Installation Fails**
```bash
# Alternative installation methods:
# Option 1: Use system package manager
sudo apt install conda  # Ubuntu
sudo yum install conda  # CentOS

# Option 2: Manual installation without conda
sudo apt install python3-pip
pip3 install pandas numpy cyvcf2 pyyaml
```

#### **Issue 3: VEP Installation Problems**
```bash
# Check Perl dependencies
perl -MCPAN -e 'install Archive::Zip'
perl -MCPAN -e 'install DBI'

# Alternative VEP installation
docker pull ensemblorg/ensembl-vep:latest
# Use containerized VEP if local installation fails
```

#### **Issue 4: Database Download Failures**
```bash
# Resume interrupted downloads
wget -c <URL>  # Continue interrupted download

# Use alternative mirrors
# gnomAD: Try Google Cloud Storage direct links
# ClinVar: Use FTP mirrors
# CADD: Use local mirrors if available

# Parallel downloads for speed
wget --parallel=4 <URL>
```

#### **Issue 5: Permission Denied Errors**
```bash
# Fix ownership
sudo chown -R $(whoami):$(whoami) /mnt/d/Genome

# Fix permissions
chmod -R 755 /mnt/d/Genome
chmod +x /mnt/d/Genome/PIPELINES/VCF_PIPELINE/*.sh
```

#### **Issue 6: Memory Issues During Testing**
```bash
# Reduce resource usage for testing
bash clinical_genomics_pipeline.sh single test.vcf.gz TEST 2  # Use 2 threads

# Monitor memory usage
free -h
top -p $(pgrep -f vep)
```

### **Installation Validation Scripts**

**Quick System Check:**
```bash
#!/bin/bash
# quick_validation.sh

echo "=== Clinical Genomics Pipeline Installation Check ==="

# Check disk space
echo "Disk space:"
df -h /mnt/d/Genome | tail -1

# Check key directories
echo "Key directories:"
for dir in databases PIPELINES COMPONENTS DATA; do
    if [ -d "/mnt/d/Genome/$dir" ]; then
        echo "✅ $dir exists"
    else
        echo "❌ $dir missing"
    fi
done

# Check essential databases
echo "Essential databases:"
for db in reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz \
          vep_cache/homo_sapiens \
          clinvar/clinvar_current.vcf.gz; do
    if [ -e "/mnt/d/Genome/databases/$db" ]; then
        echo "✅ $db exists"
    else
        echo "❌ $db missing"
    fi
done

# Check tools
echo "Tools:"
for tool in conda python bcftools vep; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool available"
    else
        echo "❌ $tool missing"
    fi
done
```

### **Performance Optimization Post-Installation**

```bash
# Optimize system for genomics workloads
echo "# Genomics optimizations" >> ~/.bashrc
echo "ulimit -n 65536" >> ~/.bashrc  # Increase file handle limit
echo "export OMP_NUM_THREADS=8" >> ~/.bashrc  # Optimize threading

# Create swap file if needed (for systems with limited RAM)
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

---

## 📋 Post-Installation Setup

### **Step 1: Create User Documentation**

```bash
# Create quick reference
cat > /mnt/d/Genome/QUICK_START.md << 'EOF'
# Clinical Genomics Pipeline - Quick Start

## Activate Environment
source /mnt/d/Genome/activate_pipeline.sh

## Process Single Sample
bash PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh single \
    input.vcf.gz SAMPLE_ID 8

## View Results
cd DATA/RESULTS/VCF_ANALYSIS/individuals/SAMPLE_ID/
cat SAMPLE_ANALYSIS_SUMMARY.md
EOF
```

### **Step 2: Set Up Maintenance Scripts**

```bash
mkdir -p /mnt/d/Genome/maintenance

# Monthly ClinVar update script
cat > /mnt/d/Genome/maintenance/update_clinvar.sh << 'EOF'
#!/bin/bash
cd /mnt/d/Genome/databases/clinvar
CURRENT_DATE=$(date +%Y%m01)
wget "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_${CURRENT_DATE}.vcf.gz"
wget "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_${CURRENT_DATE}.vcf.gz.tbi"
ln -sf "clinvar_${CURRENT_DATE}.vcf.gz" clinvar_current.vcf.gz
ln -sf "clinvar_${CURRENT_DATE}.vcf.gz.tbi" clinvar_current.vcf.gz.tbi
echo "ClinVar updated to ${CURRENT_DATE}"
EOF

chmod +x /mnt/d/Genome/maintenance/update_clinvar.sh
```

### **Step 3: Configure Automatic Backups**

```bash
# Create backup script for results
cat > /mnt/d/Genome/maintenance/backup_results.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/mnt/backup/genome_pipeline"
mkdir -p "$BACKUP_DIR"

# Backup configuration and results (not databases)
tar -czf "$BACKUP_DIR/pipeline_backup_$(date +%Y%m%d).tar.gz" \
    --exclude="databases" \
    --exclude="DATA/PROCESSED" \
    /mnt/d/Genome/

echo "Backup completed: $BACKUP_DIR/pipeline_backup_$(date +%Y%m%d).tar.gz"
EOF

chmod +x /mnt/d/Genome/maintenance/backup_results.sh
```

---

## ✅ Installation Complete

### **Final Verification**

**System Status Check:**
```bash
cd /mnt/d/Genome
source activate_pipeline.sh

echo "=== Installation Complete ==="
echo "Base Directory: $(pwd)"
echo "Environment: $CONDA_DEFAULT_ENV"
echo "VEP Version: $(vep --help | head -1)"
echo "Database Size: $(du -sh databases/)"
echo "System Ready: $(date)"

# Test pipeline availability
bash PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh --help | head -5
```

**Next Steps:**
1. Review the User Manual for detailed usage instructions
2. Test with your first sample VCF file
3. Set up periodic database updates (monthly ClinVar)
4. Configure backup procedures for results
5. Review security and access controls as needed

### **Support and Maintenance**

**Regular Maintenance:**
- **Monthly:** Update ClinVar database
- **Quarterly:** Check for VEP cache updates
- **Semi-annually:** Review disk usage and clean old logs
- **Annually:** Check for major database updates (gnomAD, CADD)

**Getting Help:**
- Check log files in `DATA/LOGS/` for troubleshooting
- Review Technical Reference for advanced configuration
- Consult Troubleshooting Guide for common issues

---

**Installation Guide Version:** 1.0  
**Pipeline Version:** v4.1  
**Target System:** Ubuntu 22.04+ / WSL2  
**Last Updated:** September 2025  

*This installation guide provides comprehensive setup instructions for the Clinical Genomics Pipeline. For ongoing maintenance and updates, consult the maintenance scripts and documentation provided.*