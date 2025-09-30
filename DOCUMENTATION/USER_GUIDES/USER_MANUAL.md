# Clinical Genomics Pipeline - User Manual v4.1

**Step-by-Step Guide for Research-Grade Clinical Genomics Analysis**

This comprehensive manual provides detailed instructions for using the Clinical Genomics Pipeline for research-grade clinical variant interpretation across 626+ genes and 22 medical specialties.

---

## 📋 Table of Contents

1. [Quick Start Guide](#quick-start-guide)
2. [Pre-Processing Requirements](#pre-processing-requirements)
3. [Single Sample Analysis](#single-sample-analysis)
4. [Understanding Results](#understanding-results)
5. [Advanced Usage](#advanced-usage)
6. [Quality Control](#quality-control)
7. [Troubleshooting](#troubleshooting)
8. [Clinical Interpretation Guidelines](#clinical-interpretation-guidelines)

---

## 🚀 Quick Start Guide

### **Prerequisites Checklist**
- ✅ System meets requirements (64GB+ RAM, 1.1TB+ disk space)
- ✅ All databases installed and current (see installation guide)
- ✅ VCF file is properly formatted (VCF 4.2+ standard)
- ✅ Assembly is GRCh38 (GRCh37 not supported)

### **Basic Command Structure**
```bash
bash clinical_genomics_pipeline.sh <mode> <inputs> [threads]
```

### **Simplest Example**
```bash
cd /mnt/d/Genome
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_001 8
```

---

## 🔧 Pre-Processing Requirements

### **Input File Requirements**

**Supported VCF Types:**
- ✅ DRAGEN VCF files (automatic fixes applied)
- ✅ GATK VCF files
- ✅ Illumina VCF files
- ✅ Standard VCF 4.2+ format
- ✅ Compressed (.vcf.gz) or uncompressed (.vcf)

**Required Assembly:**
- ✅ **GRCh38 only** (mandatory requirement)
- ❌ GRCh37/hg19 not supported

**VCF Quality Checks:**
```bash
# Verify VCF format
bcftools view input.vcf.gz | head -20

# Check assembly version (must be GRCh38)
bcftools view -h input.vcf.gz | grep "##reference"

# Validate basic structure
bcftools stats input.vcf.gz > input_stats.txt
```

### **File Preparation**

**If using DRAGEN VCF (Recommended):**
```bash
# No preparation needed - automatic fixes applied
# Pipeline will automatically:
# - Fix header typos ("ReatPosRankSum" → "ReadPosRankSum")
# - Remove invalid '$' characters
# - Normalize chromosome names (chr1 → 1)
# - Clean malformed records
```

**If using other VCF sources:**
```bash
# Ensure VCF is sorted and indexed
bcftools sort input.vcf > input_sorted.vcf
bgzip input_sorted.vcf
tabix -p vcf input_sorted.vcf.gz
```

---

## 👤 Single Sample Analysis

### **Step 1: Navigate to Pipeline Directory**
```bash
cd /mnt/d/Genome
```

### **Step 2: Execute Pipeline**

**Basic Single Sample:**
```bash
bash clinical_genomics_pipeline.sh single \
    input_data/raw_vcfs/patient.vcf.gz \
    PATIENT_001 \
    8
```

**Parameter Explanation:**
- `single` - Analysis mode (single sample)
- `input_data/raw_vcfs/patient.vcf.gz` - Path to input VCF file
- `PATIENT_001` - Sample identifier (alphanumeric, no spaces)
- `8` - Number of CPU threads (adjust based on system)

### **Step 3: Monitor Progress**

**Real-time Progress Monitoring:**
```bash
# Monitor main pipeline log
tail -f DATA/LOGS/master_pipeline.log

# Monitor in separate terminal
watch 'ls -la DATA/RESULTS/VCF_ANALYSIS/individuals/PATIENT_001/'
```

**Expected Progress Stages:**
1. **System Check (1-2 minutes):** Dependency and database validation
2. **VCF Preprocessing (5-10 minutes):** DRAGEN fixes and quality control
3. **VEP Annotation (150-180 minutes):** Comprehensive variant annotation
4. **Clinical Analysis (30-60 minutes):** ACMG/AMP classification
5. **Report Generation (5 minutes):** HTML, CSV, and summary reports

### **Step 4: Processing Completion**

**Success Indicators:**
```bash
# Check for completion message
tail DATA/LOGS/master_pipeline.log | grep "COMPLETED SUCCESSFULLY"

# Verify output files exist
ls -la DATA/RESULTS/VCF_ANALYSIS/individuals/PATIENT_001/
```

**Expected Final Message:**
```
============================================================================
Clinical Genomics Pipeline v4.1 - COMPLETED SUCCESSFULLY
============================================================================
🎯 AlphaMissense + REVEL + CADD analysis complete
📁 Results: DATA/RESULTS/VCF_ANALYSIS/individuals/PATIENT_001/
============================================================================
```

---

## 📊 Understanding Results

### **Result File Structure**
```
DATA/RESULTS/VCF_ANALYSIS/individuals/PATIENT_001/
├── SAMPLE_ANALYSIS_SUMMARY.md                    # 📋 START HERE
├── vep_annotation/                               # VEP annotation
│   ├── PATIENT_001_comprehensive.vcf.gz         # Annotated variants
│   ├── PATIENT_001_comprehensive_stats.html     # Annotation statistics
│   └── PATIENT_001_comprehensive_warnings.txt   # VEP warnings
└── clinical_analysis/                           # Clinical interpretation
    ├── PATIENT_001_ENHANCED_VARIANTS.csv        # Detailed variant table
    ├── PATIENT_001_ENHANCED_ANALYSIS.html       # Interactive report
    └── PATIENT_001_enhanced_acmg_results.txt    # ACMG results
```

### **Primary Analysis Files**

#### **1. Sample Analysis Summary** (`SAMPLE_ANALYSIS_SUMMARY.md`)
**Purpose:** Comprehensive overview of analysis and quick-access commands
```bash
# View summary
cat DATA/RESULTS/VCF_ANALYSIS/individuals/PATIENT_001/SAMPLE_ANALYSIS_SUMMARY.md
```

#### **2. Enhanced Variants CSV** (`PATIENT_001_ENHANCED_VARIANTS.csv`)
**Purpose:** Detailed spreadsheet of all clinically relevant variants
**Key Columns:**
- `Gene` - Gene symbol
- `Condition` - Associated medical condition
- `Evidence_Tier` - Clinical evidence level (TIER_1_CLINICAL → TIER_7_MINIMAL)
- `Actionability` - Clinical actionability (IMMEDIATELY_ACTIONABLE → RESEARCH_INTEREST)
- `Combined_Score` - Overall clinical significance score
- `REVEL_Score` - Pathogenicity prediction (>0.5 pathogenic)
- `AlphaMissense_Score` - Structure-based pathogenicity (>0.564 pathogenic)
- `CADD_Score` - Deleteriousness score (>25 likely deleterious)
- `ClinVar_Significance` - Known clinical significance

```bash
# View top variants
head -20 clinical_analysis/PATIENT_001_ENHANCED_VARIANTS.csv

# Filter high-priority variants
awk -F',' 'NR==1 || $9>100' clinical_analysis/PATIENT_001_ENHANCED_VARIANTS.csv
```

#### **3. Interactive HTML Report** (`PATIENT_001_ENHANCED_ANALYSIS.html`)
**Purpose:** Professional clinical report with interactive features
```bash
# Open in browser
firefox clinical_analysis/PATIENT_001_ENHANCED_ANALYSIS.html
```

### **Annotation Files**

#### **4. Annotated VCF** (`PATIENT_001_comprehensive.vcf.gz`)
**Purpose:** Complete variant annotations for further analysis
```bash
# Query specific genes
bcftools view vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    grep -E "(NIPBL|BRCA1|TTN)" | head -10

# Count variants by consequence
bcftools view vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    grep -v "^#" | cut -f8 | grep -o "missense_variant\|stop_gained\|frameshift" | \
    sort | uniq -c
```

#### **5. VEP Statistics** (`PATIENT_001_comprehensive_stats.html`)
**Purpose:** Annotation quality metrics and variant consequence summary
```bash
# Open VEP statistics
firefox vep_annotation/PATIENT_001_comprehensive_stats.html
```

---

## 🔍 Advanced Usage

### **Processing Multiple Samples**

**Sequential Processing:**
```bash
# Process multiple samples one by one
for vcf in input_data/raw_vcfs/*.vcf.gz; do
    sample_id=$(basename "$vcf" .vcf.gz)
    bash clinical_genomics_pipeline.sh single "$vcf" "$sample_id" 8
done
```

**Batch Processing Mode:**
```bash
# Process all VCFs in directory
bash clinical_genomics_pipeline.sh batch input_data/raw_vcfs/ 8
```

### **Optimizing Performance**

**High-Memory Systems (128GB+ RAM):**
```bash
# Increase parallel processing
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_001 16
```

**Lower-Memory Systems (32-64GB RAM):**
```bash
# Reduce parallel processing
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_001 4
```

**Storage Optimization:**
```bash
# Clean up intermediate files after successful run
rm -rf DATA/PROCESSED/vcf_processed/SAMPLE_001_*
```

### **Specialty-Focused Analysis**

**Query Specific Medical Specialties:**
```bash
# Find CDLS-related variants
grep -i "cornelia\|cdls" clinical_analysis/PATIENT_001_ENHANCED_VARIANTS.csv

# Find cardiac variants
grep -i "cardiac\|cardio\|heart" clinical_analysis/PATIENT_001_ENHANCED_VARIANTS.csv

# Find high-actionability variants
awk -F',' '$6 ~ /IMMEDIATELY_ACTIONABLE|SCREENING_ACTIONABLE/' \
    clinical_analysis/PATIENT_001_ENHANCED_VARIANTS.csv
```

### **Custom Variant Queries**

**High-Impact Variants:**
```bash
# Find pathogenic/likely pathogenic variants
bcftools view vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    grep -i "pathogenic" | grep -v "benign" | cut -f1,2,4,5,8
```

**Population Frequency Filtering:**
```bash
# Find rare variants (AF < 0.1%)
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%INFO/gnomADe_AF\n' \
    vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    awk '$5 < 0.001 || $5 == "."'
```

---

## 🔬 Quality Control

### **Pipeline Success Validation**

**1. Check Processing Logs:**
```bash
# Verify no critical errors
grep -i "error\|failed\|critical" DATA/LOGS/master_pipeline.log

# Confirm successful completion
tail -5 DATA/LOGS/master_pipeline.log
```

**2. Validate Output Files:**
```bash
# Check all expected files exist
ls -la DATA/RESULTS/VCF_ANALYSIS/individuals/PATIENT_001/

# Verify VCF file integrity
bcftools view -h vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    grep "##VEP"

# Check variant count consistency
zcat vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    grep -v "^#" | wc -l
```

**3. Review Score Extraction:**
```bash
# Verify enhanced multi-transcript parsing
awk -F',' 'NR>1 {if($14>0) revel++; if($15>0) alpha++; if($16>0) cadd++} 
    END {print "REVEL:", revel, "AlphaMissense:", alpha, "CADD:", cadd}' \
    clinical_analysis/PATIENT_001_ENHANCED_VARIANTS.csv
```

### **Quality Metrics Interpretation**

**Expected Results for Whole Genome:**
- **Total Variants:** 4-6 million
- **Clinically Relevant Variants:** 50,000-150,000
- **High-Priority Variants:** 100-1,000
- **REVEL Scores:** >50 variants with scores >0.5
- **CADD Scores:** >10,000 variants with scores >20

**Quality Red Flags:**
- ❌ No REVEL/AlphaMissense scores extracted
- ❌ Extremely low variant counts (<100 clinical variants)
- ❌ All variants showing gnomAD frequency = 1.0
- ❌ No ClinVar annotations found

---

## 🛠️ Troubleshooting

### **Common Issues and Solutions**

#### **Issue 1: Pipeline Fails During VCF Preprocessing**
**Symptoms:** Error in first 10 minutes, logs show VCF parsing errors
```bash
# Check VCF format
bcftools view input.vcf.gz | head -10

# Solution: Verify VCF is properly formatted
bcftools sort input.vcf > temp_sorted.vcf
bgzip temp_sorted.vcf
tabix -p vcf temp_sorted.vcf.gz
```

#### **Issue 2: VEP Annotation Warnings (Non-Critical)**
**Symptoms:** Plugin warnings in logs, but annotation continues
```bash
# Common warnings (SAFE TO IGNORE):
# - dbNSFP plugin warnings
# - SpliceAI authentication errors
# - Missing plugins for some scores

# Solution: Continue - core annotation still works
# Check annotation stats to verify success
```

#### **Issue 3: Low Score Extraction**
**Symptoms:** Very few REVEL/AlphaMissense scores in results
```bash
# Check VEP CSQ format
bcftools view -h vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    grep "##INFO=<ID=CSQ"

# Verify field positions
zcat vep_annotation/PATIENT_001_comprehensive.vcf.gz | \
    grep "^#" | tail -1 | grep -o "CSQ=[^,]*"
```

#### **Issue 4: Memory Issues**
**Symptoms:** Pipeline killed or system freezes
```bash
# Reduce resource usage
bash clinical_genomics_pipeline.sh single input.vcf.gz SAMPLE_001 4

# Monitor memory usage
watch 'free -h && ps aux | grep -E "(vep|python)" | head -5'
```

#### **Issue 5: Disk Space Issues**
**Symptoms:** Pipeline fails with "No space left on device"
```bash
# Check disk usage
df -h /mnt/d/Genome

# Clean up previous runs
rm -rf DATA/PROCESSED/vcf_processed/*_temp*
rm -rf DATA/LOGS/*_old*
```

### **Log File Analysis**

**Main Pipeline Log:**
```bash
# View recent entries
tail -50 DATA/LOGS/master_pipeline.log

# Search for errors
grep -A 5 -B 5 -i "error\|failed" DATA/LOGS/master_pipeline.log
```

**VCF Processing Log:**
```bash
# Check DRAGEN fixes applied
grep -i "dragen\|fix" DATA/LOGS/maximum_quality_processing_PATIENT_001.log
```

**Quality Control Log:**
```bash
# Review QC metrics
cat DATA/LOGS/quality_control_PATIENT_001.log
```

---

## 📋 Clinical Interpretation Guidelines

### **⚠️ Critical Clinical Disclaimers**

**IMPORTANT:** This pipeline provides research-grade computational analysis for clinical guidance only.

**Before Clinical Application:**
1. **All findings require CLIA laboratory confirmation** before medical decisions
2. **Consult clinical genetics professionals** for interpretation
3. **Use results to guide clinical testing strategy**, not for diagnosis
4. **Computational predictions have inherent false positive/negative rates**

### **Clinical Significance Scoring**

**Combined Score Interpretation:**
- **>150:** Highest priority for clinical validation
- **100-150:** High priority, strong clinical evidence
- **50-99:** Moderate priority, consider patient phenotype
- **20-49:** Lower priority, research interest
- **<20:** Minimal clinical significance

**Evidence Tier Hierarchy:**
1. **TIER_1_CLINICAL:** ACMG Secondary Findings v3.3 genes
2. **TIER_2_EXPERT:** ClinGen Expert Panel genes
3. **TIER_3_CLINICAL_LAB:** Clinical laboratory panel genes
4. **TIER_4_ESTABLISHED:** OMIM established associations
5. **TIER_5_EMERGING:** ClinVar pathogenic variants
6. **TIER_6_RESEARCH:** Specialty database genes
7. **TIER_7_MINIMAL:** Research literature only

### **Actionability Categories**

**IMMEDIATELY_ACTIONABLE:**
- Medical interventions available
- Screening protocols established
- Examples: BRCA1/2, cardiac genes, pharmacogenomics

**SCREENING_ACTIONABLE:**
- Surveillance recommendations available
- Preventive measures possible
- Examples: Cancer predisposition genes

**FAMILY_ACTIONABLE:**
- Family screening indicated
- Reproductive counseling relevant
- Examples: Autosomal recessive carriers

**COUNSELING_INDICATED:**
- Genetic counseling recommended
- Phenotype correlation needed
- Examples: Neurodevelopmental genes

### **Pathogenicity Score Thresholds**

**REVEL Score (Range: 0-1):**
- ≥0.75: Likely pathogenic
- 0.5-0.74: Uncertain significance (lean pathogenic)
- 0.25-0.49: Uncertain significance (lean benign)
- <0.25: Likely benign

**AlphaMissense Score (Range: 0-1):**
- ≥0.564: Likely pathogenic
- 0.34-0.563: Uncertain significance
- <0.34: Likely benign

**CADD Score (Phred-scaled):**
- ≥30: Top 0.1% most deleterious
- ≥25: Top 1% most deleterious
- ≥20: Top 10% most deleterious
- <15: Lower impact predicted

### **Clinical Workflow Integration**

**Step 1: Priority Triage**
```bash
# High-priority variants for immediate review
awk -F',' 'NR==1 || $9>100' clinical_analysis/PATIENT_001_ENHANCED_VARIANTS.csv
```

**Step 2: Phenotype Correlation**
- Review patient phenotype against identified genes
- Focus on specialty-relevant findings
- Consider inheritance patterns

**Step 3: Clinical Validation Planning**
- Prioritize ACMG SF genes for reporting
- Plan confirmatory testing for pathogenic variants
- Consider family screening for inherited conditions

**Step 4: Genetic Counseling**
- Discuss limitations of computational predictions
- Review inheritance patterns and recurrence risks
- Plan family testing strategy

### **Specialty-Specific Guidelines**

**Cornelia de Lange Syndrome (CDLS):**
- Focus on NIPBL, SMC1A, SMC3, RAD21, HDAC8
- Consider phenotype severity correlation
- Family history important for interpretation

**Cardiac Genetics:**
- ACMG SF v3.3 genes require careful evaluation
- Consider family history of sudden death
- Immediate cardiology referral for pathogenic variants

**Cancer Predisposition:**
- Distinguish between high and moderate penetrance genes
- Consider age of onset and family history
- Screening recommendations vary by gene

---

## 📞 Support and Additional Resources

### **Getting Help**

**Documentation Resources:**
- Technical Architecture: `DOCUMENTATION/TECHNICAL_DOCS/TECHNICAL_ARCHITECTURE.md`
- Installation Guide: `DOCUMENTATION/USER_GUIDES/INSTALLATION_GUIDE.md`
- Clinical Guidelines: `DOCUMENTATION/TECHNICAL_DOCS/CLINICAL_GUIDELINES.md`
- Troubleshooting: `DOCUMENTATION/TECHNICAL_DOCS/TROUBLESHOOTING.md`

**Log File Locations:**
- Main Pipeline: `DATA/LOGS/master_pipeline.log`
- VCF Processing: `DATA/LOGS/maximum_quality_processing_SAMPLE_ID.log`
- Quality Control: `DATA/LOGS/quality_control_SAMPLE_ID.log`

**Validation Commands:**
```bash
# System status check
bash clinical_genomics_pipeline.sh --help

# Database verification
ls -la databases/*/
```

### **Best Practices**

**Before Starting:**
1. Verify system meets requirements
2. Check disk space availability
3. Validate input VCF format
4. Review sample ID naming conventions

**During Processing:**
1. Monitor log files for errors
2. Check system resources
3. Avoid interrupting long-running processes
4. Keep terminal sessions active

**After Completion:**
1. Review quality metrics
2. Validate expected output files
3. Archive results appropriately
4. Clean up temporary files

### **Performance Optimization Tips**

**For Faster Processing:**
- Use more CPU threads (if available)
- Ensure adequate RAM availability
- Store data on fast SSD storage
- Process samples sequentially to avoid resource conflicts

**For Resource-Constrained Systems:**
- Reduce thread count
- Process smaller VCF subsets
- Clean up temporary files between runs
- Monitor system resources closely

---

**User Manual Version:** 1.0  
**Pipeline Version:** v4.1  
**Last Updated:** September 2025  

*This manual provides comprehensive guidance for using the Clinical Genomics Pipeline for research-grade clinical variant interpretation. Always consult clinical genetics professionals for medical decision-making based on computational results.*