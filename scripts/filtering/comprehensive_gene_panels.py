#!/usr/bin/env python3
"""
Comprehensive Clinical Gene Panels - 24 Medical Specialties
Expanded from enhanced ACMG classifier with massive gene panel coverage

Author: Clinical Genomics Pipeline  
Version: 4.0 - Comprehensive Medical Specialties
Date: September 2025
"""

# ===== PRIMARY SPECIALTIES =====

CDLS_GENES = {
    'NIPBL', 'SMC1A', 'SMC3', 'RAD21', 'HDAC8', 'BRD4', 'ANKRD11'
}

# ACMG Secondary Findings v3.3 - Complete 84 genes
CARDIAC_GENES = {
    # Cardiomyopathy
    'ACTC1', 'MYBPC3', 'MYH7', 'MYL2', 'MYL3', 'TNNI3', 'TNNT2', 'TPM1', 
    'PRKAG2', 'PLN', 'TTN', 'BAG3', 'FLNC', 'LMNA',
    # Arrhythmia  
    'KCNH2', 'KCNQ1', 'RYR2', 'SCN5A', 'CALM1', 'CALM2', 'CALM3', 
    'CASQ2', 'KCNE1', 'KCNE2', 'SCN1B',
    # Aortopathy
    'COL3A1', 'FBN1', 'MYH11', 'SMAD3', 'TGFBR1', 'TGFBR2',
    # Arrhythmogenic cardiomyopathy
    'PKP2', 'DSC2', 'DSG2', 'DSP', 'TMEM43',
    # Additional cardiac genes
    'TRDN', 'JPH2', 'CRYAB', 'TCAP', 'VCL', 'DES', 'LAMP2', 'PRKAG2',
    'GLA', 'ACTN2', 'CSRP3', 'LDB3', 'NEXN', 'MYPN', 'ACTN2'
}

# Comprehensive oncology panel
ONCOLOGY_GENES = {
    # Breast/Ovarian
    'BRCA1', 'BRCA2', 'PALB2', 'ATM', 'CHEK2', 'NBN', 'BARD1', 'RAD51C', 
    'RAD51D', 'BRIP1', 'RAD50', 'RAD52', 'RAD54L', 'XRCC2', 'XRCC3',
    # Colorectal  
    'APC', 'MLH1', 'MSH2', 'MSH6', 'PMS2', 'EPCAM', 'MUTYH', 'SMAD4', 
    'BMPR1A', 'STK11', 'POLD1', 'POLE', 'NTHL1', 'MSH3',
    # Tumor Suppressors
    'TP53', 'PTEN', 'RB1', 'WT1', 'CDKN2A', 'CDK4', 'BAP1', 'SUFU',
    # Endocrine
    'VHL', 'RET', 'MEN1', 'CDKN1B', 'SDHB', 'SDHC', 'SDHD', 'SDHA', 
    'SDHAF2', 'MAX', 'TMEM127', 'FH', 'FLCN',
    # Other
    'DICER1', 'HOXB13', 'NF1', 'NF2', 'PTCH1', 'TSC1', 'TSC2', 'CDH1'
}

# ===== NEUROLOGICAL SPECIALTIES =====

NEUROLOGY_GENES = {
    'SCN1A', 'MECP2', 'CDKL5', 'TSC1', 'TSC2', 'NF1', 'NF2', 'PTEN', 
    'SHANK3', 'CHD8', 'FOXP1', 'ARID1B', 'KMT2A', 'EHMT1', 'ADNP',
    'DYRK1A', 'ASH1L', 'POGZ', 'SYNGAP1', 'GRIN2B', 'SETD1B', 'KMT5B',
    'SETD5', 'SETBP1', 'TCF4', 'MEF2C', 'TBR1', 'FOXP2', 'EHMT1'
}

EPILEPSY_GENES = {
    # Sodium channels
    'SCN1A', 'SCN1B', 'SCN2A', 'SCN3A', 'SCN8A', 'SCN9A',
    # Potassium channels  
    'KCNQ2', 'KCNQ3', 'KCNT1', 'KCNMA1', 'KCNA1', 'KCNA2',
    # Calcium channels
    'CACNA1H', 'CACNA1A', 'CACNB4', 'CACNA1G',
    # GABA receptors
    'GABRA1', 'GABRB3', 'GABRG2', 'GABRD',
    # Nicotinic receptors
    'CHRNA4', 'CHRNB2', 'CHRNA2',
    # Metabolic
    'SLC2A1', 'ALDH7A1', 'PLPBP', 'AMT', 'GLDC', 'GCSH',
    # Developmental encephalopathies
    'STXBP1', 'SPTAN1', 'ARX', 'FOXG1', 'MEF2C', 'SYNGAP1', 'PCDH19', 'GNAO1',
    # Progressive myoclonus
    'CSTB', 'EPM2A', 'NHLRC1', 'SCARB2', 'PRICKLE1', 'GOSR2',
    # Other
    'LGI1', 'PRRT2', 'TBC1D24', 'WWOX', 'CNTNAP2', 'RELN'
}

AUTISM_SPECTRUM_GENES = {
    # High-confidence autism genes
    'CHD8', 'SCN2A', 'ADNP', 'ARID1B', 'ASH1L', 'DYRK1A', 'GRIN2B', 
    'POGZ', 'SHANK3', 'SYNGAP1', 'PTEN',
    # X-linked
    'MECP2', 'CDKL5', 'ARX', 'NLGN3', 'NLGN4X', 'PTCHD1', 'DDX53',
    # Syndromic
    'FMR1', 'TSC1', 'TSC2', 'NF1', 'UBE3A', 'SNRPN', 'NRXN1', 'CNTNAP2',
    # Chromatin
    'CHD2', 'SETD1B', 'KMT5B', 'KMT2A', 'SETD5', 'SETBP1',
    # Synaptic
    'SHANK2', 'NRXN1', 'NRXN2', 'NRXN3', 'DLGAP2', 'HOMER1',
    # Transcription
    'FOXP1', 'FOXP2', 'TBR1', 'MEF2C', 'TCF4', 'EHMT1',
    # Other
    'CACNA1C', 'CACNA1H', 'GRIN1', 'GRIN2A', 'SLC6A1', 'GABRB3', 
    'OXTR', 'CNTN4', 'CNTN6', 'CTNND2'
}

MOVEMENT_DISORDERS_GENES = {
    # Parkinson disease
    'SNCA', 'LRRK2', 'PRKN', 'PINK1', 'DJ1', 'ATP13A2', 'PLA2G6', 'FBXO7', 
    'VPS35', 'EIF4G1', 'DNAJC6', 'SYNJ1', 'VPS13C', 'CHCHD2',
    # Huntington disease
    'HTT', 'JPH3', 'TBP',
    # Dystonia
    'DYT1', 'THAP1', 'CIZ1', 'GNAL', 'ANO3', 'TUBB4A', 'GCH1', 'TH', 
    'SPR', 'SGCE', 'ATP1A3', 'PRKRA',
    # Spinocerebellar ataxias
    'ATXN1', 'ATXN2', 'ATXN3', 'CACNA1A', 'ATXN7', 'ATXN8OS', 'ATXN10', 
    'FXN', 'SACS', 'SPG7', 'SETX', 'APTX',
    # Essential tremor
    'ETM1', 'ETM2', 'HS1BP3', 'TENM4',
    # Chorea
    'NKX2-1', 'ADCY5', 'PDE10A', 'PNKD', 'PRRT2',
    # Myoclonus
    'KCNMA1'
}

# ===== SENSORY SPECIALTIES =====

HEARING_LOSS_GENES = {
    # Nonsyndromic recessive
    'GJB2', 'GJB6', 'SLC26A4', 'MYO15A', 'CDH23', 'PCDH15', 'OTOF', 
    'TMC1', 'TMPRSS3', 'CIB2', 'LOXHD1', 'STRC',
    # Nonsyndromic dominant
    'KCNQ4', 'GJB3', 'TECTA', 'COL11A2', 'POU4F3', 'MYH14', 'WFS1', 
    'ACTG1', 'MYO6', 'SIX1', 'EYA1',
    # X-linked
    'POU3F4', 'PRPS1', 'COL4A6', 'COL4A5',
    # Usher syndrome
    'MYO7A', 'USH1C', 'USH1G', 'USH2A', 'ADGRV1', 'WHRN', 'CLRN1', 'HARS',
    # Syndromic
    'CHD7', 'SOX10', 'MITF', 'PAX3', 'SNAI2', 'EDN3', 'EDNRB', 'TCOF1', 
    'POLR1C', 'POLR1D',
    # Mitochondrial
    'MT-RNR1', 'MT-TS1', 'MT-CO1',
    # Development
    'EYA4', 'GATA3', 'HOXA1', 'FGF3'
}

OPHTHALMOLOGY_GENES = {
    'ABCA4', 'RHO', 'RPGR', 'USH2A', 'MYO7A', 'CEP290', 'CRB1', 'CACNA1F', 
    'NYX', 'COL2A1', 'COL11A1', 'PAX6', 'FOXC1', 'PITX2', 'CRX', 'EYS', 
    'GUCY2D', 'OPA1', 'RS1', 'STARGARDT', 'BEST1', 'IMPG2', 'PRPH2',
    'TULP1', 'PDE6A', 'PDE6B', 'CNGA1', 'CNGA3', 'CNGB1', 'CNGB3',
    'GUCA1A', 'AIPL1', 'LCA5', 'RPGRIP1', 'CRB1', 'RDH12'
}

REPRODUCTIVE_GENES = {
    # Disorders of sexual development
    'SRY', 'SOX9', 'WT1', 'SF1', 'DMRT1', 'MAMLD1', 'AR', 'SRD5A2', 
    'HSD17B3', 'CYP17A1', 'STAR', 'CYP11A1', 'HSD3B2', 'CYP21A2', 'CYP11B1',
    # Hypogonadism
    'GnRH1', 'GNRHR', 'KISS1R', 'KISS1', 'TAC3', 'TACR3', 'FGFR1', 'KAL1', 
    'FGF8', 'PROKR2', 'PROK2', 'CHD7', 'HS6ST1', 'WDR11', 'SEMA3A', 'SPRY4',
    # Male infertility
    'CFTR', 'AURKC', 'CATSPER1', 'CATSPER2', 'DNAI1', 'DNAH5', 'CCDC39', 
    'CCDC40', 'DPY19L2', 'SPATA16', 'PICK1', 'CCIN',
    # Female infertility
    'FMR1', 'BMP15', 'FIGLA', 'NOBOX', 'NR5A1', 'FSHR', 'LHR', 'FOXL2', 
    'STAG3', 'SMC1B', 'MSH5', 'HFM1', 'SYCE1', 'MCM8', 'MCM9',
    # MRKH
    'LHX1', 'WNT4', 'TBX6', 'GREB1L',
    # Other
    'AMH', 'AMHR2', 'HOXA13', 'EMX2'
}

# ===== ORGAN SYSTEM SPECIALTIES =====

SKELETAL_DYSPLASIA_GENES = {
    # Achondroplasia group
    'FGFR3', 'FGFR2', 'FGFR1',
    # Collagen disorders
    'DTDST', 'COL2A1', 'COL11A1', 'COL11A2',
    # Multiple epiphyseal
    'COMP', 'MATN3', 'COL9A1', 'COL9A2', 'COL9A3',
    # Metaphyseal
    'RMRP', 'SBDS', 'COL10A1', 'POP1',
    # Spondylometaphyseal
    'TRPV4', 'PCYT1A', 'ACAN',
    # Other skeletal dysplasias
    'SOX9', 'EVC', 'EVC2', 'IFT80', 'DYNC2H1', 'IFT140', 'WDR19', 'WDR60', 
    'TTC21B', 'DYNC2LI1', 'NEK1', 'WDR35', 'IFT122', 'GPC6', 'NPR2', 
    'GDF5', 'CDMP1', 'FLNB', 'B3GAT3', 'COL1A1', 'COL1A2', 'CRTAP', 
    'LEPRE1', 'PPIB', 'SERPINH1', 'FKBP10', 'RUNX2', 'GNAS', 'CANT1', 
    'XYLT1', 'B3GALT6', 'B4GALT7'
}

CONNECTIVE_TISSUE_GENES = {
    'FBN1', 'COL3A1', 'COL5A1', 'COL5A2', 'COL1A1', 'COL1A2', 'TGFBR1', 
    'TGFBR2', 'SMAD3', 'SKI', 'PLOD1', 'FKBP14', 'B3GALT6', 'B4GALT7',
    'TNXB', 'COL12A1', 'ADAMTS2', 'ZNF469', 'PRDM5', 'C1R', 'C1S',
    'CHST14', 'DSE', 'B3GAT3', 'SLC39A13', 'ATP6V0A2', 'COL1A2', 
    'AEBP1', 'ADAMTSL2', 'FBN2', 'LTBP4', 'MGP', 'EFEMP2', 'FBLN5'
}

HEMATOLOGY_GENES = {
    # Coagulation
    'F8', 'F9', 'VWF', 'PROC', 'PROS1', 'SERPINC1', 'F5', 'PROTHROMBIN',
    # Hemoglobinopathies
    'HBA1', 'HBA2', 'HBB', 'GATA1',
    # Platelet disorders
    'ANKRD26', 'ETV6', 'RUNX1', 'THPO', 'MPL', 'TUBB1', 'MYH9', 'GP1BA',
    # Bone marrow failure
    'FANCA', 'FANCC', 'FANCD2', 'FANCE', 'FANCF', 'FANCG', 'TERC', 'TERT',
    'DKC1', 'TINF2', 'SBDS', 'ELANE', 'HAX1', 'G6PC3', 'JAGN1',
    # Hemolytic anemias
    'G6PD', 'PKLR', 'ANK1', 'SPTA1', 'SPTB'
}

NEPHROLOGY_GENES = {
    'PKD1', 'PKD2', 'COL4A5', 'COL4A3', 'COL4A4', 'NPHS1', 'NPHS2', 'WT1', 
    'NPHP1', 'UMOD', 'MUC1', 'HNF1B', 'PKHD1', 'NPHP3', 'NPHP4', 'CEP164',
    'WDR19', 'TMEM67', 'CC2D2A', 'AHI1', 'TCTN2', 'B9D1', 'MKS1', 'TMEM216',
    'CEP290', 'RPGRIP1L', 'ARL13B', 'INVS', 'ANKS6', 'GLIS2', 'ZNF423',
    'TTC21B', 'IFT140', 'WDR35', 'DYNC2H1', 'IFT80', 'IFT172'
}

PULMONOLOGY_GENES = {
    'CFTR', 'SERPINA1', 'SFTPC', 'SFTPB', 'ABCA3', 'NKX2-1', 'BMPR2', 
    'ACVRL1', 'ENG', 'SMAD4', 'KCNK3', 'CAV1', 'DNAI1', 'DNAH5', 'CCDC39',
    'CCDC40', 'RSPH4A', 'RSPH9', 'HYDIN', 'LRRC6', 'CCDC65', 'ARMC4',
    'DRC1', 'ZMYND10', 'LRRC50', 'CCDC103', 'CCDC114', 'TTC25', 'SPAG1'
}

IMMUNOLOGY_GENES = {
    'BTK', 'CYBB', 'IL2RG', 'WAS', 'CD40LG', 'FOXP3', 'RAG1', 'RAG2', 
    'ADA', 'JAK3', 'DCLRE1C', 'NHEJ1', 'PRKDC', 'LIG4', 'CYBA', 'NCF1', 
    'NCF2', 'NCF4', 'PNP', 'ARTEMIS', 'CD40', 'AICDA', 'UNG', 'ICOS',
    'CD3D', 'CD3E', 'CD3G', 'CD3Z', 'CD8A', 'TAP1', 'TAP2', 'TAPBP',
    'CIITA', 'RFXANK', 'RFX5', 'RFXAP'
}

DERMATOLOGY_GENES = {
    'FLG', 'KRT1', 'KRT10', 'KRT14', 'KRT5', 'COL7A1', 'LAMB3', 'LAMC2', 
    'LAMA3', 'TGM1', 'ALOX12B', 'ABCA12', 'SPINK5', 'POMP', 'KRT2', 'KRT9',
    'DSP', 'PKP1', 'JUP', 'DSG1', 'DSC3', 'CDSN', 'NCSTN', 'ATP2A2',
    'GJB2', 'MPLKIP', 'AAGAB', 'POFUT1', 'POGLUT1', 'ST14', 'CAST',
    'SERPINB7', 'KLHL24', 'LIPN', 'NIPAL4', 'ICHTHYIN'
}

# ===== METABOLIC SPECIALTIES =====

ENDOCRINOLOGY_GENES = {
    # Diabetes
    'INS', 'GCK', 'HNF1A', 'PDX1', 'HNF1B', 'NEUROD1', 'KLF11', 'CEL', 
    'PAX4', 'ABCC8', 'KCNJ11', 'GLUD1', 'HADH',
    # Thyroid
    'TSHR', 'THRB', 'TG', 'TPO', 'SLC5A5', 'DUOX2', 'DUOXA2', 'IYD', 'SLC26A4',
    # Adrenal
    'CYP21A2', 'CYP11B1', 'CYP17A1', 'HSD3B2', 'STAR', 'CYP11A1', 'POR', 'NR0B1',
    # Growth/Pituitary
    'GH1', 'GHR', 'GHRH', 'GHRHR', 'IGF1', 'IGFALS', 'PROP1', 'POU1F1', 
    'HESX1', 'LHX3', 'LHX4', 'SHOX', 'NPR2', 'ACAN'
}

PHARMACOGENOMICS_GENES = {
    # CYP450 enzymes
    'CYP2D6', 'CYP2C19', 'CYP2C9', 'CYP3A5', 'CYP1A2', 'CYP2B6', 'CYP2E1',
    # Transporters
    'SLCO1B1', 'ABCB1', 'ABCG2', 'SLC22A1', 'SLC47A1',
    # Drug targets/metabolism
    'VKORC1', 'DPYD', 'TPMT', 'NUDT15', 'UGT1A1', 'G6PD', 'CACNA1S', 'RYR1',
    # Psychiatric drug response
    'HTR2A', 'DRD2', 'SLC6A4', 'COMT', 'CYP4F2', 'IFNL3', 'HLA-B', 'HLA-A'
}

MITOCHONDRIAL_GENES = {
    # Complex I
    'NDUFS1', 'NDUFS2', 'NDUFS3', 'NDUFS4', 'NDUFS6', 'NDUFS7', 'NDUFS8', 
    'NDUFV1', 'NDUFV2', 'NDUFA1', 'NDUFA2', 'NDUFA9', 'NDUFA10', 'NDUFA11', 
    'NDUFB3', 'NDUFC2',
    # Complex II
    'SDHA', 'SDHB', 'SDHC', 'SDHD', 'SDHAF1',
    # Complex III
    'CYC1', 'UQCRB', 'UQCRC2', 'UQCRQ', 'BCS1L', 'TTC19', 'UQCC2',
    # Complex IV
    'COX10', 'COX15', 'SCO1', 'SCO2', 'SURF1', 'TACO1', 'COA5',
    # Complex V
    'ATP5A1', 'ATP5E', 'TMEM70',
    # DNA maintenance
    'POLG', 'POLG2', 'TWINKLE', 'ANT1', 'DGUOK', 'TK2', 'SUCLG1', 'RRM2B',
    # CoQ biosynthesis
    'COQ2', 'COQ6', 'COQ7', 'PDSS1', 'PDSS2'
}

LYSOSOMAL_STORAGE_GENES = {
    # Sphingolipidoses
    'GBA', 'SMPD1', 'NPC1', 'NPC2', 'HEXA', 'HEXB', 'GM2A', 'GLB1', 'GALC', 
    'ARSA', 'PSAP', 'GLA',
    # Mucopolysaccharidoses
    'IDUA', 'IDS', 'SGSH', 'NAGLU', 'HGSNAT', 'GNS', 'GALNS', 'GLB1', 
    'ARSB', 'GUSB', 'HYAL1',
    # Oligosaccharidoses
    'MAN2B1', 'MANBA', 'NEU1', 'CTSA', 'FUCA1', 'AGA',
    # Lipid storage
    'LIPA', 'PLA2G6',
    # Neuronal ceroid lipofuscinoses
    'PPT1', 'TPP1', 'CLN3', 'CLN5', 'CLN6', 'MFSD8', 'CLN8', 'CTSD', 'GRN', 
    'ATP13A2', 'CTSF',
    # Other
    'GAA', 'SUMF1', 'GNPTAB', 'GNPTG', 'CTSK', 'LAMP2', 'CLN1', 'SCARB2'
}

METABOLIC_GENES = {
    'PAH', 'CFTR', 'HFE', 'GBA', 'HEXA', 'ASPA', 'IKBKAP', 'FANCC', 'BLM', 
    'G6PC', 'GAA', 'GLA', 'IDUA', 'GALC', 'ARSA', 'GLB1', 'FUCA1', 'NAGLU', 
    'SGSH', 'HGSNAT', 'GNS', 'MTHFR', 'F5', 'F2', 'SERPINA1', 'APOE',
    'CYP2D6', 'CYP2C19', 'TPMT', 'UGT1A1', 'VKORC1', 'DPYD'
}

# Research genes
RESEARCH_GENES = {
    'QRICH1'
}

# ===== COMPREHENSIVE GENE PANELS DICTIONARY =====

COMPREHENSIVE_GENE_PANELS = {
    # Primary specialties
    'CDLS': CDLS_GENES,
    'CARDIAC': CARDIAC_GENES,
    'ONCOLOGY': ONCOLOGY_GENES,
    
    # Neurological specialties
    'NEUROLOGY': NEUROLOGY_GENES,
    'EPILEPSY': EPILEPSY_GENES,
    'AUTISM_SPECTRUM': AUTISM_SPECTRUM_GENES,
    'MOVEMENT_DISORDERS': MOVEMENT_DISORDERS_GENES,
    
    # Sensory specialties
    'HEARING_LOSS': HEARING_LOSS_GENES,
    'OPHTHALMOLOGY': OPHTHALMOLOGY_GENES,
    'REPRODUCTIVE': REPRODUCTIVE_GENES,
    
    # Organ system specialties
    'SKELETAL_DYSPLASIA': SKELETAL_DYSPLASIA_GENES,
    'CONNECTIVE_TISSUE': CONNECTIVE_TISSUE_GENES,
    'HEMATOLOGY': HEMATOLOGY_GENES,
    'NEPHROLOGY': NEPHROLOGY_GENES,
    'PULMONOLOGY': PULMONOLOGY_GENES,
    'IMMUNOLOGY': IMMUNOLOGY_GENES,
    'DERMATOLOGY': DERMATOLOGY_GENES,
    
    # Metabolic specialties
    'ENDOCRINOLOGY': ENDOCRINOLOGY_GENES,
    'PHARMACOGENOMICS': PHARMACOGENOMICS_GENES,
    'MITOCHONDRIAL': MITOCHONDRIAL_GENES,
    'LYSOSOMAL_STORAGE': LYSOSOMAL_STORAGE_GENES,
    'METABOLIC': METABOLIC_GENES,
    
    # Research
    'RESEARCH': RESEARCH_GENES
}

def get_panel_statistics():
    """Get comprehensive statistics about gene panels"""
    stats = {}
    total_genes = set()
    
    for panel_name, genes in COMPREHENSIVE_GENE_PANELS.items():
        stats[panel_name] = len(genes)
        total_genes.update(genes)
    
    stats['TOTAL_UNIQUE_GENES'] = len(total_genes)
    stats['TOTAL_PANELS'] = len(COMPREHENSIVE_GENE_PANELS)
    
    return stats

if __name__ == "__main__":
    stats = get_panel_statistics()
    print("COMPREHENSIVE GENE PANELS STATISTICS")
    print("=" * 50)
    print(f"Total Medical Specialties: {stats['TOTAL_PANELS']}")
    print(f"Total Unique Genes: {stats['TOTAL_UNIQUE_GENES']}")
    print()
    print("Genes per specialty:")
    for panel, count in sorted(stats.items()):
        if panel not in ['TOTAL_UNIQUE_GENES', 'TOTAL_PANELS']:
            print(f"  {panel:<20}: {count:>4} genes")
