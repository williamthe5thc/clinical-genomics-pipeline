# Scripts Directory - VCF Pipeline Core Components

**Version:** 4.1 (Post-Organization Cleanup)  
**Status:** PRODUCTION READY - All components operational  
**Pipeline:** VCF Processing (tested and validated September 2025)  
**Performance:** 3.1 hours for whole genome analysis

## 📁 ORGANIZED DIRECTORY STRUCTURE

```
scripts/
├── 🔧 CORE PROCESSING
│   └── professional_vcf_processor.py    # VCF preprocessing (Step 1)
│
├── 📝 ANNOTATION
│   ├── vep_master_clinical_v115.sh      # VEP annotation (Step 2)
│   └── README.md                        # Annotation documentation
│
├── 🧬 CLASSIFICATION & FILTERING  
│   ├── enhanced_acmg_classifier.py      # ACMG classification (Step 3)
│   ├── multi_specialty_analysis.py     # Analysis wrapper
│   ├── comprehensive_gene_panels.py    # Gene definitions
│   ├── CLINICAL_ANALYSIS_GUIDE.md      # Clinical analysis guide
│   └── README.md                        # Filtering documentation
│
├── 📊 REPORTING
│   ├── clinical_report_generator.py    # Report generation
│   └── README.md                        # Reporting documentation
│
├── 🔍 CLASSIFICATION UTILITIES
│   ├── acmg_classifier.py              # ACMG utilities
│   └── README.md                        # Classification docs
│
├── 📋 LOGS & MONITORING
│   └── README.md                        # Logging documentation
│
├── 📖 DOCUMENTATION
│   ├── README.md                        # This file
│   └── TROUBLESHOOTING.md               # Troubleshooting guide
│
└── 🗂️ ORGANIZED ARCHIVE (moved to /Archive/)
    └── All old VEP versions moved to /Archive/old_vep_scripts/
```

## 🎯 VCF PIPELINE CORE WORKFLOW (All Validated)

### **4-Step VCF Processing Pipeline**

#### **Step 1: Professional VCF Preprocessing** ⚡ ~4 minutes
```bash
# Located: scripts/professional_vcf_processor.py
python3 professional_vcf_processor.py input.vcf.gz output.vcf SAMPLE_ID
```
**Features:**
- ✅ DRAGEN VCF header fixing and standardization
- ✅ Comprehensive quality control and validation
- ✅ Variant normalization and duplicate removal
- ✅ Clinical-grade preprocessing standards

#### **Step 2: VEP Clinical Annotation** 🧬 ~180 minutes
```bash
# Located: scripts/annotation/vep_master_clinical_v115.sh
bash vep_master_clinical_v115.sh input.vcf.gz output.vcf.gz SAMPLE_ID 8
```
**Features:**
- ✅ VEP v114+ with comprehensive clinical databases
- ✅ AlphaMissense structure-based predictions (Google DeepMind)
- ✅ REVEL pathogenicity scoring (ClinGen #1 recommendation)
- ✅ CADD v1.6/1.7 comprehensive scoring
- ✅ gnomAD v4.1 + ClinVar September 2025

#### **Step 3: ACMG/AMP Classification** 📋 ~2 minutes
```bash
# Located: scripts/filtering/enhanced_acmg_classifier.py
python3 enhanced_acmg_classifier.py --vcf-file annotated.vcf.gz --sample-id SAMPLE_ID
```
**Features:**
- ✅ 23 medical specialties, 915+ genes
- ✅ Complete ACMG/AMP evidence code implementation
- ✅ Clinical significance scoring (0-100 scale)
- ✅ Enhanced pathogenicity integration

#### **Step 4: Clinical Reporting** 📊 ~1 minute
**Features:**
- ✅ Organized output structure
- ✅ Interactive HTML reports
- ✅ Professional clinical disclaimers
- ✅ Comprehensive analysis summaries

## 📊 VALIDATED PERFORMANCE METRICS

### **September 2025 Test Results (CS335A Sample)**
- **Input:** 4,737,881 variants (whole genome DRAGEN VCF)
- **Processing Time:** 185 minutes (3.08 hours) total
- **Clinical Variants:** 130,149 across 915 genes
- **Pathogenic/Likely Pathogenic:** 344 variants
- **Success Rate:** 100% completion

### **Component Performance Breakdown**
```
Step 1 - VCF Preprocessing:    ~4 minutes    (235 seconds actual)
Step 2 - VEP Annotation:       ~180 minutes  (validated timing)
Step 3 - ACMG Classification:  ~2 minutes    (79 seconds actual)  
Step 4 - Report Generation:    ~1 minute     (77 seconds actual)
Total Pipeline Runtime:        ~185 minutes  (3.08 hours)
```

## 🔧 CORE SCRIPT DETAILS

### **professional_vcf_processor.py** (Step 1)
**Purpose:** Maximum quality VCF preprocessing  
**Status:** ✅ Production validated  
**Features:**
- DRAGEN VCF header standardization
- Comprehensive quality control (Ti/Tv ratios, depth analysis)
- Variant normalization and duplicate removal
- Clinical-grade error handling

**Usage:**
```bash
python3 scripts/professional_vcf_processor.py \
    input_data/raw_vcfs/sample.vcf.gz \
    processed_vcfs/sample_processed.vcf \
    SAMPLE_ID
```

### **vep_master_clinical_v115.sh** (Step 2)
**Purpose:** Comprehensive clinical annotation  
**Status:** ✅ Production validated  
**Features:**
- VEP v114+ with clinical databases
- AlphaMissense + REVEL + CADD integration
- Enhanced error capture and logging
- Clinical-grade pathogenicity predictions

**Usage:**
```bash
bash scripts/annotation/vep_master_clinical_v115.sh \
    processed_vcfs/sample.vcf.gz \
    annotation_results/sample_annotated.vcf.gz \
    SAMPLE_ID 8
```

### **enhanced_acmg_classifier.py** (Step 3)
**Purpose:** Multi-specialty ACMG/AMP classification  
**Status:** ✅ Production validated  
**Features:**
- 23 medical specialties (915+ genes)
- Complete ACMG/AMP evidence codes
- Clinical significance scoring
- Professional reporting

**Usage:**
```bash
cd scripts/filtering
python3 enhanced_acmg_classifier.py \
    --vcf-file ../../annotation_results/sample.vcf.gz \
    --sample-id SAMPLE_ID \
    --output-dir ../../annotation_results/clinical/
```

## 📁 MEDICAL SPECIALTY COVERAGE (Validated)

### **Gene Panel Integration**
**File:** `scripts/filtering/comprehensive_gene_panels.py`  
**Status:** ✅ All 23 specialties operational

**Coverage Summary:**
```python
COMPREHENSIVE_GENE_PANELS = {
    'CARDIAC': 30+ genes,        # Cardiomyopathy, arrhythmia
    'ONCOLOGY': 40+ genes,       # Hereditary cancer syndromes  
    'NEUROLOGY': 50+ genes,      # Neurodevelopmental disorders
    'CDLS': 7 genes,            # Cornelia de Lange syndrome
    'EPILEPSY': 20+ genes,      # Epileptic encephalopathies
    # ... 18 additional specialties
    # Total: 915+ unique genes
}
```

### **Clinical Analysis Integration**
**File:** `scripts/filtering/multi_specialty_analysis.py`  
**Purpose:** Coordinate multi-specialty analysis and reporting  
**Status:** ✅ Production wrapper for enhanced classifier

## 🗃️ ORGANIZED ARCHIVE SYSTEM

### **Historical Files Moved to /Archive/**
```
/Archive/old_vep_scripts/     # Previous VEP versions (6 files)
├── comprehensive_vep_v114.sh
├── comprehensive_vep_v114_enhanced_alphamissense.sh  
├── comprehensive_vep_v114_enhanced_logging.sh
├── comprehensive_vep_v114_final_fix.sh
├── comprehensive_vep_v114_fixed.sh
└── comprehensive_vep_v114_fixed_alphamissense.sh
```

**Current Production Version:** `scripts/annotation/vep_master_clinical_v115.sh`  
**Status:** Latest consolidated version with all features validated

## 💾 SYSTEM REQUIREMENTS (Validated)

### **Tested Configuration**
- **Platform:** WSL Ubuntu 22.04 on Windows
- **Memory:** 30GB minimum, 64-128GB recommended
- **Storage:** 1TB+ (600GB databases + 400GB processing)
- **CPU:** Multi-core (8 threads optimal for VEP)

### **Software Dependencies (All Confirmed)**
- ✅ **VEP:** v114+ with comprehensive plugins
- ✅ **Python:** 3.12.3 with pandas, cyvcf2, yaml
- ✅ **Tools:** bcftools 1.21, tabix, bgzip
- ✅ **Databases:** All current versions operational

## 🔍 QUALITY CONTROL & VALIDATION

### **Built-in QC Features**
- **Input validation:** VCF format checking and repair
- **Processing validation:** Error detection and reporting
- **Output validation:** File integrity and completeness
- **Performance monitoring:** Timing and resource usage

### **Clinical Standards**
- **ACMG/AMP compliance:** Complete evidence code implementation
- **Database currency:** Monthly ClinVar, quarterly cache updates
- **Population frequencies:** gnomAD v4.1 integration
- **Pathogenicity predictions:** Multi-tool consensus

## 🚨 IMPORTANT CLINICAL DISCLAIMERS

**RESEARCH-GRADE ANALYSIS FOR CLINICAL GUIDANCE ONLY**

All scripts produce research-grade analysis that:
- ⚠️ Requires CLIA laboratory validation before medical decisions
- ⚠️ Should guide clinical testing strategy, not replace diagnosis
- ⚠️ Needs clinical genetics consultation for interpretation
- ⚠️ Is not a substitute for clinical laboratory testing

## 📖 COMPONENT DOCUMENTATION

### **Detailed Documentation Available**
- **`scripts/annotation/README.md`** - VEP annotation details
- **`scripts/filtering/README.md`** - ACMG classification guide  
- **`scripts/reporting/README.md`** - Report generation
- **`scripts/classification/README.md`** - Utility functions
- **`scripts/TROUBLESHOOTING.md`** - Problem solving guide

### **Usage Examples**
Each component directory includes:
- Detailed usage instructions
- Command-line examples
- Performance benchmarks
- Troubleshooting procedures

## 🔧 MAINTENANCE & UPDATES

### **Regular Maintenance**
- **Monthly:** ClinVar database updates
- **Quarterly:** VEP cache updates, literature review
- **Annual:** Major database version updates
- **Ongoing:** Performance monitoring and optimization

### **Quality Assurance**
- **Positive controls:** Known pathogenic variants
- **Negative controls:** Common benign variants  
- **Clinical concordance:** Expert manual review comparison
- **Literature validation:** Gene-disease association updates

---

**Scripts Directory Status:** PRODUCTION READY - All VCF pipeline components operational with comprehensive validation, organized structure, and professional clinical standards.

*Component Status: All Validated September 2025*  
*Pipeline Performance: 3.1 hours for whole genome (4.7M variants)*  
*Clinical Coverage: 915+ genes across 23 medical specialties*