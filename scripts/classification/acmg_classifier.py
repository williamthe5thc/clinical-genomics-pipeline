#!/usr/bin/env python3

"""
ACMG/AMP Automated Classifier v3.1
Systematic evidence assignment and variant classification

Purpose: Implement ACMG/AMP 2015 guidelines with 2025 clinical standards
Features: Automated evidence code assignment, population frequency analysis, 
          computational prediction integration, ClinVar correlation
Output: Standardized variant classifications with evidence documentation

Location: D:\Genome\scripts\classification\acmg_classifier.py
Author: Clinical Genomics Pipeline
"""

import os
import sys
import argparse
import logging
import pandas as pd
import cyvcf2
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = "/mnt/d/Genome"
LOGS_DIR = f"{BASE_DIR}/logs"

# ACMG/AMP Evidence Codes and Weights
EVIDENCE_WEIGHTS = {
    # Pathogenic Evidence
    'PVS1': 8,    # Very Strong Pathogenic
    'PS1': 4,     # Strong Pathogenic
    'PS2': 4,
    'PS3': 4,
    'PS4': 4,
    'PM1': 2,     # Moderate Pathogenic  
    'PM2': 2,
    'PM3': 2,
    'PM4': 2,
    'PM5': 2,
    'PM6': 2,
    'PP1': 1,     # Supporting Pathogenic
    'PP2': 1,
    'PP3': 1,
    'PP4': 1,
    'PP5': 1,
    
    # Benign Evidence
    'BA1': -8,    # Stand-alone Benign
    'BS1': -4,    # Strong Benign
    'BS2': -4,
    'BS3': -4,
    'BS4': -4,
    'BP1': -1,    # Supporting Benign
    'BP2': -1,
    'BP3': -1,
    'BP4': -1,
    'BP5': -1,
    'BP6': -1,
    'BP7': -1
}

# Population frequency thresholds (2025 standards)
FREQUENCY_THRESHOLDS = {
    'ba1_dominant': 0.05,          # 5% - Stand-alone benign for dominant
    'bs1_dominant': 0.01,          # 1% - Strong benign for dominant  
    'pm2_dominant': 0.0001,        # 0.01% - Moderate pathogenic threshold
    'ba1_recessive': 0.02,         # 2% - Recessive carrier frequency
    'bs1_recessive': 0.005,        # 0.5% - Strong benign for recessive
    'x_linked_hemizygous': 0.001   # 0.1% - X-linked hemizygous
}

# High-impact consequences (PVS1 eligible)
PVS1_CONSEQUENCES = [
    'stop_gained', 'frameshift_variant', 'splice_donor_variant', 
    'splice_acceptor_variant', 'start_lost'
]

# Moderate-impact consequences
MODERATE_CONSEQUENCES = [
    'missense_variant', 'splice_region_variant', 'inframe_deletion', 
    'inframe_insertion', 'protein_altering_variant'
]

# Haploinsufficient genes (curated list for PVS1)
HAPLOINSUFFICIENT_GENES = {
    # CdLS genes
    'NIPBL', 'SMC3', 'RAD21', 'BRD4', 'ANKRD11',
    
    # Cardiac genes
    'MYBPC3', 'MYH7', 'TNNI3', 'TNNT2', 'TPM1', 'MYL2', 'MYL3', 'ACTC1',
    'LMNA', 'PLN', 'TTN', 'BAG3', 'FLNC', 'PKP2', 'DSP', 'DSG2', 'DSC2',
    
    # Tumor suppressor genes
    'TP53', 'BRCA1', 'BRCA2', 'APC', 'VHL', 'NF1', 'NF2', 'PTEN', 'RB1',
    'MLH1', 'MSH2', 'MSH6', 'PMS2', 'CDKN2A', 'STK11',
    
    # Neurodevelopmental genes
    'MECP2', 'CDKL5', 'TSC1', 'TSC2', 'SHANK3', 'CHD8', 'FOXP1', 'ARID1B',
    
    # Additional haploinsufficient genes
    'SETD2', 'KMT2D', 'KDM6A', 'CREBBP', 'EP300', 'GATA2', 'RUNX1'
}

# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging(sample_id):
    """Setup logging configuration"""
    log_dir = Path(LOGS_DIR)
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"acmg_classifier_{sample_id}.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# =============================================================================
# EVIDENCE ASSIGNMENT FUNCTIONS
# =============================================================================

def assign_frequency_evidence(variant_data, inheritance='AD'):
    """Assign population frequency evidence (PM2, BA1, BS1)"""
    evidence = []
    
    max_af = variant_data.get('max_af', 0)
    
    if inheritance == 'AD':
        if max_af >= FREQUENCY_THRESHOLDS['ba1_dominant']:
            evidence.append('BA1')
        elif max_af >= FREQUENCY_THRESHOLDS['bs1_dominant']:
            evidence.append('BS1')
        elif max_af <= FREQUENCY_THRESHOLDS['pm2_dominant']:
            evidence.append('PM2')
    
    elif inheritance == 'AR':
        if max_af >= FREQUENCY_THRESHOLDS['ba1_recessive']:
            evidence.append('BA1')
        elif max_af >= FREQUENCY_THRESHOLDS['bs1_recessive']:
            evidence.append('BS1')
        elif max_af <= FREQUENCY_THRESHOLDS['pm2_dominant']:
            evidence.append('PM2')
    
    elif inheritance == 'XL':
        # For X-linked, consider hemizygous males
        if max_af >= FREQUENCY_THRESHOLDS['bs1_dominant']:
            evidence.append('BS1')
        elif max_af <= FREQUENCY_THRESHOLDS['x_linked_hemizygous']:
            evidence.append('PM2')
    
    return evidence

def assign_functional_evidence(variant_data):
    """Assign functional consequence evidence (PVS1, PS1)"""
    evidence = []
    
    consequence = variant_data.get('consequence', '')
    gene = variant_data.get('symbol', '')
    impact = variant_data.get('impact', '')
    
    # PVS1: Null variants in haploinsufficient genes
    if consequence in PVS1_CONSEQUENCES and gene in HAPLOINSUFFICIENT_GENES:
        evidence.append('PVS1')
    elif consequence in PVS1_CONSEQUENCES:
        # Null variant but unknown haploinsufficiency - use PS1
        evidence.append('PS1')
    
    # Special cases for splice variants
    if 'splice' in consequence:
        if consequence in ['splice_donor_variant', 'splice_acceptor_variant']:
            if gene in HAPLOINSUFFICIENT_GENES:
                evidence.append('PVS1')
            else:
                evidence.append('PS1')
        elif consequence == 'splice_region_variant':
            # Splice region variants need additional evidence
            evidence.append('PM1')  # Assume in functional domain
    
    # Missense variants in critical domains
    if consequence == 'missense_variant':
        # Assume missense variants are in functional domains (PM1)
        evidence.append('PM1')
    
    return evidence

def assign_computational_evidence(variant_data):
    """Assign computational prediction evidence (PP3, BP4)"""
    evidence = []
    
    # Extract pathogenicity scores
    scores = variant_data.get('pathogenicity_scores', {})
    
    # Count damaging vs benign predictions
    damaging_count = 0
    benign_count = 0
    total_predictions = 0
    
    # SIFT predictions
    if 'SIFT_pred' in scores:
        total_predictions += 1
        if scores['SIFT_pred'] in ['D', 'damaging']:
            damaging_count += 1
        elif scores['SIFT_pred'] in ['T', 'tolerated']:
            benign_count += 1
    
    # PolyPhen predictions
    if 'Polyphen2_HDIV_pred' in scores:
        total_predictions += 1
        if scores['Polyphen2_HDIV_pred'] in ['D', 'P', 'probably_damaging', 'possibly_damaging']:
            damaging_count += 1
        elif scores['Polyphen2_HDIV_pred'] in ['B', 'benign']:
            benign_count += 1
    
    # CADD scores
    if 'CADD_phred' in scores:
        try:
            cadd_score = float(scores['CADD_phred'])
            total_predictions += 1
            if cadd_score >= 25:
                damaging_count += 1
            elif cadd_score <= 10:
                benign_count += 1
        except (ValueError, TypeError):
            pass
    
    # REVEL scores
    if 'REVEL_score' in scores:
        try:
            revel_score = float(scores['REVEL_score'])
            total_predictions += 1
            if revel_score >= 0.75:
                damaging_count += 1
            elif revel_score <= 0.25:
                benign_count += 1
        except (ValueError, TypeError):
            pass
    
    # AlphaMissense
    if 'AlphaMissense_class' in scores:
        total_predictions += 1
        if scores['AlphaMissense_class'] == 'pathogenic':
            damaging_count += 1
        elif scores['AlphaMissense_class'] == 'benign':
            benign_count += 1
    
    # Evidence assignment based on consensus
    if total_predictions >= 3:
        damaging_ratio = damaging_count / total_predictions
        benign_ratio = benign_count / total_predictions
        
        if damaging_ratio >= 0.75:  # 75% or more predict damaging
            evidence.append('PP3')
        elif benign_ratio >= 0.75:  # 75% or more predict benign
            evidence.append('BP4')
    
    return evidence

def assign_clinvar_evidence(variant_data):
    """Assign ClinVar-based evidence (PS1, PM5, BP6)"""
    evidence = []
    
    clinvar_data = variant_data.get('clinvar', {})
    clinvar_sig = variant_data.get('clinvar_significance', '').lower()
    
    # Check for pathogenic/likely pathogenic in ClinVar
    if 'pathogenic' in clinvar_sig and 'conflicting' not in clinvar_sig:
        if 'likely_pathogenic' in clinvar_sig:
            evidence.append('PS1')  # Strong evidence from ClinVar
        else:
            evidence.append('PS1')  # Pathogenic in ClinVar
    
    # Check for benign/likely benign in ClinVar
    elif 'benign' in clinvar_sig and 'conflicting' not in clinvar_sig:
        evidence.append('BP6')  # Benign in ClinVar
    
    # Check for conflicting interpretations
    elif 'conflicting' in clinvar_sig:
        # Reduce confidence in classification
        pass  # Don't assign evidence for conflicting interpretations
    
    return evidence

def assign_segregation_evidence(variant_data):
    """Assign segregation evidence (PP1, BS4) - placeholder for family data"""
    evidence = []
    
    # This would require family/pedigree data
    # For now, return empty - could be extended with trio analysis
    
    return evidence

def assign_de_novo_evidence(variant_data):
    """Assign de novo evidence (PS2, PM6) - placeholder for trio data"""
    evidence = []
    
    # This would require parental data
    # For now, return empty - could be extended with trio analysis
    
    return evidence

# =============================================================================
# MAIN CLASSIFICATION FUNCTION
# =============================================================================

def classify_variant_acmg(variant_data, inheritance='AD'):
    """Main ACMG/AMP variant classification function"""
    
    all_evidence = []
    evidence_details = {}
    
    # Assign different types of evidence
    freq_evidence = assign_frequency_evidence(variant_data, inheritance)
    all_evidence.extend(freq_evidence)
    evidence_details['frequency'] = freq_evidence
    
    func_evidence = assign_functional_evidence(variant_data)
    all_evidence.extend(func_evidence)
    evidence_details['functional'] = func_evidence
    
    comp_evidence = assign_computational_evidence(variant_data)
    all_evidence.extend(comp_evidence)
    evidence_details['computational'] = comp_evidence
    
    clinvar_evidence = assign_clinvar_evidence(variant_data)
    all_evidence.extend(clinvar_evidence)
    evidence_details['clinvar'] = clinvar_evidence
    
    seg_evidence = assign_segregation_evidence(variant_data)
    all_evidence.extend(seg_evidence)
    evidence_details['segregation'] = seg_evidence
    
    denovo_evidence = assign_de_novo_evidence(variant_data)
    all_evidence.extend(denovo_evidence)
    evidence_details['de_novo'] = denovo_evidence
    
    # Calculate evidence score
    total_score = sum(EVIDENCE_WEIGHTS.get(code, 0) for code in all_evidence)
    
    # Apply ACMG classification rules
    classification = determine_acmg_classification(all_evidence, total_score)
    
    return {
        'classification': classification,
        'evidence_codes': all_evidence,
        'evidence_details': evidence_details,
        'evidence_score': total_score,
        'evidence_summary': format_evidence_summary(all_evidence)
    }

def determine_acmg_classification(evidence_codes, total_score):
    """Determine final ACMG classification based on evidence codes"""
    
    # Count evidence by strength
    pathogenic_counts = {
        'PVS': len([e for e in evidence_codes if e.startswith('PVS')]),
        'PS': len([e for e in evidence_codes if e.startswith('PS')]),
        'PM': len([e for e in evidence_codes if e.startswith('PM')]),
        'PP': len([e for e in evidence_codes if e.startswith('PP')])
    }
    
    benign_counts = {
        'BA': len([e for e in evidence_codes if e.startswith('BA')]),
        'BS': len([e for e in evidence_codes if e.startswith('BS')]),
        'BP': len([e for e in evidence_codes if e.startswith('BP')])
    }
    
    # Apply ACMG classification rules
    
    # Stand-alone classifications
    if benign_counts['BA'] >= 1:
        return 'Benign'
    
    # Pathogenic combinations
    if pathogenic_counts['PVS'] >= 1:
        if pathogenic_counts['PS'] >= 1:
            return 'Pathogenic'
        elif pathogenic_counts['PM'] >= 2:
            return 'Pathogenic'
        elif pathogenic_counts['PM'] >= 1 and pathogenic_counts['PP'] >= 1:
            return 'Pathogenic'
        elif pathogenic_counts['PP'] >= 2:
            return 'Likely Pathogenic'
    
    if pathogenic_counts['PS'] >= 2:
        return 'Pathogenic'
    
    if pathogenic_counts['PS'] >= 1:
        if pathogenic_counts['PM'] >= 3:
            return 'Pathogenic'
        elif pathogenic_counts['PM'] >= 2:
            return 'Likely Pathogenic'
        elif pathogenic_counts['PM'] >= 1 and pathogenic_counts['PP'] >= 2:
            return 'Likely Pathogenic'
        elif pathogenic_counts['PP'] >= 4:
            return 'Likely Pathogenic'
    
    # Benign combinations
    if benign_counts['BS'] >= 2:
        return 'Benign'
    
    if benign_counts['BS'] >= 1 and benign_counts['BP'] >= 1:
        return 'Likely Benign'
    
    if benign_counts['BP'] >= 2:
        return 'Likely Benign'
    
    # If no strong evidence either way
    return 'Uncertain Significance'

def format_evidence_summary(evidence_codes):
    """Format evidence codes for human-readable summary"""
    if not evidence_codes:
        return "No evidence assigned"
    
    # Group by strength
    evidence_groups = defaultdict(list)
    for code in evidence_codes:
        if code.startswith(('PVS', 'PS', 'PM', 'PP')):
            evidence_groups['pathogenic'].append(code)
        elif code.startswith(('BA', 'BS', 'BP')):
            evidence_groups['benign'].append(code)
    
    summary_parts = []
    if evidence_groups['pathogenic']:
        summary_parts.append(f"Pathogenic: {', '.join(sorted(evidence_groups['pathogenic']))}")
    if evidence_groups['benign']:
        summary_parts.append(f"Benign: {', '.join(sorted(evidence_groups['benign']))}")
    
    return "; ".join(summary_parts)

# =============================================================================
# VCF PARSING AND MAIN ANALYSIS
# =============================================================================

def parse_vep_annotation(vep_string):
    """Parse VEP annotation string"""
    if not vep_string or vep_string == '.':
        return []
    
    annotations = []
    for annotation in vep_string.split(','):
        fields = annotation.split('|')
        if len(fields) >= 14:
            ann = {
                'allele': fields[0],
                'consequence': fields[1],
                'impact': fields[2],
                'symbol': fields[3],
                'gene': fields[4],
                'feature_type': fields[5],
                'feature': fields[6],
                'biotype': fields[7],
                'exon': fields[8],
                'intron': fields[9],
                'hgvsc': fields[10],
                'hgvsp': fields[11],
                'cdna_position': fields[12],
                'cds_position': fields[13],
                'protein_position': fields[14] if len(fields) > 14 else '',
                'amino_acids': fields[15] if len(fields) > 15 else '',
                'codons': fields[16] if len(fields) > 16 else '',
                'existing_variation': fields[17] if len(fields) > 17 else '',
                'extra_fields': fields[18:] if len(fields) > 18 else []
            }
            annotations.append(ann)
    
    return annotations

def extract_variant_data(variant):
    """Extract comprehensive variant data from cyvcf2 variant - FIXED VERSION"""
    variant_data = {
        'chrom': variant.CHROM,
        'pos': variant.POS,
        'ref': variant.REF,
        'alt': str(variant.ALT[0]) if variant.ALT else '',
        'qual': variant.QUAL if variant.QUAL is not None else 0
    }
    
    # Extract frequencies - FIXED to handle VEP CSQ fields properly
    frequencies = {}
    max_af = 0.0
    
    # Try to get frequency from VEP annotation first
    if 'CSQ' in variant.INFO:
        csq = variant.INFO.get('CSQ')
        if csq:
            # Parse first transcript for frequency data
            first_transcript = csq.split(',')[0]
            fields = first_transcript.split('|')
            
            # Try different frequency field positions (VEP v114)
            frequency_positions = {
                'MAX_AF': 70,
                'gnomADe_AF': 51,
                'gnomADg_AF': 59,
                'gnomADe_NFE_AF': 56,
                'gnomADe_AFR_AF': 52
            }
            
            for freq_name, pos in frequency_positions.items():
                if len(fields) > pos and fields[pos]:
                    try:
                        freq_val = float(fields[pos])
                        frequencies[freq_name] = freq_val
                        if freq_val > max_af:
                            max_af = freq_val
                    except (ValueError, TypeError):
                        continue
    
    # Fallback: try to extract from INFO fields directly
    if hasattr(variant, 'INFO') and variant.INFO and max_af == 0.0:
        for key, value in variant.INFO:
            if 'AF' in key and value and value != '.':
                try:
                    freq_val = float(value) if isinstance(value, str) else float(value)
                    frequencies[key] = freq_val
                    if freq_val > max_af:
                        max_af = freq_val
                except (ValueError, TypeError):
                    continue
    
    variant_data['max_af'] = max_af
    variant_data['frequencies'] = frequencies
    
    # Extract pathogenicity scores - FIXED to handle VEP fields
    scores = {}
    if 'CSQ' in variant.INFO:
        csq = variant.INFO.get('CSQ')
        if csq:
            first_transcript = csq.split(',')[0]
            fields = first_transcript.split('|')
            
            # VEP field positions for predictions
            if len(fields) > 41:  # SIFT position
                sift_raw = fields[41]
                if sift_raw and '(' in sift_raw:
                    scores['SIFT_pred'] = sift_raw.split('(')[0]
                    scores['SIFT_score'] = sift_raw.split('(')[1].rstrip(')')
                elif sift_raw:
                    scores['SIFT_pred'] = sift_raw
            
            if len(fields) > 42:  # PolyPhen position
                polyphen_raw = fields[42]
                if polyphen_raw and '(' in polyphen_raw:
                    scores['Polyphen2_HDIV_pred'] = polyphen_raw.split('(')[0]
                    scores['Polyphen2_HDIV_score'] = polyphen_raw.split('(')[1].rstrip(')')
                elif polyphen_raw:
                    scores['Polyphen2_HDIV_pred'] = polyphen_raw
            
            # CADD scores
            if len(fields) > 77:  # CADD_PHRED position
                scores['CADD_phred'] = fields[77]
            if len(fields) > 78:  # CADD_RAW position
                scores['CADD_raw'] = fields[78]
    
    variant_data['pathogenicity_scores'] = scores
    
    # Extract ClinVar - FIXED to handle VEP fields
    clinvar = {}
    if 'CSQ' in variant.INFO:
        csq = variant.INFO.get('CSQ')
        if csq:
            first_transcript = csq.split(',')[0]
            fields = first_transcript.split('|')
            
            # ClinVar fields in VEP
            if len(fields) > 80:  # ClinVar_CLNSIG position
                clinvar['CLNSIG'] = fields[80]
            if len(fields) > 81:  # ClinVar_CLNREVSTAT position
                clinvar['CLNREVSTAT'] = fields[81]
            if len(fields) > 82:  # ClinVar_CLNDN position
                clinvar['CLNDN'] = fields[82]
    
    variant_data['clinvar'] = clinvar
    variant_data['clinvar_significance'] = clinvar.get('CLNSIG', '')
    
    return variant_data

def analyze_vcf_acmg(vcf_file, sample_id, output_dir, gene_list=None, inheritance='AD'):
    """Main ACMG analysis function"""
    logger = setup_logging(sample_id)
    
    logger.info(f"Starting ACMG/AMP classification for sample: {sample_id}")
    logger.info(f"VCF file: {vcf_file}")
    logger.info(f"Inheritance pattern: {inheritance}")
    logger.info(f"Gene list: {gene_list if gene_list else 'All genes'}")
    
    if not os.path.exists(vcf_file):
        logger.error(f"VCF file not found: {vcf_file}")
        return False
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Parse VCF and classify variants
    classified_variants = []
    
    try:
        vcf = cyvcf2.VCF(vcf_file)
        processed_count = 0
        
        for variant in vcf:
            processed_count += 1
            if processed_count % 5000 == 0:
                logger.info(f"Processed {processed_count} variants...")
            
            # Extract VEP annotations
            if 'CSQ' not in variant.INFO:
                continue
            
            vep_annotations = parse_vep_annotation(variant.INFO['CSQ'])
            
            for ann in vep_annotations:
                gene = ann['symbol']
                
                # Filter by gene list if provided
                if gene_list and gene not in gene_list:
                    continue
                
                # Only classify protein-coding variants
                if ann['biotype'] != 'protein_coding':
                    continue
                
                # Extract variant data
                variant_data = extract_variant_data(variant)
                
                # Add annotation data
                variant_data.update({
                    'symbol': gene,
                    'gene': ann['gene'],
                    'consequence': ann['consequence'],
                    'impact': ann['impact'],
                    'hgvsc': ann['hgvsc'],
                    'hgvsp': ann['hgvsp'],
                    'exon': ann['exon'],
                    'intron': ann['intron'],
                    'biotype': ann['biotype'],
                    'canonical': 'YES' in ann.get('extra_fields', []),
                    'mane_select': 'MANE_SELECT' in ann.get('extra_fields', [])
                })
                
                # Classify variant using ACMG guidelines
                acmg_result = classify_variant_acmg(variant_data, inheritance)
                variant_data.update(acmg_result)
                
                # Only keep variants with some evidence
                if acmg_result['evidence_codes']:
                    classified_variants.append(variant_data)
        
        logger.info(f"Classified {len(classified_variants)} variants with ACMG evidence")
        
    except Exception as e:
        logger.error(f"Error parsing VCF: {e}")
        return False
    
    if not classified_variants:
        logger.warning("No variants with ACMG evidence found")
        return False
    
    # Convert to DataFrame and sort by evidence score
    variants_df = pd.DataFrame(classified_variants)
    variants_df = variants_df.sort_values('evidence_score', ascending=False)
    
    # Generate reports
    try:
        generate_acmg_report(variants_df, sample_id, output_path, inheritance, logger)
        return True
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        return False

def generate_acmg_report(variants_df, sample_id, output_path, inheritance, logger):
    """Generate ACMG classification report"""
    
    # Summary statistics
    total_variants = len(variants_df)
    classification_counts = variants_df['classification'].value_counts()
    
    # Generate detailed CSV
    csv_file = output_path / f"{sample_id}_acmg_classified.csv"
    variants_df.to_csv(csv_file, index=False)
    
    # Generate summary JSON
    summary_data = {
        'sample_id': sample_id,
        'analysis_date': datetime.now().isoformat(),
        'inheritance_pattern': inheritance,
        'total_classified_variants': total_variants,
        'classification_counts': classification_counts.to_dict(),
        'evidence_code_frequency': {},
        'methodology': 'ACMG/AMP 2015 guidelines with 2025 clinical standards'
    }
    
    # Count evidence code frequency
    all_evidence = []
    for evidence_list in variants_df['evidence_codes']:
        all_evidence.extend(evidence_list)
    
    evidence_counts = pd.Series(all_evidence).value_counts()
    summary_data['evidence_code_frequency'] = evidence_counts.head(20).to_dict()
    
    json_file = output_path / f"{sample_id}_acmg_summary.json"
    with open(json_file, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    # Generate pathogenic/likely pathogenic variants report
    actionable_variants = variants_df[variants_df['classification'].isin(['Pathogenic', 'Likely Pathogenic'])]
    if not actionable_variants.empty:
        actionable_file = output_path / f"{sample_id}_pathogenic_variants.csv"
        actionable_variants.to_csv(actionable_file, index=False)
        logger.info(f"Pathogenic variants saved: {actionable_file}")
    
    logger.info(f"ACMG classification completed: {csv_file}")
    logger.info(f"Summary saved: {json_file}")
    logger.info(f"Classification breakdown: {dict(classification_counts)}")

# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(
        description="ACMG/AMP Automated Classifier v3.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Classify all variants (autosomal dominant)
    python3 acmg_classifier.py annotated.vcf.gz SAMPLE_001
    
    # X-linked inheritance pattern
    python3 acmg_classifier.py annotated.vcf.gz SAMPLE_001 --inheritance XL
    
    # Specific genes only
    python3 acmg_classifier.py annotated.vcf.gz SAMPLE_001 --genes BRCA1,BRCA2,TP53

Output Files:
    - {sample_id}_acmg_classified.csv       # All classified variants
    - {sample_id}_pathogenic_variants.csv   # Pathogenic/Likely pathogenic only
    - {sample_id}_acmg_summary.json         # Analysis summary

ACMG Evidence Codes:
    Pathogenic: PVS1 (very strong), PS1-4 (strong), PM1-6 (moderate), PP1-5 (supporting)
    Benign: BA1 (stand-alone), BS1-4 (strong), BP1-7 (supporting)
    
Classifications:
    Pathogenic, Likely Pathogenic, Uncertain Significance, Likely Benign, Benign
        """
    )
    
    parser.add_argument('vcf_file', help='VEP-annotated VCF file')
    parser.add_argument('sample_id', help='Sample identifier')
    parser.add_argument('--inheritance', choices=['AD', 'AR', 'XL'], default='AD',
                       help='Inheritance pattern (AD=autosomal dominant, AR=recessive, XL=X-linked)')
    parser.add_argument('--genes', help='Comma-separated list of genes to analyze')
    parser.add_argument('--output_dir', default=f"{BASE_DIR}/annotation_results/classification",
                       help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Parse gene list
    gene_list = None
    if args.genes:
        gene_list = set(gene.strip().upper() for gene in args.genes.split(','))
    
    # Setup logging
    logger = setup_logging(args.sample_id)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info("ACMG/AMP Automated Classifier v3.1 - Starting")
    logger.info(f"VCF file: {args.vcf_file}")
    logger.info(f"Sample ID: {args.sample_id}")
    logger.info(f"Inheritance: {args.inheritance}")
    
    # Run analysis
    success = analyze_vcf_acmg(args.vcf_file, args.sample_id, args.output_dir, 
                               gene_list, args.inheritance)
    
    if success:
        logger.info("ACMG classification completed successfully")
        print("\n" + "="*70)
        print("ACMG/AMP Variant Classification - COMPLETED")
        print("="*70)
        print(f"Sample: {args.sample_id}")
        print(f"Inheritance: {args.inheritance}")
        print(f"Results: {args.output_dir}")
        print("\nIMPORTANT:")
        print("- Research-grade classification for clinical guidance only")
        print("- Clinical validation required for medical decisions")
        print("- Review evidence codes for each variant")
        print("="*70)
        sys.exit(0)
    else:
        logger.error("ACMG classification failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
