# Clinical Genomics Pipeline Scripts Directory

**Version:** 4.1-alphamissense-fixed (2025-09-17)  
**Status:** Production Ready - 2024-2025 Gold Standard  
**Last Updated:** September 2025

## Overview

This directory contains the core computational scripts for the clinical genomics pipeline, implementing state-of-the-art variant annotation and clinical interpretation workflows.

## Directory Structure

```
scripts/
├── annotation/          # VEP annotation and pathogenicity prediction
├── classification/      # Variant classification utilities  
├── filtering/           # ACMG/AMP classification and clinical analysis
├── logs/               # Logging and monitoring utilities
└── reporting/          # Clinical report generation
```

## Core Pipeline Scripts

### Primary Workflow Scripts

| Script | Purpose | Status | Performance |
|--------|---------|---------|-------------|
| `professional_vcf_processor.py` | DRAGEN VCF preprocessing | ✅ Production | ~4 min/WGS |
| `vep_master_clinical_v115.sh` | VEP annotation with clinical databases | ✅ Production | ~3 hr/WGS |
| `enhanced_acmg_classifier.py` | Multi-specialty ACMG/AMP classification | ✅ Production | ~1-2 min/WGS |

### Pipeline Integration

Scripts are orchestrated by the master pipeline (`master_pipeline_enhanced_logging.sh`) which provides:
- Comprehensive error handling and validation
- Enhanced logging and audit trails
- Organized results structure
- Performance monitoring

## Key Features Implemented

### 2024-2025 Clinical Genomics Standards
- **AlphaMissense Integration**: Google DeepMind structure-based predictions
- **REVEL Pathogenicity**: ClinGen #1 recommendation (via dbNSFP v4.9a)
- **CADD v1.6/1.7**: Comprehensive genomic deleteriousness
- **Current Databases**: gnomAD v4.1, ClinVar September 2025

### Clinical Analysis Coverage
- **23 Medical Specialties**: Comprehensive clinical coverage
- **915+ Genes**: Curated clinical gene panels
- **ACMG/AMP Classification**: Evidence-based variant interpretation
- **Professional Reporting**: Research-grade clinical guidance

## Script Dependencies

### System Requirements
- **Platform**: WSL Ubuntu 22.04+ / Linux
- **Memory**: 64-128GB RAM for whole genome analysis
- **Storage**: 1.1TB+ (600GB databases + 500GB processing)
- **CPU**: Multi-core (8+ cores recommended)

### Software Dependencies
- VEP v114.2+ (with cache and plugins)
- bcftools v1.21+
- Python 3.12+ with required packages:
  - pandas, cyvcf2, yaml, numpy, scipy
- tabix/bgzip utilities

### Database Dependencies
- Reference genome: GRCh38 primary assembly
- VEP cache v114 (GRCh38)
- gnomAD v4.1 (all chromosomes)
- ClinVar (current monthly release)
- dbNSFP v4.9a (with REVEL, AlphaMissense)
- CADD v1.6/1.7 (SNVs and InDels)

## Usage Examples

### Single Sample Analysis
```bash
# From pipeline root directory
bash master_pipeline_enhanced_logging.sh single \
  input_data/raw_vcfs/sample.vcf.gz \
  SAMPLE_ID \
  8  # threads
```

### Script Testing
```bash
# Test individual components
python3 scripts/professional_vcf_processor.py --help
bash scripts/annotation/vep_master_clinical_v115.sh --help
python3 scripts/filtering/enhanced_acmg_classifier.py --help
```

## Performance Benchmarks

### Whole Genome Analysis (4.7M variants)
- **Step 1 - VCF Preprocessing**: ~4 minutes
- **Step 2 - VEP Annotation**: ~180 minutes  
- **Step 3 - Clinical Analysis**: ~2 minutes
- **Total Pipeline Runtime**: ~185 minutes (3.1 hours)

### Output Metrics
- **Clinical Variants Identified**: ~130,000 across 23 specialties
- **Pathogenic/Likely Pathogenic**: ~300-400 variants typical
- **Comprehensive Coverage**: 915+ genes analyzed

## Quality Control

### Validation Features
- Input VCF format validation and repair
- Comprehensive error checking and logging
- Output file integrity verification
- Performance monitoring and reporting

### Clinical Standards Compliance
- ACMG/AMP evidence code integration
- Population frequency filtering (gnomAD v4.1)
- Clinical significance annotations (ClinVar current)
- Appropriate research disclaimers

## Troubleshooting

### Common Issues
- **Memory limitations**: Adjust `--buffer_size` and `--fork` parameters in VEP
- **Plugin warnings**: Generally non-critical, core annotation still works
- **Database path issues**: Verify all database paths in configuration
- **Permission errors**: Ensure write access to output directories

### Log Locations
- Master pipeline logs: `logs/master_pipeline.log`
- VEP annotation logs: `logs/annotation_logs/`
- Individual script logs: Component-specific locations

## Development Guidelines

### Code Standards
- Comprehensive error handling and validation
- Detailed logging for audit trails
- Modular design for maintenance
- Performance optimization for clinical scale

### Testing Procedures
- Validate with known control samples
- Cross-reference with previous pipeline versions
- Monitor performance metrics
- Verify clinical output accuracy

## Support and Maintenance

### Regular Maintenance Tasks
- Monthly ClinVar database updates
- Quarterly VEP cache updates  
- Annual major database version updates
- Performance monitoring and optimization

### Clinical Validation
- Regular validation with positive/negative controls
- Comparison with established clinical results
- Literature review for gene-disease associations
- Quality assurance monitoring

## Important Clinical Disclaimers

⚠️ **RESEARCH-GRADE ANALYSIS FOR CLINICAL GUIDANCE ONLY**

- All findings require clinical validation before medical decisions
- Use results to guide clinical testing strategy, not for diagnosis
- Consult clinical genetics professionals for interpretation
- Not a replacement for CLIA-certified clinical laboratory testing

---

*This pipeline provides research-grade analysis suitable for clinical correlation when used by qualified genetics professionals with appropriate validation procedures.*
