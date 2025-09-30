#!/usr/bin/env python3
"""
ENHANCED: Comprehensive Clinical Gene Analysis System
Multi-transcript VEP CSQ parser - extracts ALL valid scores from '&' separated values
FIXES: REVEL, AlphaMissense, CADD, ClinVar multi-transcript parsing
"""

import argparse
import pandas as pd
import numpy as np
import json
import gzip
import re
from pathlib import Path
from datetime import datetime
import logging
from collections import defaultdict
import cyvcf2

# Import gene panels from the proper location
from gene_panels_database import COMPREHENSIVE_GENE_PANELS, ALL_COMPREHENSIVE_GENES

class VEPCSQParser:
    """Parser for VEP CSQ format that reads header to determine field positions"""
    
    def __init__(self, vcf_path):
        self.vcf_path = vcf_path
        self.csq_fields = []
        self.field_indices = {}
        self._parse_csq_header()
    
    def _parse_csq_header(self):
        """Parse VCF header to extract CSQ field positions"""
        print("🔍 Parsing VEP CSQ header format...")
        
        try:
            vcf = cyvcf2.VCF(self.vcf_path)
            
            # Look for CSQ header in raw header
            for line in vcf.raw_header.split('\n'):
                if line.startswith('##INFO=<ID=CSQ,'):
                    # Extract format string
                    format_match = re.search(r'Format:\s*([^"]+)', line)
                    if format_match:
                        format_string = format_match.group(1).strip()
                        self.csq_fields = format_string.split('|')
                        
                        # Create index mapping for quick lookup
                        for i, field in enumerate(self.csq_fields):
                            self.field_indices[field] = i
                        
                        print(f"✅ Found CSQ format with {len(self.csq_fields)} fields")
                        print("📋 Enhanced multi-transcript parser enabled!")
                        break
            
            vcf.close()
            return len(self.csq_fields) > 0
            
        except Exception as e:
            print(f"❌ Error parsing VCF header: {e}")
            return False
    
    def get_field_value(self, csq_annotation, field_name):
        """Extract specific field value from CSQ annotation string"""
        if not csq_annotation or not self.csq_fields:
            return ""
        
        # Split by pipe for individual fields
        fields = csq_annotation.split('|')
        
        # Try exact match first
        if field_name in self.field_indices:
            idx = self.field_indices[field_name]
            if idx < len(fields):
                return fields[idx].strip()
        
        # Try fuzzy match for common variations
        fuzzy_matches = {
            'REVEL': ['REVEL_score', 'REVEL'],
            'AlphaMissense': ['am_pathogenicity', 'AlphaMissense', 'AM_pathogenicity', 'AlphaMissense_am_pathogenicity'],
            'CADD': ['CADD_phred', 'CADD_PHRED', 'CADD'],
            'ClinVar': ['ClinVar_CLNSIG', 'CLNSIG', 'ClinVar']
        }
        
        if field_name in fuzzy_matches:
            for variant in fuzzy_matches[field_name]:
                if variant in self.field_indices:
                    idx = self.field_indices[variant]
                    if idx < len(fields):
                        return fields[idx].strip()
        
        return ""
    
    def extract_genes_from_csq(self, csq_value):
        """Extract gene symbols from CSQ field"""
        genes = set()
        
        if not csq_value or not self.csq_fields:
            return list(genes)
        
        # Split by comma for multiple transcript annotations
        for annotation in csq_value.split(','):
            # Extract SYMBOL
            gene_symbol = self.get_field_value(annotation, 'SYMBOL')
            if gene_symbol and gene_symbol != '.':
                genes.add(gene_symbol)
        
        return list(genes)
    
    def extract_consequence_from_csq(self, csq_value):
        """Extract consequence from CSQ field"""
        if not csq_value:
            return 'unknown'
        
        # Get first annotation (typically most severe)
        first_annotation = csq_value.split(',')[0]
        return self.get_field_value(first_annotation, 'Consequence') or 'unknown'

class ComprehensiveGeneDatabase:
    """Comprehensive database of clinical genes"""
    
    def __init__(self):
        self.genes = {}
        self.evidence_hierarchy = {
            'TIER_1_CLINICAL': 100, 'TIER_2_EXPERT': 90, 'TIER_3_CLINICAL_LAB': 80,
            'TIER_4_ESTABLISHED': 70, 'TIER_5_EMERGING': 60, 'TIER_6_RESEARCH': 50, 'TIER_7_MINIMAL': 30
        }
        self.actionability_scores = {
            'IMMEDIATELY_ACTIONABLE': 50, 'SCREENING_ACTIONABLE': 40, 'FAMILY_ACTIONABLE': 30,
            'COUNSELING_INDICATED': 20, 'RESEARCH_INTEREST': 10, 'UNCERTAIN_ACTIONABILITY': 5
        }
        self._build_comprehensive_database()
    
    def _build_comprehensive_database(self):
        print("🧬 Building comprehensive clinical gene database...")
        self._add_acmg_genes()
        self._add_clingen_genes()
        self._add_clinical_lab_genes()
        self._add_omim_genes()
        self._add_clinvar_genes()
        self._add_specialty_genes()
        self._add_research_genes()
        print(f"✅ Comprehensive database built: {len(self.genes)} genes")
    
    def _add_acmg_genes(self):
        """Add ACMG Secondary Findings v3.3 genes"""
        acmg_genes = {
            'ACTC1': {'condition': 'Hypertrophic cardiomyopathy', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'MYBPC3': {'condition': 'Hypertrophic cardiomyopathy', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'MYH7': {'condition': 'Hypertrophic cardiomyopathy', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'TNNI3': {'condition': 'Hypertrophic cardiomyopathy', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'TNNT2': {'condition': 'Hypertrophic cardiomyopathy', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'TPM1': {'condition': 'Hypertrophic cardiomyopathy', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'KCNH2': {'condition': 'Long QT syndrome', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'KCNQ1': {'condition': 'Long QT syndrome', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'SCN5A': {'condition': 'Brugada syndrome', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'RYR2': {'condition': 'CPVT', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'TTN': {'condition': 'Dilated cardiomyopathy', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'KCNE1': {'condition': 'Long QT syndrome', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'KCNE2': {'condition': 'Long QT syndrome', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'BRCA1': {'condition': 'Hereditary breast/ovarian cancer', 'actionability': 'SCREENING_ACTIONABLE'},
            'BRCA2': {'condition': 'Hereditary breast/ovarian cancer', 'actionability': 'SCREENING_ACTIONABLE'},
            'MLH1': {'condition': 'Lynch syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'MSH2': {'condition': 'Lynch syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'APC': {'condition': 'Familial adenomatous polyposis', 'actionability': 'SCREENING_ACTIONABLE'},
            'TP53': {'condition': 'Li-Fraumeni syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'VHL': {'condition': 'Von Hippel-Lindau syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'FBN1': {'condition': 'Marfan syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'COL3A1': {'condition': 'Ehlers-Danlos syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'LDLR': {'condition': 'Familial hypercholesterolemia', 'actionability': 'IMMEDIATELY_ACTIONABLE'}
        }
        
        for gene, info in acmg_genes.items():
            self.genes[gene] = {
                'evidence_tier': 'TIER_1_CLINICAL', 'evidence_score': 100,
                'actionability': info['actionability'], 'condition': info['condition'],
                'source': 'ACMG_SF_v3.3', 'specialty': self._categorize_specialty(info['condition']),
                'inheritance': 'AUTOSOMAL_DOMINANT', 'actionability_score': self.actionability_scores[info['actionability']],
                'total_score': 100 + self.actionability_scores[info['actionability']]
            }
    
    def _add_clingen_genes(self):
        """Add 20 additional ClinGen genes"""
        clingen_genes = {
            'LMNA': {'condition': 'Dilated cardiomyopathy', 'actionability': 'SCREENING_ACTIONABLE'},
            'DMD': {'condition': 'Duchenne muscular dystrophy', 'actionability': 'FAMILY_ACTIONABLE'},
            'HTT': {'condition': 'Huntington disease', 'actionability': 'COUNSELING_INDICATED'},
            'GJB2': {'condition': 'Hearing loss', 'actionability': 'FAMILY_ACTIONABLE'},
            'CFTR': {'condition': 'Cystic fibrosis', 'actionability': 'FAMILY_ACTIONABLE'},
            'PALB2': {'condition': 'Breast cancer predisposition', 'actionability': 'SCREENING_ACTIONABLE'},
            'ATM': {'condition': 'Ataxia telangiectasia', 'actionability': 'SCREENING_ACTIONABLE'},
            'CHEK2': {'condition': 'Breast cancer predisposition', 'actionability': 'SCREENING_ACTIONABLE'},
            'NF1': {'condition': 'Neurofibromatosis type 1', 'actionability': 'SCREENING_ACTIONABLE'},
            'TSC1': {'condition': 'Tuberous sclerosis', 'actionability': 'SCREENING_ACTIONABLE'},
            'TSC2': {'condition': 'Tuberous sclerosis', 'actionability': 'SCREENING_ACTIONABLE'},
            'PTEN': {'condition': 'PTEN hamartoma syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'SCN1A': {'condition': 'Dravet syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'PAH': {'condition': 'Phenylketonuria', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'GAA': {'condition': 'Pompe disease', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'GBA': {'condition': 'Gaucher disease', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'HEXA': {'condition': 'Tay-Sachs disease', 'actionability': 'FAMILY_ACTIONABLE'},
            'COL1A1': {'condition': 'Osteogenesis imperfecta', 'actionability': 'COUNSELING_INDICATED'},
            'FGFR3': {'condition': 'Achondroplasia', 'actionability': 'COUNSELING_INDICATED'},
            'BTK': {'condition': 'X-linked agammaglobulinemia', 'actionability': 'IMMEDIATELY_ACTIONABLE'}
        }
        
        for gene, info in clingen_genes.items():
            if gene not in self.genes:
                self.genes[gene] = {
                    'evidence_tier': 'TIER_2_EXPERT', 'evidence_score': 90,
                    'actionability': info['actionability'], 'condition': info['condition'],
                    'source': 'ClinGen_Expert_Panel', 'specialty': self._categorize_specialty(info['condition']),
                    'inheritance': 'AUTOSOMAL_DOMINANT', 'actionability_score': self.actionability_scores[info['actionability']],
                    'total_score': 90 + self.actionability_scores[info['actionability']]
                }
    
    def _add_clinical_lab_genes(self):
        """Add clinical lab genes"""
        lab_genes = {
            'RAD51C': {'condition': 'Ovarian cancer predisposition', 'actionability': 'SCREENING_ACTIONABLE'},
            'RAD51D': {'condition': 'Ovarian cancer predisposition', 'actionability': 'SCREENING_ACTIONABLE'},
            'CDKN2A': {'condition': 'Melanoma predisposition', 'actionability': 'SCREENING_ACTIONABLE'},
            'STK11': {'condition': 'Peutz-Jeghers syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'MSH6': {'condition': 'Lynch syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'PMS2': {'condition': 'Lynch syndrome', 'actionability': 'SCREENING_ACTIONABLE'},
            'SDHB': {'condition': 'Paraganglioma', 'actionability': 'SCREENING_ACTIONABLE'},
            'SDHD': {'condition': 'Paraganglioma', 'actionability': 'SCREENING_ACTIONABLE'},
            'RET': {'condition': 'Multiple endocrine neoplasia', 'actionability': 'SCREENING_ACTIONABLE'},
            'MEN1': {'condition': 'Multiple endocrine neoplasia type 1', 'actionability': 'SCREENING_ACTIONABLE'},
            'HFE': {'condition': 'Hereditary hemochromatosis', 'actionability': 'SCREENING_ACTIONABLE'},
            'APOB': {'condition': 'Familial hypercholesterolemia', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'PCSK9': {'condition': 'Familial hypercholesterolemia', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'CYP2D6': {'condition': 'Drug metabolism', 'actionability': 'IMMEDIATELY_ACTIONABLE'}
        }
        
        for gene, info in lab_genes.items():
            if gene not in self.genes:
                self.genes[gene] = {
                    'evidence_tier': 'TIER_3_CLINICAL_LAB', 'evidence_score': 80,
                    'actionability': info['actionability'], 'condition': info['condition'],
                    'source': 'Clinical_Laboratory_Panels', 'specialty': self._categorize_specialty(info['condition']),
                    'inheritance': 'AUTOSOMAL_DOMINANT', 'actionability_score': self.actionability_scores[info['actionability']],
                    'total_score': 80 + self.actionability_scores[info['actionability']]
                }
    
    def _add_omim_genes(self):
        """Add OMIM genes"""
        omim_genes = {
            'G6PC': {'condition': 'Glycogen storage disease type Ia', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'IL2RG': {'condition': 'SCID', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'CYBB': {'condition': 'Chronic granulomatous disease', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'NF2': {'condition': 'Neurofibromatosis type 2', 'actionability': 'SCREENING_ACTIONABLE'},
            'COL1A2': {'condition': 'Osteogenesis imperfecta', 'actionability': 'COUNSELING_INDICATED'},
            'SMN1': {'condition': 'Spinal muscular atrophy', 'actionability': 'FAMILY_ACTIONABLE'},
            'MYO7A': {'condition': 'Usher syndrome', 'actionability': 'FAMILY_ACTIONABLE'},
            'ABCA4': {'condition': 'Stargardt disease', 'actionability': 'COUNSELING_INDICATED'},
            'CEP290': {'condition': 'Leber congenital amaurosis', 'actionability': 'COUNSELING_INDICATED'},
            'SCN2A': {'condition': 'Epileptic encephalopathy', 'actionability': 'COUNSELING_INDICATED'},
            'SCN8A': {'condition': 'Epileptic encephalopathy', 'actionability': 'COUNSELING_INDICATED'},
            'KCNT1': {'condition': 'Epileptic encephalopathy', 'actionability': 'COUNSELING_INDICATED'},
            'CACNA1C': {'condition': 'Timothy syndrome', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'TPMT': {'condition': 'Thiopurine metabolism', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'DPYD': {'condition': 'Fluoropyrimidine metabolism', 'actionability': 'IMMEDIATELY_ACTIONABLE'}
        }
        
        for gene, info in omim_genes.items():
            if gene not in self.genes:
                self.genes[gene] = {
                    'evidence_tier': 'TIER_4_ESTABLISHED', 'evidence_score': 70,
                    'actionability': info['actionability'], 'condition': info['condition'],
                    'source': 'OMIM_Established', 'specialty': self._categorize_specialty(info['condition']),
                    'inheritance': 'AUTOSOMAL_DOMINANT', 'actionability_score': self.actionability_scores[info['actionability']],
                    'total_score': 70 + self.actionability_scores[info['actionability']]
                }
    
    def _add_clinvar_genes(self):
        """Add ClinVar genes"""
        clinvar_genes = {
            'NIPBL': {'condition': 'Cornelia de Lange syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'SMC1A': {'condition': 'Cornelia de Lange syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'SMC3': {'condition': 'Cornelia de Lange syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'RAD21': {'condition': 'Cornelia de Lange syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'HDAC8': {'condition': 'Cornelia de Lange syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'CHD7': {'condition': 'CHARGE syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'CREBBP': {'condition': 'Rubinstein-Taybi syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'GATA4': {'condition': 'Congenital heart disease', 'actionability': 'SCREENING_ACTIONABLE'},
            'GATA6': {'condition': 'Congenital heart disease', 'actionability': 'SCREENING_ACTIONABLE'},
            'TBX5': {'condition': 'Holt-Oram syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'NKX2-5': {'condition': 'Congenital heart disease', 'actionability': 'COUNSELING_INDICATED'}
        }
        
        for gene, info in clinvar_genes.items():
            if gene not in self.genes:
                self.genes[gene] = {
                    'evidence_tier': 'TIER_5_EMERGING', 'evidence_score': 60,
                    'actionability': info['actionability'], 'condition': info['condition'],
                    'source': 'ClinVar_Pathogenic', 'specialty': self._categorize_specialty(info['condition']),
                    'inheritance': 'AUTOSOMAL_DOMINANT', 'actionability_score': self.actionability_scores[info['actionability']],
                    'total_score': 60 + self.actionability_scores[info['actionability']]
                }
    
    def _add_specialty_genes(self):
        """Add specialty genes"""
        specialty_genes = {
            'EGFR': {'condition': 'Lung cancer', 'actionability': 'RESEARCH_INTEREST'},
            'KRAS': {'condition': 'Colorectal cancer', 'actionability': 'RESEARCH_INTEREST'},
            'PIK3CA': {'condition': 'Breast cancer', 'actionability': 'RESEARCH_INTEREST'},
            'CYP2C19': {'condition': 'Drug metabolism', 'actionability': 'IMMEDIATELY_ACTIONABLE'},
            'ARID1A': {'condition': 'Coffin-Siris syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'ARID1B': {'condition': 'Coffin-Siris syndrome', 'actionability': 'COUNSELING_INDICATED'},
            'PKP2': {'condition': 'ARVC', 'actionability': 'SCREENING_ACTIONABLE'},
            'DSC2': {'condition': 'ARVC', 'actionability': 'SCREENING_ACTIONABLE'},
            'DSG2': {'condition': 'ARVC', 'actionability': 'SCREENING_ACTIONABLE'}
        }
        
        for gene, info in specialty_genes.items():
            if gene not in self.genes:
                self.genes[gene] = {
                    'evidence_tier': 'TIER_6_RESEARCH', 'evidence_score': 50,
                    'actionability': info['actionability'], 'condition': info['condition'],
                    'source': 'Specialty_Databases', 'specialty': self._categorize_specialty(info['condition']),
                    'inheritance': 'AUTOSOMAL_DOMINANT', 'actionability_score': self.actionability_scores[info['actionability']],
                    'total_score': 50 + self.actionability_scores[info['actionability']]
                }
    
    def _add_research_genes(self):
        """Add research genes"""
        research_genes = {
            'ANKRD11': {'condition': 'KBG syndrome', 'actionability': 'RESEARCH_INTEREST'},
            'POGZ': {'condition': 'Intellectual disability', 'actionability': 'RESEARCH_INTEREST'},
            'SETD2': {'condition': 'Luscan-Lumish syndrome', 'actionability': 'RESEARCH_INTEREST'},
            'KDM6A': {'condition': 'Kabuki syndrome', 'actionability': 'RESEARCH_INTEREST'},
            'ARID2': {'condition': 'Intellectual disability', 'actionability': 'RESEARCH_INTEREST'}
        }
        
        for gene, info in research_genes.items():
            if gene not in self.genes:
                self.genes[gene] = {
                    'evidence_tier': 'TIER_7_MINIMAL', 'evidence_score': 30,
                    'actionability': info['actionability'], 'condition': info['condition'],
                    'source': 'Research_Literature', 'specialty': self._categorize_specialty(info['condition']),
                    'inheritance': 'AUTOSOMAL_DOMINANT', 'actionability_score': self.actionability_scores[info['actionability']],
                    'total_score': 30 + self.actionability_scores[info['actionability']]
                }
    
    def _categorize_specialty(self, condition):
        """Categorize condition into medical specialty"""
        condition_lower = condition.lower()
        if any(term in condition_lower for term in ['cardio', 'heart', 'arrhyth', 'aortic', 'qt']):
            return 'CARDIAC'
        elif any(term in condition_lower for term in ['cancer', 'tumor', 'oncol', 'melanoma', 'breast', 'ovarian']):
            return 'ONCOLOGY'
        elif any(term in condition_lower for term in ['drug', 'metabolism']):
            return 'PHARMACOGENOMICS'
        else:
            return 'OTHER'

class ComprehensiveVariantAnalyzer:
    """ENHANCED: Multi-transcript VEP CSQ parser"""
    
    def __init__(self, gene_database):
        self.gene_db = gene_database
        self.variant_results = []
        self.csq_parser = None
        
    def analyze_annotated_vcf(self, vcf_path, sample_id):
        """Analyze pre-annotated VCF with ENHANCED multi-transcript parsing"""
        
        print(f"🔬 Analyzing {sample_id} against {len(self.gene_db.genes)} genes...")
        print("🚀 Enhanced multi-transcript parser enabled!")
        
        # Initialize VEP CSQ parser
        self.csq_parser = VEPCSQParser(vcf_path)
        if not self.csq_parser.csq_fields:
            print("❌ Could not parse VEP CSQ format from VCF header")
            return False
        
        variants_found = 0
        clinically_significant = 0
        
        try:
            vcf = cyvcf2.VCF(vcf_path)
            
            variant_count = 0
            for variant in vcf:
                variant_count += 1
                if variant_count % 100000 == 0:
                    print(f"   Processed {variant_count:,} variants...")
                
                # Extract CSQ value
                csq_value = variant.INFO.get('CSQ', '')
                
                if csq_value:
                    # Extract gene symbols using proper CSQ parser
                    gene_symbols = self.csq_parser.extract_genes_from_csq(csq_value)
                    
                    for gene in gene_symbols:
                        if gene in self.gene_db.genes:
                            variants_found += 1
                            
                            # Calculate variant significance
                            variant_score = self._calculate_variant_score(variant, gene, csq_value)
                            
                            if variant_score >= 50:  # Clinically significant threshold
                                clinically_significant += 1
                            
                            variant_result = {
                                'gene': gene,
                                'chromosome': variant.CHROM,
                                'position': variant.POS,
                                'ref': variant.REF,
                                'alt': str(variant.ALT[0]),
                                'variant_score': variant_score,
                                'gene_info': self.gene_db.genes[gene],
                                'consequence': self.csq_parser.extract_consequence_from_csq(csq_value),
                                'clinvar_sig': self._extract_clinvar_from_csq(csq_value),
                                'gnomad_af': self._extract_gnomad_af_from_csq(csq_value),
                                'revel_score': self._extract_revel_from_csq(csq_value),
                                'alphamissense_score': self._extract_alphamissense_from_csq(csq_value),
                                'cadd_score': self._extract_cadd_from_csq(csq_value),
                                'raw_csq': csq_value[:200] + '...' if len(csq_value) > 200 else csq_value
                            }
                            
                            self.variant_results.append(variant_result)
            
            vcf.close()
            
        except Exception as e:
            print(f"❌ Error reading VCF: {e}")
            return False
        
        # Sort results by combined score
        self.variant_results.sort(key=lambda x: x['gene_info']['total_score'] + x['variant_score'], reverse=True)
        
        print(f"✅ Analysis complete:")
        print(f"   Total variants processed: {variant_count:,}")
        print(f"   Variants in comprehensive genes: {variants_found:,}")
        print(f"   Clinically significant variants: {clinically_significant:,}")
        print(f"   Unique genes with variants: {len(set(r['gene'] for r in self.variant_results)):,}")
        
        return True
    
    def _extract_best_score_from_multivalue(self, raw_value, score_type='default'):
        """
        ENHANCED: Extract the best score from VEP multi-transcript format like '0.145&.&.&.&.&.'
        """
        if not raw_value or raw_value in ['.', '', 'unknown']:
            return 0.0
        
        # Handle multi-transcript values separated by &
        values = raw_value.split('&')
        valid_scores = []
        
        for value in values:
            value = value.strip()
            if value and value != '.' and value != '':
                try:
                    score = float(value)
                    
                    # Validate score range based on type
                    if score_type in ['revel', 'alphamissense'] and (score < 0.0 or score > 1.0):
                        continue
                    elif score_type == 'cadd' and score < 0:
                        continue
                    elif score_type == 'gnomad' and (score < 0.0 or score > 1.0):
                        continue
                    else:
                        valid_scores.append(score)
                        
                except (ValueError, TypeError):
                    continue
        
        if not valid_scores:
            return 0.0
        
        # Return strategy based on score type
        if score_type == 'gnomad':
            return min(valid_scores)  # Most conservative frequency
        else:
            return max(valid_scores)  # Most pathogenic/deleterious score
    
    def _extract_revel_from_csq(self, csq_value):
        """ENHANCED: Extract REVEL score from CSQ - Multi-transcript parser"""
        if not self.csq_parser:
            return 0.0
        
        # Get REVEL value (might be multi-transcript like "0.145&.&.&.&.&.")
        raw_value = self.csq_parser.get_field_value(csq_value.split(',')[0], 'REVEL_score')
        return self._extract_best_score_from_multivalue(raw_value, 'revel')
    
    def _extract_cadd_from_csq(self, csq_value):
        """ENHANCED: Extract CADD score from CSQ - Multi-transcript parser"""
        if not self.csq_parser:
            return 0.0
        
        # Try multiple CADD field names
        for field_name in ['CADD_phred', 'CADD_PHRED', 'CADD']:
            raw_value = self.csq_parser.get_field_value(csq_value.split(',')[0], field_name)
            if raw_value and raw_value not in ['.', '', 'unknown']:
                return self._extract_best_score_from_multivalue(raw_value, 'cadd')
        
        return 0.0
    
    def _extract_alphamissense_from_csq(self, csq_value):
        """ENHANCED: Extract AlphaMissense score from CSQ - Multi-transcript parser"""
        if not self.csq_parser:
            return 0.0
        
        first_annotation = csq_value.split(',')[0]
        
        # Try the correct field names based on your VCF structure
        field_candidates = [
            'AlphaMissense_am_pathogenicity',  # Position 106 from your VCF
            'AlphaMissense',                   # Position 105 from your VCF  
            'am_pathogenicity',               # Alternative name
        ]
        
        for field_name in field_candidates:
            raw_value = self.csq_parser.get_field_value(first_annotation, field_name)
            if raw_value and raw_value not in ['.', '', 'unknown']:
                score = self._extract_best_score_from_multivalue(raw_value, 'alphamissense')
                if score > 0:
                    return score
        
        return 0.0
    
    def _extract_clinvar_from_csq(self, csq_value):
        """ENHANCED: Extract ClinVar significance from CSQ - Multi-transcript parser"""
        if not self.csq_parser:
            return 'unknown'
        
        raw_value = self.csq_parser.get_field_value(csq_value.split(',')[0], 'ClinVar_CLNSIG')
        
        if raw_value and raw_value not in ['.', '', 'unknown']:
            # Handle multi-transcript values like "Benign&.&.&."
            values = raw_value.split('&')
            
            # Priority order for clinical significance (higher = more important)
            significance_priority = {
                'pathogenic': 10, 'likely_pathogenic': 9, 'pathogenic/likely_pathogenic': 8,
                'drug_response': 7, 'risk_factor': 6, 'uncertain_significance': 5,
                'conflicting_classifications_of_pathogenicity': 4, 'likely_benign': 3,
                'benign': 2, 'benign/likely_benign': 1, 'other': 1, '.': 0
            }
            
            best_significance = 'unknown'
            best_priority = 0
            
            for value in values:
                value = value.strip().lower()
                if value and value != '.':
                    # Handle common variations
                    if 'pathogenic' in value and 'likely' not in value:
                        value = 'pathogenic'
                    elif 'likely_pathogenic' in value:
                        value = 'likely_pathogenic'
                    elif 'benign' in value and 'likely' not in value:
                        value = 'benign'
                    elif 'likely_benign' in value:
                        value = 'likely_benign'
                    elif 'uncertain' in value:
                        value = 'uncertain_significance'
                    elif 'conflicting' in value:
                        value = 'conflicting_classifications_of_pathogenicity'
                    
                    priority = significance_priority.get(value, 0)
                    if priority > best_priority:
                        best_priority = priority
                        best_significance = value.replace('_', ' ').title()
            
            return best_significance
        
        return 'unknown'
    
    def _extract_gnomad_af_from_csq(self, csq_value):
        """ENHANCED: Extract gnomAD allele frequency from CSQ - Multi-transcript parser"""
        if not self.csq_parser:
            return 1.0
        
        # Try multiple possible field names
        for field_name in ['gnomADe_AF', 'gnomADg_AF', 'AF']:
            raw_value = self.csq_parser.get_field_value(csq_value.split(',')[0], field_name)
            if raw_value and raw_value not in ['.', '', 'unknown']:
                freq = self._extract_best_score_from_multivalue(raw_value, 'gnomad')
                if freq < 1.0:  # Valid frequency found
                    return freq
        
        return 1.0  # Conservative assumption if not found
    
    def _calculate_variant_score(self, variant, gene, csq_value):
        """Calculate variant clinical significance score"""
        score = 0
        
        # ClinVar significance (highest weight)
        clinvar = self._extract_clinvar_from_csq(csq_value)
        if 'pathogenic' in clinvar.lower() and 'conflicting' not in clinvar.lower():
            score += 40
        elif 'likely_pathogenic' in clinvar.lower():
            score += 30
        elif 'uncertain' in clinvar.lower():
            score += 10
        elif 'benign' in clinvar.lower():
            score -= 20
        
        # Consequence severity
        consequence = self.csq_parser.extract_consequence_from_csq(csq_value) if self.csq_parser else 'unknown'
        if any(c in consequence.lower() for c in ['stop_gained', 'frameshift', 'splice_donor', 'splice_acceptor']):
            score += 25
        elif 'missense' in consequence.lower():
            score += 15
        elif 'synonymous' in consequence.lower():
            score += 5
        
        # Population frequency
        gnomad_af = self._extract_gnomad_af_from_csq(csq_value)
        if gnomad_af < 0.00001:
            score += 20
        elif gnomad_af < 0.0001:
            score += 15
        elif gnomad_af < 0.001:
            score += 10
        elif gnomad_af > 0.01:
            score -= 15
        
        # Pathogenicity predictions
        revel = self._extract_revel_from_csq(csq_value)
        if revel >= 0.75:
            score += 15
        elif revel >= 0.5:
            score += 10
        
        alphamissense = self._extract_alphamissense_from_csq(csq_value)
        if alphamissense >= 0.564:
            score += 10
        elif alphamissense <= 0.34:
            score -= 5
        
        cadd = self._extract_cadd_from_csq(csq_value)
        if cadd >= 30:
            score += 10
        elif cadd >= 25:
            score += 5
        
        return max(score, 0)

# Report generator class
class ComprehensiveReportGenerator:
    """Generate comprehensive ranked reports"""
    
    def __init__(self, analyzer, sample_id, output_dir):
        self.analyzer = analyzer
        self.sample_id = sample_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_reports(self):
        """Generate all comprehensive reports"""
        print(f"📄 Generating comprehensive reports for {self.sample_id}...")
        self._generate_detailed_variants()
        self._generate_interactive_html()
        print(f"✅ All reports generated in: {self.output_dir}")
    
    def _generate_detailed_variants(self):
        """Generate detailed CSV of all variants"""
        csv_file = self.output_dir / f"{self.sample_id}_ENHANCED_VARIANTS.csv"
        
        # Prepare data for CSV
        csv_data = []
        for result in self.analyzer.variant_results:
            gene_info = result['gene_info']
            csv_data.append({
                'Gene': result['gene'],
                'Chromosome': result['chromosome'],
                'Position': result['position'],
                'Ref': result['ref'],
                'Alt': result['alt'],
                'Condition': gene_info['condition'],
                'Evidence_Tier': gene_info['evidence_tier'],
                'Actionability': gene_info['actionability'],
                'Combined_Score': gene_info['total_score'] + result['variant_score'],
                'Variant_Score': result['variant_score'],
                'Specialty': gene_info['specialty'],
                'Source': gene_info['source'],
                'Consequence': result['consequence'],
                'ClinVar_Significance': result['clinvar_sig'],
                'gnomAD_AF': result['gnomad_af'],
                'REVEL_Score': result['revel_score'],
                'AlphaMissense_Score': result['alphamissense_score'],
                'CADD_Score': result['cadd_score']
            })
        
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_file, index=False)
        
        print(f"   ✅ Enhanced CSV: {csv_file}")
        
        # Print ENHANCED validation statistics
        print(f"   📊 ENHANCED Score extraction:")
        revel_count = len(df[df['REVEL_Score'] > 0])
        alphamissense_count = len(df[df['AlphaMissense_Score'] > 0])
        cadd_count = len(df[df['CADD_Score'] > 0])
        
        print(f"      REVEL scores: {revel_count} (was 3)")
        print(f"      AlphaMissense scores: {alphamissense_count} (was 3)")
        print(f"      CADD scores: {cadd_count} (was 3)")
        
        if revel_count > 3 or cadd_count > 3:
            print("      🚀 IMPROVEMENT CONFIRMED! Multi-transcript parser working!")
        else:
            print("      ⚠️  No improvement - check VEP annotation or field names")
    
    def _generate_interactive_html(self):
        """Generate interactive HTML report"""
        html_file = self.output_dir / f"{self.sample_id}_ENHANCED_ANALYSIS.html"
        
        # Get top findings
        top_findings = self.analyzer.variant_results[:20]
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ENHANCED: Multi-Transcript Gene Analysis - {self.sample_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .enhanced {{ border-left: 5px solid #27ae60; background-color: #f1f8e9; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .score-high {{ background-color: #ffebee; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 ENHANCED: Multi-Transcript Clinical Gene Analysis</h1>
        <h2>Sample: {self.sample_id}</h2>
        <p>Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Genes Analyzed: {len(self.analyzer.gene_db.genes):,} | Variants Found: {len(self.analyzer.variant_results):,}</p>
        <p style="color: #2ecc71;"><strong>✅ Multi-Transcript '&' Parser Enhanced!</strong></p>
    </div>
    
    <div class="section enhanced">
        <h3>🎯 Enhanced Score Extraction Results</h3>
        <table>
            <tr><th>Score Type</th><th>Count</th><th>Improvement</th></tr>
            <tr>
                <td>REVEL</td>
                <td>{len([r for r in self.analyzer.variant_results if r['revel_score'] > 0])}</td>
                <td>{"🚀 IMPROVED!" if len([r for r in self.analyzer.variant_results if r['revel_score'] > 0]) > 3 else "Same"}</td>
            </tr>
            <tr>
                <td>CADD</td>
                <td>{len([r for r in self.analyzer.variant_results if r['cadd_score'] > 0])}</td>
                <td>{"🚀 IMPROVED!" if len([r for r in self.analyzer.variant_results if r['cadd_score'] > 0]) > 3 else "Same"}</td>
            </tr>
            <tr>
                <td>ClinVar</td>
                <td>{len([r for r in self.analyzer.variant_results if r['clinvar_sig'] not in ['unknown', '.']])}</td>
                <td>Enhanced priority classification</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h3>🏆 Top Clinical Findings</h3>
        <table>
            <tr><th>Gene</th><th>Condition</th><th>Actionability</th><th>REVEL</th><th>CADD</th><th>ClinVar</th></tr>
"""
        
        for result in top_findings:
            gene_info = result['gene_info']
            
            html_content += f"""
            <tr>
                <td><strong>{result['gene']}</strong></td>
                <td>{gene_info['condition']}</td>
                <td>{gene_info['actionability'].replace('_', ' ')}</td>
                <td>{result['revel_score']:.3f}</td>
                <td>{result['cadd_score']:.1f}</td>
                <td>{result['clinvar_sig']}</td>
            </tr>"""
        
        html_content += """
        </table>
    </div>
</body>
</html>
"""
        
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"   ✅ Enhanced HTML report: {html_file}")

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='ENHANCED: Multi-Transcript Clinical Gene Analysis')
    parser.add_argument('--sample-id', required=True, help='Sample ID')
    parser.add_argument('--vcf-file', required=True, help='Path to VEP-annotated VCF file')
    parser.add_argument('--output-dir', help='Output directory', default='.')
    parser.add_argument('--min-score', type=int, default=20, help='Minimum clinical significance score')
    
    args = parser.parse_args()
    
    print("🚀 ENHANCED: MULTI-TRANSCRIPT CLINICAL GENE ANALYSIS")
    print("=" * 65)
    print(f"Sample: {args.sample_id}")
    print(f"Annotated VCF: {args.vcf_file}")
    print(f"Output Directory: {args.output_dir}")
    print()
    print("🔧 ENHANCED FEATURES:")
    print("   ✅ Multi-transcript '&' separated value parsing")
    print("   ✅ Best score extraction from all transcript positions")
    print("   ✅ Improved ClinVar significance prioritization")
    print("   ✅ Enhanced score range validation")
    print()
    
    # Initialize comprehensive gene database
    gene_db = ComprehensiveGeneDatabase()
    
    # Initialize ENHANCED variant analyzer
    analyzer = ComprehensiveVariantAnalyzer(gene_db)
    
    # Analyze variants with enhanced parser
    success = analyzer.analyze_annotated_vcf(args.vcf_file, args.sample_id)
    
    if not success:
        print("❌ Analysis failed")
        return 1
    
    # Generate comprehensive reports
    report_generator = ComprehensiveReportGenerator(analyzer, args.sample_id, args.output_dir)
    report_generator.generate_all_reports()
    
    print("\n🎉 ENHANCED ANALYSIS COMPLETE!")
    
    # Enhanced score extraction summary
    if analyzer.variant_results:
        revel_count = len([r for r in analyzer.variant_results if r['revel_score'] > 0])
        alphamissense_count = len([r for r in analyzer.variant_results if r['alphamissense_score'] > 0])
        cadd_count = len([r for r in analyzer.variant_results if r['cadd_score'] > 0])
        clinvar_count = len([r for r in analyzer.variant_results if r['clinvar_sig'] not in ['unknown', '.']])
        
        print(f"\n🎯 ENHANCED SCORE EXTRACTION RESULTS:")
        print(f"   • REVEL scores: {revel_count} (was 3) {'🚀 IMPROVED!' if revel_count > 3 else ''}")
        print(f"   • AlphaMissense scores: {alphamissense_count} (was 3) {'🚀 IMPROVED!' if alphamissense_count > 3 else ''}")
        print(f"   • CADD scores: {cadd_count} (was 3) {'🚀 IMPROVED!' if cadd_count > 3 else ''}")
        print(f"   • ClinVar annotations: {clinvar_count} (enhanced prioritization)")
        
        if revel_count > 3 or cadd_count > 3:
            print("\n🎉 SUCCESS: Multi-transcript parser is extracting more scores!")
        else:
            print("\n⚠️  No improvement detected - may need VEP plugin fixes")
    
    print(f"\n📁 Enhanced results in: {args.output_dir}")
    
    return 0

if __name__ == "__main__":
    exit(main())
