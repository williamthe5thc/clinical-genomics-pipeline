# 🔧 Clinical Genomics Pipeline - Complete Troubleshooting Guide

**Version:** 4.0 - Comprehensive Problem Resolution  
**Purpose:** Systematic diagnosis and resolution of pipeline issues  
**Scope:** All pipeline components from VCF preprocessing through clinical analysis  

---

## 🎯 **TROUBLESHOOTING PHILOSOPHY**

This guide provides systematic approaches to diagnose and resolve issues across all pipeline components. Each problem is categorized by severity and component, with step-by-step diagnostic procedures and proven solutions.

### **Problem Categories**
- 🔴 **Critical**: Pipeline fails to run or produces no output
- 🟡 **Warning**: Pipeline runs but with suboptimal results  
- 🟢 **Optimization**: Pipeline works but could perform better

### **Component Areas**
- **Stage 1**: VCF Preprocessing (professional_vcf_processor.py)
- **Stage 2**: VEP Annotation (comprehensive_vep_v114_fixed.sh)
- **Stage 3**: Clinical Analysis (enhanced_acmg_classifier.py)
- **System**: Dependencies, databases, environment

---

## 🔴 **CRITICAL ISSUES - PIPELINE FAILURES**

### **1. Zero Variants Found in Clinical Analysis**

#### **Symptoms:**
- enhanced_acmg_classifier.py finds 0 clinical variants
- "Total clinical variants identified: 0" in output
- Large input VCF but no clinical results

#### **Diagnostic Procedure:**
```bash
# Step 1: Verify VCF has VEP annotations
bcftools view -h input.vcf.gz | grep CSQ
# Expected: ##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations..."

# Step 2: Test CSQ field parsing
cd /mnt/d/Genome/scripts/filtering
python csq_field_checker.py input.vcf.gz
# Expected: Should show gene symbols and consequences

# Step 3: Check gene panel loading
python test_comprehensive_panels.py
# Expected: "790 genes across 24+ specialties confirmed"

# Step 4: Run with debug mode and minimal threshold
python enhanced_acmg_classifier.py input.vcf.gz SAMPLE_ID --debug --min-score 1
# Should show detailed parsing information
```

#### **Common Causes & Solutions:**

**A. Missing VEP Annotations:**
```bash
# Problem: VCF not annotated with VEP
# Solution: Run VEP annotation first
bash /mnt/d/Genome/scripts/annotation/comprehensive_vep_v114_fixed.sh \
  input.vcf.gz annotated.vcf.gz SAMPLE_ID 8
```

**B. Incorrect CSQ Field Format:**
```bash
# Problem: CSQ field exists but wrong format
# Diagnostic: Check CSQ header
bcftools view -h input.vcf.gz | grep CSQ | head -1

# Solution: Re-annotate with correct VEP version
# Ensure VEP v114.2 is used with proper CSQ format
```

**C. cyvcf2 Library Issues:**
```bash
# Problem: cyvcf2 cannot parse VCF properly
# Test: Simple cyvcf2 reading
python -c "
import cyvcf2
vcf = cyvcf2.VCF('input.vcf.gz')
for i, variant in enumerate(vcf):
    if i >= 5: break
    print(f'Variant {i}: {variant.CHROM}:{variant.POS}')
"

# Solution: Install/reinstall cyvcf2
pip uninstall cyvcf2
pip install cyvcf2
```

**D. Gene Panel Import Issues:**
```bash
# Problem: comprehensive_gene_panels not importing
# Test: Direct import
python -c "
from comprehensive_gene_panels import COMPREHENSIVE_GENE_PANELS
print(f'Loaded {len(COMPREHENSIVE_GENE_PANELS)} panels')
print(f'Total genes: {sum(len(genes) for genes in COMPREHENSIVE_GENE_PANELS.values())}')
"

# Solution: Fix Python path
cd /mnt/d/Genome/scripts/filtering
export PYTHONPATH="/mnt/d/Genome/scripts/filtering:$PYTHONPATH"
```

### **2. VEP Annotation Complete Failure**

#### **Symptoms:**
- VEP fails to start or crashes immediately
- "VEP annotation failed" error message
- No output VCF generated

#### **Diagnostic Procedure:**
```bash
# Step 1: Check VEP installation
which vep
vep --help | head -1
# Expected: ensembl-vep : 114

# Step 2: Check database availability
ls -la /mnt/d/Genome/databases/vep_cache/homo_sapiens/114_GRCh38/
ls -la /mnt/d/Genome/databases/clinvar/clinvar.vcf.gz
ls -la /mnt/d/Genome/databases/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

# Step 3: Test minimal VEP command
vep --input_file test.vcf --output_file test_output.vcf \
    --offline --cache --dir_cache /mnt/d/Genome/databases/vep_cache \
    --assembly GRCh38 --species homo_sapiens
```

#### **Common Causes & Solutions:**

**A. Wrong VEP Version:**
```bash
# Problem: VEP version incompatibility
# Check version:
vep --help | head -1

# Solution: Install correct version
conda uninstall ensembl-vep
conda install -c bioconda ensembl-vep=114.2

# Verify installation:
vep --help | head -1  # Should show version 114
```

**B. Missing VEP Cache:**
```bash
# Problem: VEP cache not found or corrupt
# Diagnostic:
ls -la /mnt/d/Genome/databases/vep_cache/homo_sapiens/114_GRCh38/info.txt

# Solution: Download/reinstall VEP cache
vep_install -a cf -s homo_sapiens -y GRCh38 -c /mnt/d/Genome/databases/vep_cache
```

**C. Database Path Issues:**
```bash
# Problem: VEP cannot find databases
# Check paths in script:
grep "DATABASE_DIR" /mnt/d/Genome/scripts/annotation/comprehensive_vep_v114_fixed.sh

# Verify all database paths exist:
ls -la /mnt/d/Genome/databases/clinvar/
ls -la /mnt/d/Genome/databases/gnomad/
ls -la /mnt/d/Genome/databases/dbnsfp/
```

### **3. VCF Preprocessing Failures**

#### **Symptoms:**
- professional_vcf_processor.py crashes or fails
- Malformed VCF output or no output files
- "VCF processing failed" error messages

#### **Diagnostic Procedure:**
```bash
# Step 1: Check input VCF validity
bcftools view -h input.vcf.gz | head -20
bcftools stats input.vcf.gz | head -20

# Step 2: Check dependencies
which bcftools bgzip tabix
bcftools --version
bgzip --version

# Step 3: Test with diagnostic mode
python /mnt/d/Genome/scripts/professional_vcf_processor.py \
    input.vcf.gz output.vcf SAMPLE_ID --verbose

# Step 4: Check disk space and permissions
df -h /mnt/d/Genome
ls -la /mnt/d/Genome/processed_vcfs/
```

#### **Solutions:**

**A. Corrupted Input VCF:**
```bash
# Problem: Input VCF is corrupted or malformed
# Test VCF integrity:
bgzip -t input.vcf.gz

# If bgzip test fails:
# Try re-downloading or re-generating the VCF
# Or try with uncompressed version:
gunzip -c input.vcf.gz > input.vcf
python professional_vcf_processor.py input.vcf output.vcf SAMPLE_ID
```

**B. Missing Dependencies:**
```bash
# Problem: bcftools, bgzip, or tabix not installed
# Install dependencies:
conda install -c bioconda bcftools=1.17
conda install -c bioconda htslib  # provides bgzip and tabix

# Verify installation:
which bcftools bgzip tabix
```

**C. Insufficient Disk Space:**
```bash
# Problem: Not enough disk space for processing
# Check available space:
df -h /mnt/d/Genome

# Solution: Clean up space or move to larger partition
# Temporary files need 2-3x input file size
```

---

## 🟡 **WARNING ISSUES - SUBOPTIMAL RESULTS**

### **4. Low Variant Discovery in Clinical Analysis**

#### **Symptoms:**
- Clinical analysis finds fewer variants than expected
- Known pathogenic variants not detected
- Significantly fewer variants than similar samples

#### **Diagnostic Procedure:**
```bash
# Step 1: Check input variant count
bcftools stats input.vcf.gz | grep "number of records:"

# Step 2: Test with lower threshold
python enhanced_acmg_classifier.py input.vcf.gz SAMPLE_ID --min-score 10

# Step 3: Check annotation completeness
python csq_field_checker.py input.vcf.gz --debug

# Step 4: Verify gene panel coverage
python test_comprehensive_panels.py
```

#### **Solutions:**

**A. Scoring Threshold Too High:**
```bash
# Problem: --min-score too restrictive
# Test with lower thresholds:
python enhanced_acmg_classifier.py input.vcf.gz SAMPLE_ID --min-score 10  # Very permissive
python enhanced_acmg_classifier.py input.vcf.gz SAMPLE_ID --min-score 20  # Standard
python enhanced_acmg_classifier.py input.vcf.gz SAMPLE_ID --min-score 30  # Conservative

# Choose appropriate threshold based on results
```

**B. Incomplete VEP Annotations:**
```bash
# Problem: VEP annotation missing fields
# Check annotation completeness:
bcftools query -f '%INFO/CSQ\n' input.vcf.gz | head -10

# Solution: Re-run VEP with comprehensive settings:
bash comprehensive_vep_v114_fixed.sh input.vcf.gz re_annotated.vcf.gz SAMPLE_ID 8
```

**C. Population Frequency Filtering Too Strict:**
```bash
# Problem: Common variants filtered out too aggressively
# Check frequency distribution in analysis code
# Modify frequency thresholds if needed for specific populations or conditions
```

### **5. VEP Plugin Warnings**

#### **Symptoms:**
- VEP completes but with plugin warnings
- "WARNING: Plugin X failed" messages
- Missing prediction scores in output

#### **Diagnostic Procedure:**
```bash
# Step 1: Check VEP warning file
cat /mnt/d/Genome/annotation_results/comprehensive/SAMPLE_ID_warnings.txt

# Step 2: Test individual plugins
vep --plugin dbNSFP,/mnt/d/Genome/databases/dbnsfp/dbNSFP4.9a_variant.chr1.gz \
    --input_file test.vcf --output_file test_out.vcf

# Step 3: Check plugin files
ls -la /mnt/d/Genome/databases/dbnsfp/dbNSFP4.9a_variant.chr*.gz
```

#### **Solutions:**

**A. dbNSFP Path Issues:**
```bash
# Problem: dbNSFP files not found or wrong pattern
# Check file naming:
ls -la /mnt/d/Genome/databases/dbnsfp/

# Should see: dbNSFP4.9a_variant.chr1.gz, dbNSFP4.9a_variant.chr2.gz, etc.
# Fix path in VEP script if needed
```

**B. SpliceAI Configuration:**
```bash
# Problem: SpliceAI plugin fails
# Check if SpliceAI is installed:
command -v spliceai

# If not installed:
pip install spliceai

# If authentication issues, use real-time prediction (no database needed)
# This is already configured in comprehensive_vep_v114_fixed.sh
```

**C. CADD Database Issues:**
```bash
# Problem: CADD files not found
# Check CADD files:
ls -la /mnt/d/Genome/databases/cadd/

# Should see SNV and InDel files
# Download if missing or update paths in VEP script
```

### **6. Memory Warnings and Performance Issues**

#### **Symptoms:**
- VEP or analysis scripts run slowly
- Memory warnings in logs
- System becomes unresponsive during processing

#### **Diagnostic Procedure:**
```bash
# Step 1: Monitor memory usage
htop
free -h

# Step 2: Check buffer sizes and threading
grep "buffer_size\|fork" /mnt/d/Genome/scripts/annotation/comprehensive_vep_v114_fixed.sh

# Step 3: Monitor disk I/O
iotop
df -h
```

#### **Solutions:**

**A. Reduce Memory Usage:**
```bash
# Problem: Insufficient RAM for processing
# Solution: Modify VEP settings in comprehensive_vep_v114_fixed.sh

# For systems with <64GB RAM:
--fork 4 --buffer_size 10000

# For systems with 64-128GB RAM:
--fork 8 --buffer_size 25000  # Default

# For systems with >128GB RAM:
--fork 16 --buffer_size 50000
```

**B. Optimize Threading:**
```bash
# Problem: Too many threads for available cores
# Check system cores:
nproc

# Set threads to 0.5-1x number of cores
# Edit VEP script or use parameter:
bash comprehensive_vep_v114_fixed.sh input.vcf.gz output.vcf.gz SAMPLE_ID 4
```

**C. Storage Optimization:**
```bash
# Problem: Slow disk I/O
# Check if databases are on SSD:
df -T /mnt/d/Genome/databases/

# Move temporary files to faster storage:
export TMPDIR=/path/to/fast/storage
```

---

## 🔧 **DEPENDENCY AND ENVIRONMENT ISSUES**

### **9. Python Environment Problems**

#### **Symptoms:**
- ImportError for required modules
- Python version incompatibility
- Package conflicts

#### **Diagnostic Procedure:**
```bash
# Step 1: Check Python version
python --version
# Should be 3.8+

# Step 2: Test critical imports
python -c "
import cyvcf2, pandas, numpy
print('Core dependencies OK')

from comprehensive_gene_panels import COMPREHENSIVE_GENE_PANELS
print(f'Gene panels loaded: {len(COMPREHENSIVE_GENE_PANELS)}')
"

# Step 3: Check package versions
pip list | grep -E "(cyvcf2|pandas|numpy)"
```

#### **Solutions:**

**A. Install Missing Packages:**
```bash
# Install critical dependencies:
pip install cyvcf2 pandas numpy

# For Conda environment:
conda install -c bioconda cyvcf2
conda install pandas numpy
```

**B. Fix Import Path Issues:**
```bash
# Problem: comprehensive_gene_panels not found
# Solution: Set Python path
cd /mnt/d/Genome/scripts/filtering
export PYTHONPATH="/mnt/d/Genome/scripts/filtering:$PYTHONPATH"

# Or run from correct directory:
cd /mnt/d/Genome/scripts/filtering
python enhanced_acmg_classifier.py /path/to/input.vcf.gz SAMPLE_ID
```

**C. Resolve Package Conflicts:**
```bash
# Create clean environment:
conda create -n clinical_genomics python=3.10
conda activate clinical_genomics
conda install -c bioconda ensembl-vep=114.2 cyvcf2 bcftools htslib
pip install pandas numpy
```

### **10. System Resource Issues**

#### **Symptoms:**
- "No space left on device" errors
- "Cannot allocate memory" errors
- System freezing during processing

#### **Diagnostic Procedure:**
```bash
# Check disk space:
df -h /mnt/d/Genome

# Check memory usage:
free -h

# Check system load:
uptime
top

# Check temporary space:
df -h $TMPDIR
df -h /tmp
```

#### **Solutions:**

**A. Disk Space Management:**
```bash
# Clean up old results:
find /mnt/d/Genome/annotation_results/ -name "*.vcf.gz" -mtime +30 -delete
find /mnt/d/Genome/logs/ -name "*.log" -mtime +7 -delete

# Move large files to archive:
mkdir -p /mnt/d/Genome/archive/
mv old_results/* /mnt/d/Genome/archive/

# Check database sizes:
du -sh /mnt/d/Genome/databases/*
```

**B. Memory Management:**
```bash
# For low-memory systems:
# Reduce VEP buffer size:
--buffer_size 10000 --fork 4

# Use swap space if needed:
sudo swapon /swap/file

# Close unnecessary applications:
# Run analysis during off-peak hours
```

**C. Temporary Space Issues:**
```bash
# Set temporary directory to location with more space:
export TMPDIR=/mnt/d/Genome/tmp
mkdir -p /mnt/d/Genome/tmp

# Or use system tmp with cleanup:
# Clean before processing:
sudo rm -rf /tmp/vep_*
sudo rm -rf /tmp/bcftools_*
```

---

## 🚨 **EMERGENCY PROCEDURES**

### **Complete Pipeline Reset**

If the pipeline is completely non-functional:

```bash
# 1. Stop all running processes
pkill -f vep
pkill -f python.*enhanced_acmg
pkill -f bcftools

# 2. Check system resources
df -h
free -h
uptime

# 3. Validate environment
which vep python bcftools bgzip tabix
vep --help | head -1

# 4. Test minimal components
cd /mnt/d/Genome/scripts/filtering
python test_comprehensive_panels.py

# 5. Test with minimal data
# Create small test VCF and run through pipeline
```

### **Database Integrity Check**

If database issues are suspected:

```bash
# Complete database validation script:
#!/bin/bash
cd /mnt/d/Genome/databases

echo "=== Database Integrity Check ==="

# Check ClinVar
echo "Testing ClinVar..."
bgzip -t clinvar/clinvar.vcf.gz && echo "ClinVar: OK" || echo "ClinVar: FAILED"

# Check gnomAD
echo "Testing gnomAD..."
for chr in 1 2 22; do
    bgzip -t gnomad/gnomad.exomes.v4.1.sites.chr${chr}.vcf.bgz && echo "gnomAD chr${chr}: OK" || echo "gnomAD chr${chr}: FAILED"
done

# Check reference
echo "Testing reference genome..."
bgzip -t reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz && echo "Reference: OK" || echo "Reference: FAILED"

# Check VEP cache
echo "Testing VEP cache..."
[[ -d vep_cache/homo_sapiens/114_GRCh38 ]] && echo "VEP cache: OK" || echo "VEP cache: FAILED"

echo "=== Database check complete ==="
```

---

## 📊 **PERFORMANCE BENCHMARKS**

### **Expected Processing Times**
- **VCF Preprocessing**: 5-10 minutes (any size VCF)
- **VEP Annotation**: 
  - Exome (50K variants): 20-45 minutes
  - Whole genome (5M variants): 2-4 hours
- **Clinical Analysis**: 10-30 minutes (any size)

### **Resource Requirements**
- **Minimum RAM**: 32GB (with optimized settings)
- **Recommended RAM**: 64-128GB
- **Storage**: 1.1TB total (600GB databases + 500GB processing)
- **CPU**: 8-16 cores recommended

### **Quality Benchmarks**
- **Annotation Rate**: >99% variants annotated
- **Gene Discovery**: 15,000-30,000 genes per genome
- **Clinical Variants**: 10,000-60,000 per sample (threshold dependent)
- **Pathogenic Findings**: 10-100 high-priority variants

---

## 📞 **GETTING HELP**

### **Self-Diagnosis Checklist**
Before seeking help, run through this checklist:

1. ✅ **System Resources**: Adequate disk space, memory, CPU
2. ✅ **Dependencies**: VEP v114.2, bcftools, Python packages installed
3. ✅ **Databases**: All databases present and accessible
4. ✅ **Input Files**: VCF files valid and properly formatted
5. ✅ **Permissions**: Read/write access to all directories
6. ✅ **Environment**: Proper PATH and PYTHONPATH settings

### **Diagnostic Commands Summary**
```bash
# Quick system check:
which vep python bcftools bgzip tabix
vep --help | head -1
python -c "import cyvcf2, pandas; print('OK')"
df -h /mnt/d/Genome
free -h

# Quick pipeline test:
cd /mnt/d/Genome/scripts/filtering
python test_comprehensive_panels.py
python csq_field_checker.py /path/to/annotated.vcf.gz
```

### **Log File Locations**
For detailed debugging, check these log files:
- **Master Pipeline**: `/mnt/d/Genome/logs/master_pipeline.log`
- **VCF Processing**: `/mnt/d/Genome/logs/maximum_quality_processing_*.log`
- **VEP Annotation**: `/mnt/d/Genome/logs/annotation_logs/vep_annotation.log`
- **Clinical Analysis**: Console output (redirect to file if needed)

---

## 🎯 **PREVENTION STRATEGIES**

### **Regular Maintenance**
```bash
# Monthly tasks:
bash /mnt/d/Genome/scripts/database_update.sh --clinvar-only
python /mnt/d/Genome/scripts/test_pipeline.py --validation-only

# Quarterly tasks:
bash /mnt/d/Genome/scripts/database_update.sh --all
# Clean old log files and results

# System monitoring:
# Monitor disk space usage
# Check for failed cron jobs
# Validate database integrity
```

### **Best Practices**
1. **Always preprocess VCFs** with professional_vcf_processor.py
2. **Use fixed VEP script** (comprehensive_vep_v114_fixed.sh)
3. **Monitor system resources** during processing
4. **Keep databases current** with monthly updates
5. **Validate outputs** with diagnostic tools
6. **Document processing parameters** for reproducibility

---

*Clinical Genomics Pipeline - Complete Troubleshooting Guide v4.0*  
*Systematic diagnosis and resolution for all pipeline components*  
*When in doubt: Check dependencies, validate databases, test with minimal data*

**🔧 Remember:** Most issues are environment-related. Start with dependency and database validation before diving into complex debugging.