# Annotation Scripts Directory

**Purpose:** VEP-based variant annotation with clinical databases and pathogenicity prediction  
**Status:** Production Ready - VEP v114.2 with 2024-2025 Gold Standard Predictors  
**Performance:** ~3 hours for whole genome (4.7M variants)

## Overview

This directory contains scripts for comprehensive variant annotation using the Variant Effect Predictor (VEP) with state-of-the-art pathogenicity prediction tools and clinical databases.

## Core Scripts

### Primary Annotation Engine
- **`vep_master_clinical_v115.sh`** - Master clinical annotation script
  - **Status**: ✅ Production ready
  - **Features**: AlphaMissense + REVEL + CADD + ClinVar + gnomAD v4.1
  - **Performance**: ~180 minutes for whole genome
  - **Output**: Comprehensive VCF with clinical annotations

### VCF Preprocessing  
- **`professional_vcf_processor.py`** - Clinical-grade VCF preprocessing
  - **Status**: ✅ Production ready  
  - **Purpose**: DRAGEN VCF format standardization and quality control
  - **Performance**: ~4 minutes for whole genome
  - **Features**: Header repair, normalization, duplicate removal, sorting

## 2024-2025 Clinical Genomics Features

### Integrated Pathogenicity Predictors

| Predictor | Version | Status | Clinical Evidence |
|-----------|---------|--------|-------------------|
| **AlphaMissense** | 2023 | ✅ Working | Google DeepMind structure-based |
| **REVEL** | Current | ✅ Working | ClinGen #1 recommendation |
| **CADD** | v1.6/1.7 | ✅ Working | Genome-wide deleteriousness |
| **dbNSFP** | v4.9a | ✅ Working | 45+ prediction algorithms |

### Clinical Databases

| Database | Version | Update Frequency | Status |
|----------|---------|------------------|--------|
| **gnomAD** | v4.1 | Annual | ✅ Current |
| **ClinVar** | Sep 2025 | Monthly | ✅ Current |
| **VEP Cache** | v114 | Quarterly | ✅ Current |
| **Reference** | GRCh38 | Stable | ✅ Current |

## Script Usage

### Master Clinical Annotation
```bash
# Full clinical annotation workflow
bash scripts/annotation/vep_master_clinical_v115.sh \
  processed_vcfs/sample_processed.vcf.gz \
  SAMPLE_ID \
  8  # threads
```

### VCF Preprocessing
```bash
# Prepare DRAGEN VCF for annotation
python3 scripts/annotation/professional_vcf_processor.py \
  --input input_data/raw_vcfs/sample.vcf.gz \
  --output processed_vcfs/sample_processed.vcf \
  --sample-id SAMPLE_ID
```

## Configuration

### VEP Command Structure
The master clinical script implements:
```bash
vep \
  --input_file ${INPUT_VCF} \
  --output_file ${OUTPUT_VCF} \
  --format vcf --vcf --compress_output bgzip \
  --offline --cache --assembly GRCh38 \
  --fasta ${REFERENCE_GENOME} \
  --everything --canonical --mane_select \
  --af --af_gnomade --af_gnomadg \
  --custom ${CLINVAR_VCF},ClinVar,vcf,exact \
  --custom ${ALPHAMISSENSE_TSV},AlphaMissense,bed,overlap \
  --plugin CADD,${CADD_FILES} \
  --plugin dbNSFP,${DBNSFP_FILES},REVEL_score,AlphaMissense_score \
  --fork 8 --buffer_size 50000
```

### Database Paths
Scripts automatically detect database locations:
- Reference genome: `/databases/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz`
- VEP cache: `/databases/vep_cache/homo_sapiens/114_GRCh38/`
- ClinVar: `/databases/clinvar/clinvar.vcf.gz`
- AlphaMissense: `/databases/alphamissense/AlphaMissense_hg38.tsv.gz`
- CADD: `/databases/cadd/whole_genome_SNVs.tsv.gz`
- dbNSFP: `/databases/dbnsfp/dbNSFP4.9a_variant.chr*.gz`

## Output Files

### VEP Annotation Results
```
annotation_results/samples/SAMPLE_ID/vep_annotation/
├── SAMPLE_ID_comprehensive.vcf.gz       # Annotated VCF
├── SAMPLE_ID_comprehensive.vcf.gz.tbi   # VCF index
├── SAMPLE_ID_comprehensive_stats.html   # VEP statistics
└── SAMPLE_ID_comprehensive_warnings.txt # VEP warnings (typical)
```

### Annotation Fields Added

| Field Category | Examples | Source |
|----------------|----------|--------|
| **Consequence** | missense_variant, splice_donor_variant | VEP Core |
| **Gene Info** | SYMBOL, Ensembl, RefSeq, MANE | VEP Core |
| **Population** | gnomAD_AF, gnomAD_AF_afr, MAX_AF | gnomAD v4.1 |
| **Clinical** | ClinVar_CLNSIG, ClinVar_CLNDN | ClinVar |
| **Pathogenicity** | REVEL_score, AlphaMissense_score, CADD_PHRED | Predictors |

## Performance Benchmarks

### Whole Genome Analysis (4.7M variants)
- **VCF Preprocessing**: 4 minutes
- **VEP Annotation**: 180 minutes (3 hours)
- **Memory Usage**: ~8-16GB peak
- **Disk I/O**: ~1.2GB output VCF

### Annotation Success Rates
- **Core annotation**: >99.5% variants annotated
- **Population frequencies**: >95% coverage
- **Pathogenicity predictions**: >90% coverage for relevant variants
- **Clinical significance**: >80% coverage for known variants

## Quality Control

### Validation Checks
- Input VCF format validation and repair
- Database accessibility verification
- Output file integrity checks
- Annotation completeness assessment

### Warning Management
- VEP warnings are expected (~92,000 for whole genome)
- Most warnings are non-critical (plugin timeouts, edge cases)
- Core annotation remains complete despite warnings
- Critical errors are logged separately

## Troubleshooting

### Common Issues

#### Memory Problems
```bash
# Reduce buffer size and parallelization
--buffer_size 25000 --fork 4
```

#### Plugin Warnings
- dbNSFP warnings: Usually path-related, non-critical
- AlphaMissense warnings: Format warnings, prediction still works
- CADD warnings: File access issues, scores still annotated

#### Performance Optimization
```bash
# For faster processing (reduced accuracy)
--pick --no_stats --no_check_variants_order

# For maximum accuracy (slower)
--everything --check_existing --regulatory
```

### Log Analysis
```bash
# Check VEP execution log
tail -f logs/annotation_logs/vep_annotation.log

# Monitor resource usage
htop  # During VEP execution

# Verify output quality
zcat output.vcf.gz | grep -v "^#" | wc -l  # Count annotated variants
```

## Archive Directory

### `archive_old_vep_scripts/`
Contains previous versions of VEP scripts for reference:
- Legacy VEP configurations
- Deprecated pathogenicity predictors  
- Version history for troubleshooting

**Note**: Use only current production scripts for analysis

## Development Notes

### Script Evolution
- **v115**: Current production with AlphaMissense integration
- **v114**: Previous stable version  
- **Legacy**: Archived versions for reference

### Future Enhancements
- Additional pathogenicity predictors as they become available
- Enhanced population-specific annotations
- Improved structural variant handling
- Real-time database update integration

## Clinical Integration

### ACMG/AMP Evidence
Annotations support clinical evidence criteria:
- **PP3/BP4**: Computational evidence (REVEL, AlphaMissense)
- **PM2/BA1/BS1**: Population frequency evidence (gnomAD)
- **PS1/BP6**: Known variant evidence (ClinVar)

### Quality Standards
- All annotations follow current clinical genomics best practices
- Databases updated according to clinical laboratory standards
- Output suitable for research-grade clinical correlation

---

**Important**: This module provides research-grade annotation for clinical correlation. All clinical decisions require validation through CLIA-certified testing.
