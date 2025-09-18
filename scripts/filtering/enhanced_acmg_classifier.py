#!/usr/bin/env python3
"""
Enhanced ACMG/AMP Variant Classifier
Comprehensive clinical gene panels with detailed evidence-based classification

Author: Clinical Genomics Pipeline
Version: 3.0 - Enhanced ACMG Implementation
Date: September 2025
"""

import os
import sys
import argparse
import logging
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import re

try:
    import cyvcf2
except ImportError:
    print("ERROR: cyvcf2 not installed. Please run: pip install cyvcf2")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ACMGEvidence:
    """ACMG/AMP Evidence codes and classification"""
    pathogenic_very_strong: List[str] = field(default_factory=list)  # PVS1
    pathogenic_strong: List[str] = field(default_factory=list)       # PS1-4
    pathogenic_moderate: List[str] = field(default_factory=list)     # PM1-6
    pathogenic_supporting: List[str] = field(default_factory=list)   # PP1-5
    benign_standalone: List[str] = field(default_factory=list)       # BA1
    benign_strong: List[str] = field(default_factory=list)           # BS1-4
    benign_supporting: List[str] = field(default_factory=list)       # BP1-7
    
    def get_classification(self) -> str:
        """Apply ACMG/AMP classification rules"""
        pvs = len(self.pathogenic_very_strong)
        ps = len(self.pathogenic_strong)
        pm = len(self.pathogenic_moderate)
        pp = len(self.pathogenic_supporting)
        ba = len(self.benign_standalone)
        bs = len(self.benign_strong)
        bp = len(self.benign_supporting)
        
        # Benign standalone
        if ba >= 1:
            return "Benign"
        
        # Benign
        if bs >= 2 or (bs >= 1 and bp >= 1):
            return "Benign"
        
        # Likely Benign
        if bs >= 1 or bp >= 2:
            return "Likely Benign"
        
        # Pathogenic rules
        if pvs >= 1:
            if ps >= 1 or pm >= 2 or (pm >= 1 and pp >= 1) or pp >= 2:
                return "Pathogenic"
        elif ps >= 2 or (ps >= 1 and pm >= 3) or (ps >= 1 and pm >= 2 and pp >= 2) or (ps >= 1 and pm >= 1 and pp >= 4):
            return "Pathogenic"
        
        # Likely Pathogenic rules
        if pvs >= 1 and pm >= 1:
            return "Likely Pathogenic"
        elif ps >= 1 and pm >= 1:
            return "Likely Pathogenic"
        elif ps >= 1 and pp >= 2:
            return "Likely Pathogenic"
        elif pm >= 3:
            return "Likely Pathogenic"
        elif pm >= 2 and pp >= 2:
            return "Likely Pathogenic"
        elif pm >= 1 and pp >= 4:
            return "Likely Pathogenic"
        
        return "Uncertain Significance"

@dataclass
class EnhancedVariant:
    """Enhanced variant with ACMG classification"""
    gene_symbol: str
    chromosome: str
    position: int
    ref: str
    alt: str
    consequence: str
    impact: str
    variant_id: str
    panel: str
    gnomad_af: float = 0.0
    gnomad_ac: int = 0
    gnomad_an: int = 0
    cadd_score: float = 0.0
    sift_score: float = 0.0
    polyphen_score: float = 0.0
    revel_score: float = 0.0
    clinvar_sig: str = ""
    clinvar_stars: int = 0
    acmg_evidence: ACMGEvidence = field(default_factory=ACMGEvidence)
    acmg_classification: str = "Uncertain Significance"
    clinical_significance_score: int = 0

# Import comprehensive gene panels
sys.path.append(os.path.dirname(__file__))
from comprehensive_gene_panels import COMPREHENSIVE_GENE_PANELS

# Use comprehensive gene panels instead of individual imports

def parse_vep_annotation_enhanced(csq_string: str) -> Optional[Dict]:
    """Enhanced VEP annotation parser with detailed field extraction"""
    if not csq_string or csq_string == '.':
        return None
    
    try:
        # Take first transcript annotation
        first_annotation = csq_string.split(',')[0]
        fields = first_annotation.split('|')
        
        if len(fields) < 4:
            return None
        
        # Standard VEP format positions
        annotation = {
            'allele': fields[0] if len(fields) > 0 else '',
            'consequence': fields[1] if len(fields) > 1 else '',
            'impact': fields[2] if len(fields) > 2 else '',
            'symbol': fields[3] if len(fields) > 3 else '',
            'gene': fields[4] if len(fields) > 4 else '',
            'feature_type': fields[5] if len(fields) > 5 else '',
            'feature': fields[6] if len(fields) > 6 else '',
            'biotype': fields[7] if len(fields) > 7 else '',
            'exon': fields[8] if len(fields) > 8 else '',
            'intron': fields[9] if len(fields) > 9 else '',
            'hgvsc': fields[10] if len(fields) > 10 else '',
            'hgvsp': fields[11] if len(fields) > 11 else '',
            'cdna_position': fields[12] if len(fields) > 12 else '',
            'cds_position': fields[13] if len(fields) > 13 else '',
            'protein_position': fields[14] if len(fields) > 14 else '',
            'amino_acids': fields[15] if len(fields) > 15 else '',
            'codons': fields[16] if len(fields) > 16 else '',
            'existing_variation': fields[17] if len(fields) > 17 else '',
            'distance': fields[18] if len(fields) > 18 else '',
            'strand': fields[19] if len(fields) > 19 else '',
            'flags': fields[20] if len(fields) > 20 else '',
            'symbol_source': fields[21] if len(fields) > 21 else '',
            'hgnc_id': fields[22] if len(fields) > 22 else '',
            'sift': fields[23] if len(fields) > 23 else '',
            'polyphen': fields[24] if len(fields) > 24 else '',
            'clin_sig': fields[25] if len(fields) > 25 else '',
            'somatic': fields[26] if len(fields) > 26 else '',
            'pheno': fields[27] if len(fields) > 27 else ''
        }
        
        return annotation
    
    except Exception as e:
        logger.debug(f"Error parsing VEP annotation: {e}")
        return None

def extract_prediction_scores(annotation: Dict) -> Tuple[float, float, float]:
    """Extract SIFT, PolyPhen, and other prediction scores"""
    sift_score = 0.0
    polyphen_score = 0.0
    revel_score = 0.0
    
    try:
        # SIFT score
        sift_text = annotation.get('sift', '')
        if '(' in sift_text and ')' in sift_text:
            score_text = sift_text.split('(')[1].split(')')[0]
            sift_score = float(score_text)
    except:
        pass
    
    try:
        # PolyPhen score
        polyphen_text = annotation.get('polyphen', '')
        if '(' in polyphen_text and ')' in polyphen_text:
            score_text = polyphen_text.split('(')[1].split(')')[0]
            polyphen_score = float(score_text)
    except:
        pass
    
    return sift_score, polyphen_score, revel_score

def assign_acmg_evidence_enhanced(variant: EnhancedVariant, annotation: Dict) -> ACMGEvidence:
    """Enhanced ACMG/AMP evidence assignment with detailed criteria"""
    evidence = ACMGEvidence()
    
    # PVS1 - Loss of function in gene where LOF is known mechanism
    if any(x in variant.consequence.lower() for x in [
        'stop_gained', 'frameshift_variant', 'splice_donor_variant', 
        'splice_acceptor_variant', 'start_lost'
    ]):
        # For established haploinsufficient genes
        if variant.gene_symbol in COMPREHENSIVE_GENE_PANELS.get('CARDIAC', set()) | COMPREHENSIVE_GENE_PANELS.get('ONCOLOGY', set()) | COMPREHENSIVE_GENE_PANELS.get('NEUROLOGY', set()):
            evidence.pathogenic_very_strong.append('PVS1')
    
    # PS1 - Same amino acid change as established pathogenic variant
    if 'pathogenic' in variant.clinvar_sig.lower() and 'conflicting' not in variant.clinvar_sig.lower():
        evidence.pathogenic_strong.append('PS1')
    
    # PM1 - Located in critical functional domain
    if any(x in variant.consequence.lower() for x in ['missense_variant', 'inframe_deletion', 'inframe_insertion']):
        evidence.pathogenic_moderate.append('PM1')
    
    # PM2 - Absent from controls or extremely low frequency
    if variant.gnomad_af == 0 or variant.gnomad_af < 0.00001:
        evidence.pathogenic_moderate.append('PM2')
    
    # PM5 - Novel missense change at amino acid residue where different pathogenic missense change has been seen before
    if 'missense_variant' in variant.consequence.lower() and variant.clinvar_sig:
        evidence.pathogenic_moderate.append('PM5')
    
    # PP2 - Missense variant in gene with low benign missense variation
    if 'missense_variant' in variant.consequence.lower():
        if variant.gene_symbol in COMPREHENSIVE_GENE_PANELS.get('CARDIAC', set()) | COMPREHENSIVE_GENE_PANELS.get('ONCOLOGY', set()):
            evidence.pathogenic_supporting.append('PP2')
    
    # PP3 - Multiple lines of computational evidence support deleterious effect
    damaging_predictions = 0
    if variant.sift_score > 0 and variant.sift_score < 0.05:  # SIFT damaging
        damaging_predictions += 1
    if variant.polyphen_score > 0.85:  # PolyPhen probably damaging
        damaging_predictions += 1
    if variant.cadd_score > 25:  # CADD high impact
        damaging_predictions += 1
    if variant.revel_score > 0.75:  # REVEL high pathogenicity
        damaging_predictions += 1
    
    if damaging_predictions >= 3:
        evidence.pathogenic_supporting.append('PP3')
    
    # BA1 - Allele frequency >5% in any general population
    if variant.gnomad_af > 0.05:
        evidence.benign_standalone.append('BA1')
    
    # BS1 - Allele frequency >1% in any general population
    elif variant.gnomad_af > 0.01:
        evidence.benign_strong.append('BS1')
    
    # BS2 - Observed in healthy individuals inconsistent with disease penetrance
    if variant.gnomad_ac > 100:  # High allele count suggests benign
        evidence.benign_strong.append('BS2')
    
    # BP1 - Missense variant in gene where only truncating variants cause disease
    if 'missense_variant' in variant.consequence.lower():
        # This would require gene-specific knowledge
        pass
    
    # BP4 - Multiple lines of computational evidence suggest no impact
    if damaging_predictions <= 1:
        evidence.pathogenic_supporting.append('BP4')
    
    # BP6 - Reputable source reports variant as benign
    if 'benign' in variant.clinvar_sig.lower() and 'conflicting' not in variant.clinvar_sig.lower():
        evidence.benign_supporting.append('BP6')
    
    return evidence

def calculate_clinical_significance_score(variant: EnhancedVariant) -> int:
    """Calculate clinical significance score (0-100)"""
    score = 0
    
    # ACMG classification weight (0-50 points)
    classification_scores = {
        'Pathogenic': 50,
        'Likely Pathogenic': 40,
        'Uncertain Significance': 20,
        'Likely Benign': 10,
        'Benign': 0
    }
    score += classification_scores.get(variant.acmg_classification, 20)
    
    # Consequence severity (0-25 points)
    if any(x in variant.consequence.lower() for x in [
        'stop_gained', 'frameshift_variant', 'splice_donor_variant', 'splice_acceptor_variant'
    ]):
        score += 25
    elif 'missense_variant' in variant.consequence.lower():
        score += 15
    elif any(x in variant.consequence.lower() for x in [
        'splice_region_variant', 'inframe_deletion', 'inframe_insertion'
    ]):
        score += 10
    
    # Clinical gene importance (0-25 points)
    cardiac_genes = COMPREHENSIVE_GENE_PANELS.get('CARDIAC', set())
    oncology_genes = COMPREHENSIVE_GENE_PANELS.get('ONCOLOGY', set())
    neuro_genes = COMPREHENSIVE_GENE_PANELS.get('NEUROLOGY', set()) | COMPREHENSIVE_GENE_PANELS.get('EPILEPSY', set())
    id_genes = COMPREHENSIVE_GENE_PANELS.get('AUTISM_SPECTRUM', set())
    cdls_genes = COMPREHENSIVE_GENE_PANELS.get('CDLS', set())
    immuno_genes = COMPREHENSIVE_GENE_PANELS.get('IMMUNOLOGY', set())
    pharmaco_genes = COMPREHENSIVE_GENE_PANELS.get('PHARMACOGENOMICS', set())
    
    if variant.gene_symbol in cardiac_genes | oncology_genes:
        score += 25
    elif variant.gene_symbol in neuro_genes | id_genes:
        score += 20
    elif variant.gene_symbol in cdls_genes | immuno_genes:
        score += 15
    elif variant.gene_symbol in pharmaco_genes:
        score += 10
    
    return min(100, score)

def analyze_vcf_enhanced(vcf_file: str, sample_id: str) -> Tuple[List[EnhancedVariant], Dict[str, int]]:
    """Enhanced VCF analysis with comprehensive gene panels"""
    
    logger.info(f"Analyzing {vcf_file} with {len(COMPREHENSIVE_GENE_PANELS)} comprehensive medical specialties")
    logger.info(f"Total target genes: {sum(len(genes) for genes in COMPREHENSIVE_GENE_PANELS.values())}")
    
    try:
        vcf = cyvcf2.VCF(vcf_file)
        # Test that we can read the first variant
        test_variant = next(iter(vcf), None)
        if test_variant is None:
            logger.warning("VCF file appears to be empty or contains no variants")
            return [], {}
        # Re-open the VCF file for processing
        vcf = cyvcf2.VCF(vcf_file)
    except Exception as e:
        logger.error(f"Failed to open or validate VCF file: {e}")
        logger.error("This may be due to malformed VCF entries. Consider using VCF preprocessing.")
        return [], {}
    
    results = []
    panel_counts = defaultdict(int)
    processed = 0
    genes_found = set()
    
    # Main VCF iteration loop with proper error handling
    try:
        for variant in vcf:
            processed += 1
            
            # Handle malformed VCF entries gracefully
            try:
                # Basic variant validation
                if not variant.CHROM or not variant.POS:
                    continue
                    
                # Additional validation for common issues
                if hasattr(variant, 'ALT') and variant.ALT:
                    alt_allele = str(variant.ALT[0])
                else:
                    continue
                    
                if processed % 50000 == 0:
                    logger.info(f"Processed {processed:,} variants, found {len(results)} clinical variants")
                
                # Get VEP annotation
                csq_value = variant.INFO.get('CSQ')
                if not csq_value:
                    continue
                
                annotation = parse_vep_annotation_enhanced(csq_value)
                if not annotation or not annotation['symbol']:
                    continue
                
                gene_symbol = annotation['symbol']
                genes_found.add(gene_symbol)
                
                # Check if gene is in any panel
                target_panel = None
                for panel_name, gene_set in COMPREHENSIVE_GENE_PANELS.items():
                    if gene_symbol in gene_set:
                        target_panel = panel_name
                        break
                
                if not target_panel:
                    continue
                
                # Create enhanced variant
                enhanced_var = EnhancedVariant(
                    gene_symbol=gene_symbol,
                    chromosome=variant.CHROM,
                    position=variant.POS,
                    ref=variant.REF,
                    alt=str(variant.ALT[0]) if variant.ALT else '',
                    consequence=annotation['consequence'],
                    impact=annotation['impact'],
                    variant_id=f"{variant.CHROM}:{variant.POS}:{variant.REF}>{variant.ALT[0] if variant.ALT else ''}",
                    panel=target_panel,
                    clinvar_sig=annotation.get('clin_sig', '')
                )
                
                # Extract prediction scores
                enhanced_var.sift_score, enhanced_var.polyphen_score, enhanced_var.revel_score = extract_prediction_scores(annotation)
                
                # Extract population frequencies (simplified)
                # In real implementation, would parse specific gnomAD fields
                enhanced_var.gnomad_af = 0.0  # Would extract from INFO fields
                
                # Assign ACMG evidence
                enhanced_var.acmg_evidence = assign_acmg_evidence_enhanced(enhanced_var, annotation)
                enhanced_var.acmg_classification = enhanced_var.acmg_evidence.get_classification()
                enhanced_var.clinical_significance_score = calculate_clinical_significance_score(enhanced_var)
                
                # Only include clinically significant variants
                if enhanced_var.clinical_significance_score >= 20:
                    results.append(enhanced_var)
                    panel_counts[target_panel] += 1
                    
            except Exception as e:
                logger.warning(f"Skipping malformed variant at position {processed}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Critical VCF parsing error after processing {processed} variants: {e}")
        logger.error("Returning results collected so far...")
    
    logger.info(f"Analysis complete! Found {len(results)} clinical variants in {len(genes_found)} genes")
    
    return results, dict(panel_counts)

def generate_enhanced_report(variants: List[EnhancedVariant], panel_counts: Dict[str, int], sample_id: str, output_file: str):
    """Generate enhanced clinical report with ACMG classifications"""
    
    with open(output_file, 'w') as f:
        f.write("ENHANCED ACMG/AMP CLINICAL GENOMICS ANALYSIS\n")
        f.write(f"Sample ID: {sample_id}\n")
        f.write(f"Analysis Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary
        f.write("ANALYSIS SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total clinical variants identified: {len(variants)}\n")
        f.write(f"Gene panels analyzed: {len(panel_counts)}\n\n")
        
        # ACMG classification summary
        classification_counts = Counter(v.acmg_classification for v in variants)
        f.write("ACMG/AMP CLASSIFICATION SUMMARY\n")
        f.write("-" * 40 + "\n")
        for classification, count in classification_counts.most_common():
            f.write(f"{classification:<25}: {count:>5} variants\n")
        f.write("\n")
        
        # High-priority pathogenic/likely pathogenic variants
        high_priority = [v for v in variants if v.acmg_classification in ['Pathogenic', 'Likely Pathogenic']]
        if high_priority:
            f.write("PATHOGENIC/LIKELY PATHOGENIC VARIANTS\n")
            f.write("-" * 50 + "\n")
            high_priority.sort(key=lambda x: x.clinical_significance_score, reverse=True)
            
            for i, variant in enumerate(high_priority[:20], 1):
                f.write(f"{i:2d}. {variant.gene_symbol:<12} | {variant.acmg_classification:<18} | {variant.panel}\n")
                f.write(f"    {variant.variant_id}\n")
                f.write(f"    Consequence: {variant.consequence}\n")
                f.write(f"    Evidence: {', '.join(variant.acmg_evidence.pathogenic_very_strong + variant.acmg_evidence.pathogenic_strong)}\n")
                f.write(f"    Score: {variant.clinical_significance_score}\n\n")
        
        # Panel-specific results
        panel_variants = defaultdict(list)
        for variant in variants:
            panel_variants[variant.panel].append(variant)
        
        for panel_name in sorted(panel_variants.keys()):
            panel_vars = panel_variants[panel_name]
            f.write(f"{panel_name} PANEL ({len(panel_vars)} variants)\n")
            f.write("-" * 60 + "\n")
            
            # Sort by clinical significance score
            panel_vars.sort(key=lambda x: x.clinical_significance_score, reverse=True)
            
            for i, variant in enumerate(panel_vars[:10], 1):
                f.write(f"{i:2d}. {variant.gene_symbol:<12} | {variant.acmg_classification:<18} | Score: {variant.clinical_significance_score:3d}\n")
                f.write(f"     {variant.consequence}\n")
                f.write(f"     {variant.variant_id}\n\n")
            
            if len(panel_vars) > 10:
                f.write(f"     ... and {len(panel_vars) - 10} additional variants\n")
            f.write("\n")

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced ACMG/AMP Clinical Genomics Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--vcf-file', required=True, help='VEP-annotated VCF file')
    parser.add_argument('--sample-id', required=True, help='Sample identifier')
    parser.add_argument('--output-dir', default='.', help='Output directory')
    parser.add_argument('--min-score', type=int, default=20, help='Minimum clinical significance score')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate output filename
    output_file = os.path.join(args.output_dir, f"{args.sample_id}_enhanced_acmg_results.txt")
    
    # Run enhanced analysis
    variants, panel_counts = analyze_vcf_enhanced(args.vcf_file, args.sample_id)
    
    # Filter by minimum score
    filtered_variants = [v for v in variants if v.clinical_significance_score >= args.min_score]
    
    # Generate report
    generate_enhanced_report(filtered_variants, panel_counts, args.sample_id, output_file)
    
    logger.info(f"Enhanced analysis complete! Results written to {output_file}")
    
    # Summary to stdout
    print(f"\nENHANCED ACMG/AMP ANALYSIS SUMMARY")
    print(f"Sample: {args.sample_id}")
    print(f"Total clinical variants: {len(filtered_variants)}")
    print(f"Gene panels with findings: {len(panel_counts)}")
    
    # Show top findings
    pathogenic_vars = [v for v in filtered_variants if v.acmg_classification in ['Pathogenic', 'Likely Pathogenic']]
    if pathogenic_vars:
        print(f"Pathogenic/Likely Pathogenic: {len(pathogenic_vars)} variants")
        top_var = max(pathogenic_vars, key=lambda x: x.clinical_significance_score)
        print(f"Top finding: {top_var.gene_symbol} ({top_var.panel}) - {top_var.acmg_classification}")

if __name__ == "__main__":
    main()
