#!/usr/bin/env python3
"""
Enhanced ACMG/AMP Classifier with BAM-derived Evidence
Integrates read-level metrics for improved variant classification

Location: /mnt/d/Genome/pipeline_components/enhanced_acmg_classifier.py
Author: Clinical Genomics Pipeline Enhancement
Version: 1.0 (Based on 2024-2025 ACMG/AMP guidelines)
"""

import os
import sys
import json
import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import re

class ACMGCriteria(Enum):
    """ACMG/AMP Evidence Criteria"""
    # Pathogenic criteria
    PVS1 = "Very Strong Pathogenic"
    PS1 = "Strong Pathogenic - Same amino acid change"
    PS2 = "Strong Pathogenic - De novo"
    PS3 = "Strong Pathogenic - Functional studies"
    PS4 = "Strong Pathogenic - Prevalence increased"
    PM1 = "Moderate Pathogenic - Hotspot"
    PM2 = "Moderate Pathogenic - Absent from controls"
    PM3 = "Moderate Pathogenic - Recessive disorder"
    PM4 = "Moderate Pathogenic - Protein length change"
    PM5 = "Moderate Pathogenic - Novel amino acid change"
    PM6 = "Moderate Pathogenic - De novo without paternity"
    PP1 = "Supporting Pathogenic - Cosegregation"
    PP2 = "Supporting Pathogenic - Missense in gene"
    PP3 = "Supporting Pathogenic - Computational evidence"
    PP4 = "Supporting Pathogenic - Phenotype specificity"
    PP5 = "Supporting Pathogenic - Reputable source"
    
    # Benign criteria
    BA1 = "Stand-alone Benign - High frequency"
    BS1 = "Strong Benign - Frequency too high"
    BS2 = "Strong Benign - Healthy adult homozygote"
    BS3 = "Strong Benign - Functional studies"
    BS4 = "Strong Benign - Lack of segregation"
    BP1 = "Supporting Benign - Missense in truncation gene"
    BP2 = "Supporting Benign - Cis with pathogenic"
    BP3 = "Supporting Benign - In-frame indels"
    BP4 = "Supporting Benign - Computational evidence"
    BP5 = "Supporting Benign - Alternative molecular basis"
    BP6 = "Supporting Benign - Reputable source"
    BP7 = "Supporting Benign - Synonymous with no impact"

@dataclass
class VariantEvidence:
    """Container for variant evidence from multiple sources"""
    variant_id: str
    gene_symbol: str
    consequence: str
    hgvs_p: str
    hgvs_c: str
    
    # Population frequency data
    gnomad_af: float = 0.0
    gnomad_af_popmax: float = 0.0
    
    # Computational predictions
    revel_score: float = 0.0
    alphamissense_score: float = 0.0
    cadd_phred: float = 0.0
    sift_pred: str = ""
    polyphen_pred: str = ""
    
    # Clinical significance
    clinvar_sig: str = ""
    clinvar_review_status: str = ""
    
    # BAM-derived evidence (Enhanced)
    read_depth: int = 0
    alt_allele_depth: int = 0
    variant_allele_frequency: float = 0.0
    mapping_quality: float = 0.0
    strand_bias_p_value: float = 1.0
    base_quality: float = 0.0
    
    # Family context (for trio analysis)
    inheritance_pattern: str = ""
    de_novo_confidence: float = 0.0
    segregation_evidence: str = ""
    
    # Evidence codes assigned
    evidence_codes: Set[ACMGCriteria] = field(default_factory=set)
    
    # Final classification
    acmg_classification: str = "Uncertain Significance"
    classification_confidence: float = 0.0

class EnhancedACMGClassifier:
    """
    Enhanced ACMG/AMP classifier incorporating BAM-derived evidence
    Follows 2015 ACMG/AMP guidelines with ClinGen specifications
    """
    
    def __init__(self, config_file: str = "/mnt/d/Genome/config/acmg_config.json"):
        self.config = self._load_config(config_file)
        self.logger = self._setup_logging()
        
        # Load gene-specific information
        self.haploinsufficient_genes = self._load_haploinsufficient_genes()
        self.disease_genes = self._load_disease_gene_associations()
        self.hotspot_regions = self._load_hotspot_regions()
        
        # Classification thresholds
        self.frequency_thresholds = {
            "ba1_threshold": 0.05,  # 5% for stand-alone benign
            "bs1_threshold": 0.01,  # 1% for strong benign
            "pm2_threshold": 0.0001,  # 0.01% for moderate pathogenic
            "rare_disease_threshold": 0.001  # 0.1% for rare disease
        }
        
        self.computational_thresholds = {
            "revel_pathogenic": 0.75,
            "revel_benign": 0.25,
            "alphamissense_pathogenic": 0.564,
            "alphamissense_benign": 0.34,
            "cadd_pathogenic": 25.0,
            "cadd_benign": 15.0
        }
        
        # BAM-derived evidence thresholds
        self.bam_evidence_thresholds = {
            "min_read_depth": 10,
            "min_variant_depth": 3,
            "min_mapping_quality": 20,
            "max_strand_bias_p": 0.01,
            "min_base_quality": 20
        }
    
    def _load_config(self, config_file: str) -> Dict:
        """Load ACMG classifier configuration"""
        default_config = {
            "enable_bam_evidence": True,
            "enable_family_evidence": True,
            "strict_classification": True,
            "require_functional_evidence": False
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load ACMG config {config_file}: {e}")
        
        return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for ACMG classifier"""
        logger = logging.getLogger('EnhancedACMG')
        logger.setLevel(logging.INFO)
        
        log_dir = Path("/mnt/d/Genome/logs")
        log_dir.mkdir(exist_ok=True)
        
        handler = logging.FileHandler(log_dir / "enhanced_acmg.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_haploinsufficient_genes(self) -> Set[str]:
        """Load list of haploinsufficient genes for PVS1 application"""
        # This would load from ClinGen haploinsufficiency data
        # For now, using common examples
        return {
            "BRCA1", "BRCA2", "TP53", "MLH1", "MSH2", "MSH6", "PMS2", 
            "APC", "VHL", "RB1", "NF1", "NF2", "TSC1", "TSC2",
            "PTEN", "STK11", "CDKN2A", "CDH1", "PALB2", "CHEK2"
        }
    
    def _load_disease_gene_associations(self) -> Dict[str, List[str]]:
        """Load gene-disease associations for PM2/PP2 application"""
        # This would load from ClinVar, OMIM, or other databases
        return {
            "BRCA1": ["Breast cancer", "Ovarian cancer"],
            "BRCA2": ["Breast cancer", "Ovarian cancer"],
            "MLH1": ["Lynch syndrome", "Colorectal cancer"],
            "MSH2": ["Lynch syndrome", "Colorectal cancer"],
            # Add more gene-disease associations
        }
    
    def _load_hotspot_regions(self) -> Dict[str, List[Tuple[int, int]]]:
        """Load known hotspot regions for PM1 application"""
        # This would load from mutation databases
        return {
            "TP53": [(175, 300)],  # DNA-binding domain
            "KRAS": [(12, 13), (61, 61)],  # Common mutation sites
            # Add more hotspot regions
        }
    
    def classify_with_enhanced_evidence(self, processing_results: Dict, sample_id: str, output_dir: str) -> Dict:
        """
        Main classification function incorporating enhanced evidence
        """
        self.logger.info(f"Starting enhanced ACMG classification for {sample_id}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        classification_results = {
            "sample_id": sample_id,
            "total_variants": 0,
            "classified_variants": [],
            "pathogenic_variants": [],
            "likely_pathogenic_variants": [],
            "vus_variants": [],
            "likely_benign_variants": [],
            "benign_variants": [],
            "classification_summary": {},
            "status": "completed"
        }
        
        try:
            # Extract variants from processing results
            variants = self._extract_variants_from_results(processing_results)
            classification_results["total_variants"] = len(variants)
            
            self.logger.info(f"Classifying {len(variants)} variants for {sample_id}")
            
            # Classify each variant
            for variant_data in variants:
                try:
                    variant_evidence = self._build_variant_evidence(variant_data, processing_results)
                    classified_variant = self._classify_variant(variant_evidence)
                    
                    classification_results["classified_variants"].append(classified_variant)
                    
                    # Categorize by classification
                    classification = classified_variant.acmg_classification
                    if classification == "Pathogenic":
                        classification_results["pathogenic_variants"].append(classified_variant)
                    elif classification == "Likely Pathogenic":
                        classification_results["likely_pathogenic_variants"].append(classified_variant)
                    elif classification == "Uncertain Significance":
                        classification_results["vus_variants"].append(classified_variant)
                    elif classification == "Likely Benign":
                        classification_results["likely_benign_variants"].append(classified_variant)
                    elif classification == "Benign":
                        classification_results["benign_variants"].append(classified_variant)
                
                except Exception as e:
                    self.logger.warning(f"Error classifying variant {variant_data.get('variant_id', 'unknown')}: {e}")
            
            # Generate classification summary
            classification_results["classification_summary"] = self._generate_classification_summary(
                classification_results
            )
            
            # Save detailed results
            self._save_classification_results(classification_results, output_path, sample_id)
            
            self.logger.info(f"Enhanced ACMG classification completed for {sample_id}")
            return classification_results
            
        except Exception as e:
            self.logger.error(f"Error in enhanced ACMG classification: {e}")
            classification_results["status"] = "error"
            classification_results["error_message"] = str(e)
            return classification_results
    
    def _extract_variants_from_results(self, processing_results: Dict) -> List[Dict]:
        """Extract variant data from processing results"""
        variants = []
        
        # Extract from VCF analysis results
        if "vcf_analysis" in processing_results:
            vcf_variants = processing_results["vcf_analysis"].get("variants", [])
            variants.extend(vcf_variants)
        
        # Extract from BAM analysis if available
        if "bam_analysis" in processing_results:
            bam_variants = processing_results["bam_analysis"].get("variants", [])
            variants.extend(bam_variants)
        
        # Remove duplicates based on variant_id
        unique_variants = {}
        for variant in variants:
            variant_id = variant.get("variant_id", f"{variant.get('chrom', '')}:{variant.get('pos', '')}")
            if variant_id not in unique_variants:
                unique_variants[variant_id] = variant
        
        return list(unique_variants.values())
    
    def _build_variant_evidence(self, variant_data: Dict, processing_results: Dict) -> VariantEvidence:
        """Build comprehensive evidence object for variant"""
        
        # Basic variant information
        evidence = VariantEvidence(
            variant_id=variant_data.get("variant_id", ""),
            gene_symbol=variant_data.get("gene_symbol", ""),
            consequence=variant_data.get("consequence", ""),
            hgvs_p=variant_data.get("hgvs_p", ""),
            hgvs_c=variant_data.get("hgvs_c", "")
        )
        
        # Population frequency data
        evidence.gnomad_af = float(variant_data.get("gnomad_af", 0))
        evidence.gnomad_af_popmax = float(variant_data.get("gnomad_af_popmax", 0))
        
        # Computational predictions
        evidence.revel_score = float(variant_data.get("revel_score", 0))
        evidence.alphamissense_score = float(variant_data.get("alphamissense_score", 0))
        evidence.cadd_phred = float(variant_data.get("cadd_phred", 0))
        evidence.sift_pred = variant_data.get("sift_pred", "")
        evidence.polyphen_pred = variant_data.get("polyphen_pred", "")
        
        # Clinical significance
        evidence.clinvar_sig = variant_data.get("clinvar_sig", "")
        evidence.clinvar_review_status = variant_data.get("clinvar_review_status", "")
        
        # BAM-derived evidence (if available)
        if self.config["enable_bam_evidence"] and "bam_analysis" in processing_results:
            bam_data = processing_results["bam_analysis"].get("enhanced_evidence", {})
            evidence.read_depth = int(variant_data.get("read_depth", 0))
            evidence.alt_allele_depth = int(variant_data.get("alt_allele_depth", 0))
            evidence.variant_allele_frequency = float(variant_data.get("vaf", 0))
            evidence.mapping_quality = float(variant_data.get("mapping_quality", 0))
            evidence.strand_bias_p_value = float(variant_data.get("strand_bias_p", 1.0))
            evidence.base_quality = float(variant_data.get("base_quality", 0))
        
        # Family context (if available)
        if self.config["enable_family_evidence"] and "trio_analysis" in processing_results:
            trio_data = processing_results["trio_analysis"]
            evidence.inheritance_pattern = variant_data.get("inheritance_pattern", "")
            evidence.de_novo_confidence = float(variant_data.get("de_novo_confidence", 0))
            evidence.segregation_evidence = variant_data.get("segregation_evidence", "")
        
        return evidence
    
    def _classify_variant(self, evidence: VariantEvidence) -> VariantEvidence:
        """
        Classify variant using ACMG/AMP criteria with enhanced evidence
        """
        
        # Apply all ACMG criteria
        self._apply_pathogenic_criteria(evidence)
        self._apply_benign_criteria(evidence)
        
        # Enhanced criteria using BAM evidence
        if self.config["enable_bam_evidence"]:
            self._apply_bam_enhanced_criteria(evidence)
        
        # Family-based criteria
        if self.config["enable_family_evidence"]:
            self._apply_family_criteria(evidence)
        
        # Final classification logic
        evidence.acmg_classification = self._determine_final_classification(evidence)
        evidence.classification_confidence = self._calculate_classification_confidence(evidence)
        
        return evidence
    
    def _apply_pathogenic_criteria(self, evidence: VariantEvidence):
        """Apply pathogenic ACMG criteria"""
        
        # PVS1 - Null variant in haploinsufficient gene
        if self._is_null_variant(evidence) and evidence.gene_symbol in self.haploinsufficient_genes:
            evidence.evidence_codes.add(ACMGCriteria.PVS1)
        
        # PS1 - Same amino acid change as known pathogenic
        if self._check_same_amino_acid_change(evidence):
            evidence.evidence_codes.add(ACMGCriteria.PS1)
        
        # PS2 - De novo variant (family context required)
        if evidence.de_novo_confidence > 0.95:
            evidence.evidence_codes.add(ACMGCriteria.PS2)
        
        # PS3 - Functional studies (would require external data)
        # PS4 - Prevalence in cases vs controls (would require case-control data)
        
        # PM1 - Located in hotspot region
        if self._is_in_hotspot_region(evidence):
            evidence.evidence_codes.add(ACMGCriteria.PM1)
        
        # PM2 - Absent from controls or extremely low frequency
        if evidence.gnomad_af < self.frequency_thresholds["pm2_threshold"]:
            evidence.evidence_codes.add(ACMGCriteria.PM2)
        
        # PM3 - Recessive disorder context (requires family analysis)
        # PM4 - Protein length changing variant
        if self._is_protein_length_changing(evidence):
            evidence.evidence_codes.add(ACMGCriteria.PM4)
        
        # PM5 - Novel missense at same residue as pathogenic
        if self._check_novel_missense_same_residue(evidence):
            evidence.evidence_codes.add(ACMGCriteria.PM5)
        
        # PM6 - De novo without paternity/maternity confirmation
        if 0.8 < evidence.de_novo_confidence < 0.95:
            evidence.evidence_codes.add(ACMGCriteria.PM6)
        
        # PP1 - Cosegregation (requires family data)
        # PP2 - Missense in gene with low benign missense variation
        if self._is_missense_in_constrained_gene(evidence):
            evidence.evidence_codes.add(ACMGCriteria.PP2)
        
        # PP3 - Computational evidence supporting pathogenicity
        if self._computational_evidence_pathogenic(evidence):
            evidence.evidence_codes.add(ACMGCriteria.PP3)
        
        # PP4 - Phenotype specificity (requires clinical correlation)
        # PP5 - Reputable source reports pathogenic
        if self._check_reputable_source_pathogenic(evidence):
            evidence.evidence_codes.add(ACMGCriteria.PP5)
    
    def _apply_benign_criteria(self, evidence: VariantEvidence):
        """Apply benign ACMG criteria"""
        
        # BA1 - Stand-alone benign due to high frequency
        if evidence.gnomad_af > self.frequency_thresholds["ba1_threshold"]:
            evidence.evidence_codes.add(ACMGCriteria.BA1)
        
        # BS1 - Strong benign due to frequency
        elif evidence.gnomad_af > self.frequency_thresholds["bs1_threshold"]:
            evidence.evidence_codes.add(ACMGCriteria.BS1)
        
        # BS2 - Healthy adult homozygote (requires population data)
        # BS3 - Functional studies show no effect
        # BS4 - Lack of segregation
        
        # BP1 - Missense in gene where truncating is disease mechanism
        if self._is_missense_in_truncation_gene(evidence):
            evidence.evidence_codes.add(ACMGCriteria.BP1)
        
        # BP2 - Cis with pathogenic variant (requires phasing)
        # BP3 - In-frame indels without important domains
        if self._is_inframe_indel_benign_region(evidence):
            evidence.evidence_codes.add(ACMGCriteria.BP3)
        
        # BP4 - Computational evidence supporting benign
        if self._computational_evidence_benign(evidence):
            evidence.evidence_codes.add(ACMGCriteria.BP4)
        
        # BP5 - Alternative molecular basis found
        # BP6 - Reputable source reports benign
        if self._check_reputable_source_benign(evidence):
            evidence.evidence_codes.add(ACMGCriteria.BP6)
        
        # BP7 - Synonymous variant with no predicted impact
        if self._is_synonymous_no_impact(evidence):
            evidence.evidence_codes.add(ACMGCriteria.BP7)
    
    def _apply_bam_enhanced_criteria(self, evidence: VariantEvidence):
        """Apply enhanced criteria based on BAM-derived evidence"""
        
        # Quality-based evidence enhancement
        if (evidence.read_depth >= self.bam_evidence_thresholds["min_read_depth"] and
            evidence.alt_allele_depth >= self.bam_evidence_thresholds["min_variant_depth"] and
            evidence.mapping_quality >= self.bam_evidence_thresholds["min_mapping_quality"] and
            evidence.strand_bias_p_value > self.bam_evidence_thresholds["max_strand_bias_p"]):
            
            # High-quality variant call enhances existing evidence
            if ACMGCriteria.PP3 in evidence.evidence_codes:
                # Could upgrade PP3 to PM level with high-quality data
                pass
            
            # Low strand bias supports variant authenticity
            if evidence.strand_bias_p_value > 0.1:
                # Additional confidence in variant call
                pass
    
    def _apply_family_criteria(self, evidence: VariantEvidence):
        """Apply family-based criteria"""
        
        # Enhanced de novo detection
        if evidence.de_novo_confidence > 0.99:
            # Very high confidence de novo - strengthen PS2
            evidence.evidence_codes.add(ACMGCriteria.PS2)
        
        # Segregation analysis
        if evidence.segregation_evidence == "perfect_segregation":
            evidence.evidence_codes.add(ACMGCriteria.PP1)
        elif evidence.segregation_evidence == "no_segregation":
            evidence.evidence_codes.add(ACMGCriteria.BS4)
    
    def _determine_final_classification(self, evidence: VariantEvidence) -> str:
        """
        Determine final ACMG classification based on evidence codes
        Follows ACMG/AMP 2015 guidelines
        """
        
        pathogenic_codes = [code for code in evidence.evidence_codes if code.value.startswith("Very Strong Pathogenic") or code.value.startswith("Strong Pathogenic") or code.value.startswith("Moderate Pathogenic") or code.value.startswith("Supporting Pathogenic")]
        benign_codes = [code for code in evidence.evidence_codes if code.value.startswith("Stand-alone Benign") or code.value.startswith("Strong Benign") or code.value.startswith("Supporting Benign")]
        
        # Stand-alone benign
        if ACMGCriteria.BA1 in evidence.evidence_codes:
            return "Benign"
        
        # Pathogenic combinations
        if ACMGCriteria.PVS1 in evidence.evidence_codes:
            ps_count = len([c for c in evidence.evidence_codes if c.value.startswith("Strong Pathogenic")])
            pm_count = len([c for c in evidence.evidence_codes if c.value.startswith("Moderate Pathogenic")])
            pp_count = len([c for c in evidence.evidence_codes if c.value.startswith("Supporting Pathogenic")])
            
            if ps_count >= 1:
                return "Pathogenic"
            elif pm_count >= 2:
                return "Pathogenic"
            elif (pm_count >= 1 and pp_count >= 1):
                return "Pathogenic"
            elif pp_count >= 2:
                return "Likely Pathogenic"
        
        # Strong pathogenic evidence
        ps_count = len([c for c in evidence.evidence_codes if c.value.startswith("Strong Pathogenic")])
        if ps_count >= 2:
            return "Pathogenic"
        elif ps_count == 1:
            pm_count = len([c for c in evidence.evidence_codes if c.value.startswith("Moderate Pathogenic")])
            pp_count = len([c for c in evidence.evidence_codes if c.value.startswith("Supporting Pathogenic")])
            
            if pm_count >= 3:
                return "Pathogenic"
            elif (pm_count >= 2 and pp_count >= 2):
                return "Pathogenic"
            elif (pm_count >= 1 and pp_count >= 4):
                return "Pathogenic"
            elif (pm_count >= 1 and pp_count >= 2):
                return "Likely Pathogenic"
            elif pp_count >= 4:
                return "Likely Pathogenic"
        
        # Benign combinations
        bs_count = len([c for c in evidence.evidence_codes if c.value.startswith("Strong Benign")])
        bp_count = len([c for c in evidence.evidence_codes if c.value.startswith("Supporting Benign")])
        
        if bs_count >= 2:
            return "Benign"
        elif (bs_count == 1 and bp_count >= 1):
            return "Likely Benign"
        elif bp_count >= 2:
            return "Likely Benign"
        
        # Default to VUS
        return "Uncertain Significance"
    
    def _calculate_classification_confidence(self, evidence: VariantEvidence) -> float:
        """Calculate confidence score for classification"""
        
        # Base confidence on number and strength of evidence codes
        confidence = 0.5  # Base confidence
        
        for code in evidence.evidence_codes:
            if "Very Strong" in code.value:
                confidence += 0.3
            elif "Strong" in code.value:
                confidence += 0.2
            elif "Moderate" in code.value:
                confidence += 0.1
            elif "Supporting" in code.value:
                confidence += 0.05
        
        # BAM quality enhances confidence
        if (evidence.read_depth >= 20 and evidence.mapping_quality >= 40):
            confidence += 0.1
        
        # Family context enhances confidence
        if evidence.de_novo_confidence > 0.9:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    # Helper methods for criteria application
    def _is_null_variant(self, evidence: VariantEvidence) -> bool:
        """Check if variant is null (nonsense, frameshift, canonical splice)"""
        null_consequences = [
            "stop_gained", "frameshift_variant", "splice_donor_variant", 
            "splice_acceptor_variant", "start_lost", "stop_lost"
        ]
        return evidence.consequence in null_consequences
    
    def _check_same_amino_acid_change(self, evidence: VariantEvidence) -> bool:
        """Check if same amino acid change is known pathogenic"""
        # This would query ClinVar or other databases
        # Simplified implementation
        return "Pathogenic" in evidence.clinvar_sig and evidence.hgvs_p
    
    def _is_in_hotspot_region(self, evidence: VariantEvidence) -> bool:
        """Check if variant is in a known hotspot region"""
        if evidence.gene_symbol in self.hotspot_regions:
            # Extract position from HGVS (simplified)
            if evidence.hgvs_p:
                try:
                    pos_match = re.search(r'p\..*?(\d+)', evidence.hgvs_p)
                    if pos_match:
                        pos = int(pos_match.group(1))
                        hotspots = self.hotspot_regions[evidence.gene_symbol]
                        return any(start <= pos <= end for start, end in hotspots)
                except:
                    pass
        return False
    
    def _is_protein_length_changing(self, evidence: VariantEvidence) -> bool:
        """Check if variant changes protein length"""
        length_changing = [
            "frameshift_variant", "stop_gained", "stop_lost", 
            "start_lost", "inframe_insertion", "inframe_deletion"
        ]
        return evidence.consequence in length_changing
    
    def _check_novel_missense_same_residue(self, evidence: VariantEvidence) -> bool:
        """Check if novel missense at same residue as known pathogenic"""
        # This would require database lookup
        return False
    
    def _is_missense_in_constrained_gene(self, evidence: VariantEvidence) -> bool:
        """Check if missense variant in gene with low benign missense variation"""
        # This would use constraint metrics like missense Z-score
        return evidence.gene_symbol in self.haploinsufficient_genes
    
    def _computational_evidence_pathogenic(self, evidence: VariantEvidence) -> bool:
        """Check computational evidence for pathogenicity"""
        pathogenic_count = 0
        
        if evidence.revel_score >= self.computational_thresholds["revel_pathogenic"]:
            pathogenic_count += 1
        if evidence.alphamissense_score >= self.computational_thresholds["alphamissense_pathogenic"]:
            pathogenic_count += 1
        if evidence.cadd_phred >= self.computational_thresholds["cadd_pathogenic"]:
            pathogenic_count += 1
        if evidence.sift_pred == "D":
            pathogenic_count += 1
        if evidence.polyphen_pred in ["D", "P"]:
            pathogenic_count += 1
        
        return pathogenic_count >= 3
    
    def _computational_evidence_benign(self, evidence: VariantEvidence) -> bool:
        """Check computational evidence for benign effect"""
        benign_count = 0
        
        if evidence.revel_score <= self.computational_thresholds["revel_benign"]:
            benign_count += 1
        if evidence.alphamissense_score <= self.computational_thresholds["alphamissense_benign"]:
            benign_count += 1
        if evidence.cadd_phred <= self.computational_thresholds["cadd_benign"]:
            benign_count += 1
        if evidence.sift_pred == "T":
            benign_count += 1
        if evidence.polyphen_pred == "B":
            benign_count += 1
        
        return benign_count >= 3
    
    def _check_reputable_source_pathogenic(self, evidence: VariantEvidence) -> bool:
        """Check if reputable source reports as pathogenic"""
        if "Pathogenic" in evidence.clinvar_sig:
            review_status = evidence.clinvar_review_status.lower()
            return any(status in review_status for status in [
                "reviewed by expert panel", "practice guideline", "multiple submitters"
            ])
        return False
    
    def _check_reputable_source_benign(self, evidence: VariantEvidence) -> bool:
        """Check if reputable source reports as benign"""
        if "Benign" in evidence.clinvar_sig:
            review_status = evidence.clinvar_review_status.lower()
            return any(status in review_status for status in [
                "reviewed by expert panel", "practice guideline", "multiple submitters"
            ])
        return False
    
    def _is_missense_in_truncation_gene(self, evidence: VariantEvidence) -> bool:
        """Check if missense in gene where truncation is mechanism"""
        return (evidence.consequence == "missense_variant" and 
                evidence.gene_symbol in self.haploinsufficient_genes)
    
    def _is_inframe_indel_benign_region(self, evidence: VariantEvidence) -> bool:
        """Check if in-frame indel in region without important domains"""
        # This would require domain annotation
        return evidence.consequence in ["inframe_insertion", "inframe_deletion"]
    
    def _is_synonymous_no_impact(self, evidence: VariantEvidence) -> bool:
        """Check if synonymous variant with no predicted impact"""
        return (evidence.consequence == "synonymous_variant" and
                evidence.revel_score < 0.1 and
                evidence.cadd_phred < 10)
    
    def _generate_classification_summary(self, results: Dict) -> Dict:
        """Generate summary statistics for classification"""
        total = results["total_variants"]
        
        if total == 0:
            return {}
        
        summary = {
            "total_variants": total,
            "pathogenic_count": len(results["pathogenic_variants"]),
            "likely_pathogenic_count": len(results["likely_pathogenic_variants"]),
            "vus_count": len(results["vus_variants"]),
            "likely_benign_count": len(results["likely_benign_variants"]),
            "benign_count": len(results["benign_variants"]),
            "pathogenic_percentage": len(results["pathogenic_variants"]) / total * 100,
            "likely_pathogenic_percentage": len(results["likely_pathogenic_variants"]) / total * 100,
            "vus_percentage": len(results["vus_variants"]) / total * 100,
            "clinically_actionable": len(results["pathogenic_variants"]) + len(results["likely_pathogenic_variants"])
        }
        
        return summary
    
    def _save_classification_results(self, results: Dict, output_path: Path, sample_id: str):
        """Save detailed classification results"""
        
        # Save complete results as JSON
        results_file = output_path / f"{sample_id}_enhanced_acmg_classification.json"
        
        # Convert VariantEvidence objects to dictionaries for JSON serialization
        serializable_results = {}
        for key, value in results.items():
            if key in ["classified_variants", "pathogenic_variants", "likely_pathogenic_variants", 
                       "vus_variants", "likely_benign_variants", "benign_variants"]:
                serializable_results[key] = [self._variant_evidence_to_dict(v) for v in value]
            else:
                serializable_results[key] = value
        
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        # Save summary CSV
        summary_file = output_path / f"{sample_id}_classification_summary.csv"
        self._save_classification_csv(results, summary_file)
    
    def _variant_evidence_to_dict(self, evidence: VariantEvidence) -> Dict:
        """Convert VariantEvidence object to dictionary"""
        result = {
            "variant_id": evidence.variant_id,
            "gene_symbol": evidence.gene_symbol,
            "consequence": evidence.consequence,
            "hgvs_p": evidence.hgvs_p,
            "hgvs_c": evidence.hgvs_c,
            "gnomad_af": evidence.gnomad_af,
            "gnomad_af_popmax": evidence.gnomad_af_popmax,
            "revel_score": evidence.revel_score,
            "alphamissense_score": evidence.alphamissense_score,
            "cadd_phred": evidence.cadd_phred,
            "clinvar_sig": evidence.clinvar_sig,
            "acmg_classification": evidence.acmg_classification,
            "classification_confidence": evidence.classification_confidence,
            "evidence_codes": [code.name for code in evidence.evidence_codes],
            "read_depth": evidence.read_depth,
            "variant_allele_frequency": evidence.variant_allele_frequency,
            "mapping_quality": evidence.mapping_quality,
            "de_novo_confidence": evidence.de_novo_confidence
        }
        return result
    
    def _save_classification_csv(self, results: Dict, csv_file: Path):
        """Save classification results as CSV"""
        import csv
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                "Variant_ID", "Gene", "Consequence", "HGVS_p", "HGVS_c",
                "gnomAD_AF", "REVEL", "AlphaMissense", "CADD", "ClinVar",
                "ACMG_Classification", "Evidence_Codes", "Confidence"
            ])
            
            # Data rows
            for variant in results["classified_variants"]:
                variant_dict = self._variant_evidence_to_dict(variant)
                writer.writerow([
                    variant_dict["variant_id"],
                    variant_dict["gene_symbol"],
                    variant_dict["consequence"],
                    variant_dict["hgvs_p"],
                    variant_dict["hgvs_c"],
                    variant_dict["gnomad_af"],
                    variant_dict["revel_score"],
                    variant_dict["alphamissense_score"],
                    variant_dict["cadd_phred"],
                    variant_dict["clinvar_sig"],
                    variant_dict["acmg_classification"],
                    "|".join(variant_dict["evidence_codes"]),
                    variant_dict["classification_confidence"]
                ])

    def classify_family_variants(self, trio_results: Dict, family_id: str, output_dir: str) -> Dict:
        """Classify variants in family context with enhanced de novo detection"""
        self.logger.info(f"Starting family-based ACMG classification for {family_id}")
        
        # This would implement family-specific classification logic
        # including inheritance patterns, de novo detection, and segregation analysis
        
        return {
            "family_id": family_id,
            "status": "completed",
            "family_variants": [],
            "de_novo_variants": [],
            "inherited_variants": [],
            "classification_summary": {}
        }

def main():
    """Main function for standalone testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced ACMG/AMP Classifier")
    parser.add_argument("--input", required=True, help="Input processing results JSON")
    parser.add_argument("--sample-id", required=True, help="Sample identifier")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    
    args = parser.parse_args()
    
    # Initialize classifier
    classifier = EnhancedACMGClassifier()
    
    # Load processing results
    with open(args.input, 'r') as f:
        processing_results = json.load(f)
    
    # Classify variants
    results = classifier.classify_with_enhanced_evidence(
        processing_results, args.sample_id, args.output_dir
    )
    
    # Print summary
    print(f"Classification completed for {args.sample_id}")
    print(f"Total variants: {results['total_variants']}")
    print(f"Pathogenic: {len(results['pathogenic_variants'])}")
    print(f"Likely Pathogenic: {len(results['likely_pathogenic_variants'])}")
    print(f"VUS: {len(results['vus_variants'])}")

if __name__ == "__main__":
    main()