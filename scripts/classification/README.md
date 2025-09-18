# Classification Utilities Directory

**Purpose:** Variant classification utilities and supporting algorithms  
**Status:** Supporting components for ACMG/AMP classification workflow  
**Integration:** Works with filtering module for comprehensive clinical analysis

## Overview

This directory contains supporting utilities and algorithms for variant classification, including helper functions for ACMG/AMP evidence assessment, pathogenicity scoring, and clinical interpretation support.

## Utility Scripts

### Classification Support
- **Pathogenicity scoring algorithms**
  - Multi-tool consensus scoring
  - Population frequency assessment
  - Clinical significance integration

- **Evidence code assignment utilities**
  - Automated ACMG/AMP evidence detection
  - Clinical context integration
  - Literature mining support

- **Quality control functions**
  - Classification validation
  - Consistency checking
  - Audit trail generation

## Key Functions

### ACMG Evidence Assessment
```python
def assess_computational_evidence(variant_data):
    """
    Assess PP3/BP4 evidence based on multiple pathogenicity predictors
    Implements ClinGen guidelines for computational evidence
    """
    # REVEL, AlphaMissense, CADD consensus scoring
    # Calibrated thresholds for clinical use
    # Evidence strength determination
```

### Population Frequency Analysis
```python
def evaluate_frequency_evidence(gnomad_data, inheritance_pattern):
    """
    Evaluate PM2/BA1/BS1 evidence based on population frequencies
    Accounts for inheritance patterns and disease prevalence
    """
    # gnomAD v4.1 population data analysis
    # Inheritance-specific frequency thresholds
    # Multi-population considerations
```

### Clinical Significance Integration
```python
def integrate_clinical_databases(clinvar_data, literature_data):
    """
    Integrate multiple sources of clinical evidence
    Resolve conflicts and assess reliability
    """
    # ClinVar assertion analysis
    # Literature evidence integration
    # Expert panel recommendations
```

## Configuration

### Evidence Thresholds
Classification utilities use calibrated thresholds based on clinical validation studies:

```python
EVIDENCE_THRESHOLDS = {
    'computational': {
        'REVEL': {'PP3': 0.644, 'BP4': 0.290},
        'AlphaMissense': {'PP3': 0.564, 'BP4': 0.340},
        'CADD': {'PP3': 25.3, 'BP4': 22.7}
    },
    'frequency': {
        'dominant': {'BA1': 0.05, 'BS1': 0.01, 'PM2': 0.0001},
        'recessive': {'BA1': 0.05, 'BS1': 0.01, 'PM2': 0.0001}
    }
}
```

### Clinical Context Parameters
- Gene constraint metrics (pLI, LOEUF scores)
- Disease prevalence data
- Penetrance and expressivity factors
- Age-dependent penetrance models

## Integration with Main Pipeline

### Workflow Integration
The classification utilities are called by the main ACMG classifier (`enhanced_acmg_classifier.py`) to:

1. **Evidence Collection**: Gather all available evidence for each variant
2. **Evidence Assessment**: Apply clinical guidelines to raw data
3. **Classification Logic**: Implement ACMG/AMP decision rules
4. **Quality Control**: Validate classifications and flag edge cases

### Data Flow
```
VEP Annotated VCF → Classification Utilities → ACMG Evidence Codes → Final Classification
```

## Quality Assurance

### Validation Functions
- **Cross-reference validation**: Compare against ClinVar assertions
- **Literature validation**: Check against published clinical cases
- **Population validation**: Verify frequency calculations
- **Consensus validation**: Multi-algorithm agreement assessment

### Audit Trail
All classification decisions are logged with:
- Evidence sources and versions
- Threshold parameters used  
- Decision rationale
- Confidence metrics

## Clinical Standards Compliance

### ACMG/AMP 2015 Guidelines
Full implementation of published ACMG/AMP variant interpretation guidelines:
- Evidence code definitions and criteria
- Classification decision rules
- Uncertainty handling procedures
- Reporting recommendations

### ClinGen Enhancements
Integration of ClinGen working group recommendations:
- Gene-specific evidence criteria modifications
- Disease-specific threshold adjustments
- Population-specific considerations
- Clinical actionability assessments

## Performance Optimization

### Efficient Algorithms
- Vectorized operations for large variant sets
- Cached database lookups
- Parallel processing support
- Memory-efficient data structures

### Scalability Features
- Chunked processing for memory management
- Database indexing for rapid lookups
- Configurable threading for CPU utilization
- Progress monitoring and resumption capability

## Development Guidelines

### Adding New Evidence Types
1. Define evidence criteria based on clinical literature
2. Implement validation functions
3. Calibrate thresholds using clinical datasets
4. Document clinical rationale
5. Integration testing with main classifier

### Updating Classification Rules
- Monitor ACMG/AMP guideline updates
- Incorporate ClinGen recommendations
- Validate changes against clinical datasets
- Maintain backward compatibility for comparison studies

## Future Enhancements

### Planned Features
- **Machine learning integration**: AI-assisted evidence weighting
- **Functional assay integration**: MAVE data incorporation
- **Structural variation support**: CNV and SV classification
- **Pharmacogenomics expansion**: Drug response variant classification

### Research Integration
- **Novel predictor evaluation**: Assessment of emerging prediction tools
- **Population-specific models**: Ancestry-specific classification
- **Disease-specific refinements**: Condition-specific evidence criteria
- **Real-world validation**: Clinical outcome correlation studies

## Error Handling

### Robustness Features
- **Missing data handling**: Graceful degradation with incomplete information
- **Database connectivity**: Resilient to temporary database unavailability
- **Version compatibility**: Handles different database schema versions
- **Input validation**: Comprehensive VCF format checking

### Logging and Debugging
Comprehensive logging for troubleshooting:
- Evidence assessment details
- Classification decision pathways
- Performance metrics
- Error conditions and recovery

## Clinical Integration

### Research-Grade Support
Classification utilities provide research-grade support for:
- Clinical correlation studies
- Variant interpretation workflows
- Quality improvement initiatives
- Educational and training applications

### Professional Usage
Designed for use by:
- Clinical geneticists and genetic counselors
- Molecular diagnostic laboratory personnel
- Bioinformatics specialists in clinical settings
- Researchers in clinical genomics

---

**Note**: These utilities support research-grade variant classification. All clinical decisions require validation through appropriate clinical testing and expert consultation.
