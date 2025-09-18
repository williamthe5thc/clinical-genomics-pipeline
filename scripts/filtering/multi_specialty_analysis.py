#!/usr/bin/env python3
"""
Multi-Specialty Analysis Wrapper - Backward Compatibility
Calls enhanced_acmg_classifier.py with proper argument mapping

Author: Clinical Genomics Pipeline
Version: 4.0 - Compatibility Wrapper
Date: September 2025
"""

import os
import sys
import argparse
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description='Multi-Specialty Analysis - Compatibility Wrapper for Enhanced ACMG Classifier',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('vcf_file', help='VEP-annotated VCF file')
    parser.add_argument('sample_id', help='Sample identifier')
    parser.add_argument('--tier', default='comprehensive', 
                       choices=['comprehensive', 'focused', 'neurodevelopmental'],
                       help='Analysis tier (legacy - all use comprehensive now)')
    parser.add_argument('--output_dir', default=None, help='Output directory')
    parser.add_argument('--min-score', type=int, default=20, help='Minimum clinical significance score')
    
    args = parser.parse_args()
    
    # Determine output file
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = os.path.join(args.output_dir, f"{args.sample_id}_enhanced_acmg_results.txt")
    else:
        output_file = f"{args.sample_id}_enhanced_acmg_results.txt"
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    enhanced_classifier = os.path.join(script_dir, 'enhanced_acmg_classifier.py')
    
    # Build command for enhanced ACMG classifier
    cmd = [
        'python3',
        enhanced_classifier,
        '--vcf-file', args.vcf_file,
        '--sample-id', args.sample_id,
        '--output-dir', args.output_dir if args.output_dir else os.getcwd(),
        '--min-score', str(args.min_score)
    ]
    
    logger.info(f"Calling Enhanced ACMG Classifier for {args.sample_id}")
    logger.info(f"Analysis tier: {args.tier} (using comprehensive gene panels)")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Command: {' '.join(cmd)}")
    
    try:
        # Run the enhanced ACMG classifier
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        logger.info("Enhanced ACMG classification completed successfully")
        if result.stdout:
            print(result.stdout)
        
        # Create legacy output files for backward compatibility
        if args.output_dir:
            # Create summary JSON for compatibility
            summary_file = os.path.join(args.output_dir, f"{args.sample_id}_analysis_summary.json")
            html_report = os.path.join(args.output_dir, f"{args.sample_id}_multi_specialty_report.html")
            
            # Generate compatibility files
            create_compatibility_files(args.sample_id, output_file, summary_file, html_report)
            
            logger.info(f"Compatibility files created:")
            logger.info(f"  - Summary: {summary_file}")
            logger.info(f"  - HTML Report: {html_report}")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Enhanced ACMG classifier failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        logger.error(f"Command that failed: {' '.join(cmd)}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

def create_compatibility_files(sample_id, enhanced_results_file, summary_file, html_report):
    """Create compatibility files that match the old output format"""
    import json
    from datetime import datetime
    
    # Read enhanced results
    try:
        with open(enhanced_results_file, 'r') as f:
            enhanced_content = f.read()
    except:
        enhanced_content = "Enhanced ACMG analysis completed"
    
    # Create summary JSON
    summary_data = {
        "sample_id": sample_id,
        "analysis_date": datetime.now().isoformat(),
        "pipeline_version": "4.0",
        "analysis_type": "Enhanced ACMG/AMP Multi-Specialty",
        "gene_panels": 22,
        "total_genes": 790,
        "enhanced_features": [
            "ACMG/AMP evidence-based classification",
            "Clinical significance scoring (0-100)",
            "790 genes across 22 medical specialties", 
            "Pathogenic/Likely Pathogenic variant identification",
            "Comprehensive pathogenicity prediction integration"
        ],
        "output_files": {
            "enhanced_results": enhanced_results_file,
            "html_report": html_report
        }
    }
    
    with open(summary_file, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    # Create HTML report
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Clinical Genomics Analysis - {sample_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 20px; border-radius: 10px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .enhanced {{ background-color: #e8f5e8; border-left: 4px solid #4CAF50; }}
        .pathogenic {{ background-color: #ffebee; border-left: 4px solid #f44336; }}
        .info {{ background-color: #e3f2fd; border-left: 4px solid #2196F3; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Clinical Genomics Analysis Report</h1>
        <h2>Sample: {sample_id}</h2>
        <p>Enhanced ACMG/AMP Analysis - Pipeline v4.0</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section enhanced">
        <h3>🧬 Enhanced Pipeline Capabilities</h3>
        <ul>
            <li><strong>790 unique genes</strong> across 22 medical specialties</li>
            <li><strong>ACMG/AMP evidence-based classification</strong> with detailed evidence codes</li>
            <li><strong>Clinical significance scoring</strong> (0-100 scale)</li>
            <li><strong>Pathogenic/Likely Pathogenic</strong> variant identification</li>
            <li><strong>Comprehensive pathogenicity predictions</strong> integration</li>
        </ul>
    </div>
    
    <div class="section info">
        <h3>📊 Analysis Details</h3>
        <p><strong>Detailed results:</strong> {enhanced_results_file}</p>
        <p><strong>Analysis includes:</strong></p>
        <ul>
            <li>Primary specialties: CDLS, Cardiac, Oncology</li>
            <li>Neurological: Neurology, Epilepsy, Autism Spectrum, Movement Disorders</li>
            <li>Sensory: Hearing Loss, Ophthalmology, Reproductive</li>
            <li>Organ Systems: Skeletal, Connective Tissue, Hematology, Nephrology, Pulmonology, Immunology, Dermatology</li>
            <li>Metabolic: Endocrinology, Pharmacogenomics, Mitochondrial, Lysosomal Storage, Metabolic</li>
        </ul>
    </div>
    
    <div class="section pathogenic">
        <h3>⚠️ IMPORTANT - Research Use Only</h3>
        <p><strong>This is a RESEARCH-GRADE pipeline for clinical guidance only.</strong></p>
        <ul>
            <li>All findings require clinical validation before medical decisions</li>
            <li>Use results to guide clinical testing strategy, not for diagnosis</li>
            <li>Consult clinical genetics professionals for interpretation</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>📋 Enhanced Results Summary</h3>
        <pre style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px;">
{enhanced_content[:2000] if len(enhanced_content) > 2000 else enhanced_content}
        </pre>
        {f'<p><em>... (results truncated, see full file: {enhanced_results_file})</em></p>' if len(enhanced_content) > 2000 else ''}
    </div>
</body>
</html>
    """
    
    with open(html_report, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    sys.exit(main())
