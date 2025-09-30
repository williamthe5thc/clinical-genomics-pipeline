"""
Enhanced Clinical Genomics Pipeline Components
BAM Integration and Advanced Analysis Modules

This package contains the enhanced modules for BAM-level analysis:
- bam_processor: Enhanced BAM processing with quality control
- enhanced_acmg_classifier: ACMG/AMP classification with BAM evidence
- trio_analyzer: Advanced de novo detection and family analysis
- quality_reporter: Clinical-grade reporting and quality metrics
- structural_variant_analyzer: Manta-based SV detection
- cnv_analyzer: CNVkit/GATK-gCNV copy number analysis

Author: Clinical Genomics Pipeline Enhancement
Version: 1.0 (2024-2025 Research-Based Implementation)
"""

__version__ = "1.0"
__author__ = "Clinical Genomics Pipeline Enhancement"

# Import main classes for easy access
try:
    from .bam_processor import EnhancedBAMProcessor
    from .enhanced_acmg_classifier import EnhancedACMGClassifier
    from .trio_analyzer import TrioAnalyzer
    from .quality_reporter import EnhancedQualityReporter
    from .structural_variant_analyzer import StructuralVariantAnalyzer
    from .cnv_analyzer import CNVAnalyzer
    
    __all__ = [
        'EnhancedBAMProcessor',
        'EnhancedACMGClassifier', 
        'TrioAnalyzer',
        'EnhancedQualityReporter',
        'StructuralVariantAnalyzer',
        'CNVAnalyzer'
    ]
    
except ImportError as e:
    print(f"Warning: Some pipeline components not yet implemented: {e}")
    print("Please replace placeholder files with actual implementations")
    
    __all__ = []

print("Enhanced Clinical Genomics Pipeline Components")
print("Please replace placeholder files with actual implementations from artifacts")
