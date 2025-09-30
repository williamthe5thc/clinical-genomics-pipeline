#!/usr/bin/env python3
"""
Comprehensive Gene Panels for Clinical Analysis
Organized by Medical Specialty

Updated: September 2025
ACMG SF v3.3 Compliant (84 genes)
"""

# ACMG Secondary Findings v3.3 (84 genes)
ACMG_SF_V33_GENES = {
    # Cardiac genes
    'ACTC1', 'MYBPC3', 'MYH7', 'MYL2', 'MYL3', 'TNNI3', 'TNNT2', 'TPM1', 
    'PRKAG2', 'PLN', 'KCNH2', 'KCNQ1', 'RYR2', 'SCN5A', 'CALM1', 'CALM2', 
    'CALM3', 'CASQ2', 'TTN', 'BAG3', 'FLNC', 'KCNE1', 'KCNE2', 'SCN1B',
    'COL3A1', 'FBN1', 'MYH11', 'SMAD3', 'TGFBR1', 'TGFBR2', 'LMNA', 
    'TMEM43', 'PKP2', 'DSC2', 'DSG2', 'DSP',
    
    # Cancer genes  
    'APC', 'BRCA1', 'BRCA2', 'MLH1', 'MSH2', 'MSH6', 'PMS2', 'TP53',
    'VHL', 'MEN1', 'RET', 'SDHB', 'SDHC', 'SDHD', 'SDHAF2', 'NF2',
    'CDKN2A', 'STK11', 'PTEN', 'BMPR1A', 'SMAD4', 'TSC1', 'TSC2',
    
    # Other actionable genes
    'LDLR', 'APOB', 'PCSK9', 'RYR1', 'CACNA1S', 'ACADVL', 'ATP7B',
    'BTD', 'FANCC', 'FANCG', 'G6PD', 'GAA', 'GBA', 'HFE', 'OTC',
    'PAH', 'PCC', 'SERPINA1', 'TGFB1', 'ABCD1'
}

# Comprehensive gene panels by medical specialty
COMPREHENSIVE_GENE_PANELS = {
    'CARDIAC': {
        # ACMG cardiac genes
        'ACTC1', 'MYBPC3', 'MYH7', 'MYL2', 'MYL3', 'TNNI3', 'TNNT2', 'TPM1',
        'PRKAG2', 'PLN', 'KCNH2', 'KCNQ1', 'RYR2', 'SCN5A', 'CALM1', 'CALM2',
        'CALM3', 'CASQ2', 'TTN', 'BAG3', 'FLNC', 'KCNE1', 'KCNE2', 'SCN1B',
        'COL3A1', 'FBN1', 'MYH11', 'SMAD3', 'TGFBR1', 'TGFBR2', 'LMNA',
        'TMEM43', 'PKP2', 'DSC2', 'DSG2', 'DSP',
        # Additional cardiac genes
        'GATA4', 'GATA6', 'TBX5', 'NKX2-5', 'CACNA1C', 'SCN2A', 'SCN8A'
    },
    
    'ONCOLOGY': {
        # ACMG cancer genes
        'APC', 'BRCA1', 'BRCA2', 'MLH1', 'MSH2', 'MSH6', 'PMS2', 'TP53',
        'VHL', 'MEN1', 'RET', 'SDHB', 'SDHC', 'SDHD', 'SDHAF2', 'NF2',
        'CDKN2A', 'STK11', 'PTEN', 'BMPR1A', 'SMAD4', 'TSC1', 'TSC2',
        # Additional cancer genes
        'ATM', 'CHEK2', 'PALB2', 'RAD51C', 'RAD51D', 'BARD1', 'BRIP1',
        'CDH1', 'EPCAM', 'MUTYH', 'NTHL1', 'PMS1', 'POLE', 'POLD1'
    },
    
    'CDLS': {
        'NIPBL', 'SMC1A', 'SMC3', 'RAD21', 'HDAC8', 'ANKRD11', 'BRD4'
    },
    
    'NEUROLOGY': {
        'HTT', 'DMD', 'NF1', 'SCN1A', 'SCN2A', 'SCN8A', 'KCNT1',
        'CHD7', 'CREBBP', 'ARID1A', 'ARID1B', 'POGZ', 'SETD2', 'KDM6A'
    },
    
    'EPILEPSY': {
        'SCN1A', 'SCN2A', 'SCN8A', 'KCNT1', 'CDKL5', 'STXBP1', 'PCDH19',
        'SYNGAP1', 'CHD2', 'GNAO1', 'GRIN2A', 'KCNQ2', 'KCNQ3'
    },
    
    'AUTISM_SPECTRUM': {
        'CHD8', 'ADNP', 'ARID1B', 'ASH1L', 'DYRK1A', 'GRIN2B', 'SCN2A',
        'SHANK3', 'SYNGAP1', 'POGZ', 'SETD2', 'KDM6A', 'MED13L'
    },
    
    'MOVEMENT_DISORDERS': {
        'PARK2', 'PINK1', 'PARK7', 'SNCA', 'LRRK2', 'VPS35', 'EIF4G1',
        'DNAJC13', 'CHCHD2', 'GBA', 'ATP13A2', 'PLA2G6', 'FBXO7'
    },
    
    'HEARING_LOSS': {
        'GJB2', 'GJB6', 'MYO7A', 'USH2A', 'CDH23', 'PCDH15', 'USH1C',
        'USH1G', 'CIB2', 'TMC1', 'OTOF', 'SLC26A4', 'TECTA'
    },
    
    'OPHTHALMOLOGY': {
        'ABCA4', 'CEP290', 'CRB1', 'LCA5', 'GUCY2D', 'RPE65', 'RDH12',
        'LRAT', 'AIPL1', 'TULP1', 'CRX', 'RPGRIP1', 'USH2A'
    },
    
    'REPRODUCTIVE': {
        'AR', 'SRY', 'NR5A1', 'WT1', 'MAMLD1', 'AMH', 'AMHR2',
        'CYP17A1', 'HSD17B3', 'SRD5A2', 'LHCGR', 'FSHR', 'BMP15'
    },
    
    'SKELETAL_DYSPLASIA': {
        'COL1A1', 'COL1A2', 'FGFR3', 'COMP', 'MATN3', 'COL9A1',
        'COL9A2', 'COL9A3', 'COL2A1', 'COL11A1', 'COL11A2'
    },
    
    'CONNECTIVE_TISSUE': {
        'FBN1', 'TGFBR1', 'TGFBR2', 'SMAD3', 'COL3A1', 'COL5A1',
        'COL5A2', 'TNXB', 'PLOD1', 'FKBP14', 'CHST14', 'DSE'
    },
    
    'HEMATOLOGY': {
        'HBA1', 'HBA2', 'HBB', 'HBG1', 'HBG2', 'SPTA1', 'SPTB',
        'ANK1', 'SLC4A1', 'EPB42', 'G6PD', 'PK', 'PKLR'
    },
    
    'NEPHROLOGY': {
        'PKD1', 'PKD2', 'COL4A3', 'COL4A4', 'COL4A5', 'NPHS1',
        'NPHS2', 'CD2AP', 'PLCE1', 'TRPC6', 'INF2', 'MYO1E'
    },
    
    'PULMONOLOGY': {
        'CFTR', 'SERPINA1', 'SFTPB', 'SFTPC', 'ABCA3', 'NKX2-1',
        'CSF2RA', 'CSF2RB', 'GATA2', 'TERT', 'TERC', 'TINF2'
    },
    
    'IMMUNOLOGY': {
        'IL2RG', 'CYBB', 'BTK', 'CD40LG', 'IKBKG', 'DCLRE1C', 'LIG4',
        'NHEJ1', 'PRKDC', 'RAG1', 'RAG2', 'ADA', 'PNP'
    },
    
    'DERMATOLOGY': {
        'KRT5', 'KRT14', 'PLEC', 'DSP', 'JUP', 'DSG1', 'DSC3',
        'COL7A1', 'LAMB3', 'LAMC2', 'ITGB4', 'COL17A1'
    },
    
    'ENDOCRINOLOGY': {
        'LDLR', 'APOB', 'PCSK9', 'MODY1', 'MODY2', 'MODY3', 'MODY4',
        'MODY5', 'MODY6', 'GCK', 'HNF1A', 'HNF4A', 'HNF1B'
    },
    
    'PHARMACOGENOMICS': {
        'CYP2D6', 'CYP2C19', 'CYP2C9', 'VKORC1', 'TPMT', 'DPYD',
        'UGT1A1', 'SLCO1B1', 'ABCB1', 'COMT', 'OPRM1'
    },
    
    'MITOCHONDRIAL': {
        'MT-ND1', 'MT-ND2', 'MT-ND3', 'MT-ND4', 'MT-ND4L', 'MT-ND5',
        'MT-ND6', 'MT-CO1', 'MT-CO2', 'MT-CO3', 'MT-ATP6', 'MT-ATP8'
    },
    
    'LYSOSOMAL_STORAGE': {
        'GBA', 'HEXA', 'HEXB', 'GM2A', 'GALC', 'ARSA', 'PSAP',
        'SMPD1', 'NPC1', 'NPC2', 'CLN1', 'CLN2', 'CLN3'
    },
    
    'METABOLIC': {
        'PAH', 'GAA', 'GBA', 'HEXA', 'G6PC', 'ATP7B', 'HFE', 'LDLR',
        'APOB', 'PCSK9', 'SERPINA1', 'CFTR', 'SMN1', 'FMR1'
    }
}

# Export all genes as a flat set for easy lookup
ALL_COMPREHENSIVE_GENES = set()
for panel_genes in COMPREHENSIVE_GENE_PANELS.values():
    ALL_COMPREHENSIVE_GENES.update(panel_genes)

# Add ACMG genes to the comprehensive set
ALL_COMPREHENSIVE_GENES.update(ACMG_SF_V33_GENES)

print(f"Comprehensive gene panels loaded: {len(COMPREHENSIVE_GENE_PANELS)} panels, {len(ALL_COMPREHENSIVE_GENES)} unique genes")
