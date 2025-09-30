#!/usr/bin/env python3
"""
Clinical Report Generator v2.0
==============================

Generates professional clinical genomics reports from multi-specialty analysis results.
Designed for clinical-grade output with comprehensive interpretation and recommendations.

Features:
- Professional HTML/PDF report generation
- ACMG/AMP classification integration
- Multi-specialty variant prioritization  
- Clinical recommendations and follow-up actions
- Family screening guidance
- Quality metrics and methodology documentation

Author: Clinical Genomics Pipeline Team
Version: 2.0
Location: /mnt/d/Genome/scripts/reporting/clinical_report_generator.py
"""

import os
import sys
import json
import pandas as pd
import argparse
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import yaml

# Base configuration
BASE_DIR = "/mnt/d/Genome"
LOGS_DIR = f"{BASE_DIR}/logs"

# Clinical significance mapping
CLINICAL_SIGNIFICANCE_MAPPING = {
    'Pathogenic': {'color': '#d32f2f', 'priority': 5, 'action': 'immediate'},
    'Likely Pathogenic': {'color': '#f57c00', 'priority': 4, 'action': 'urgent'},
    'Uncertain Significance': {'color': '#ffa000', 'priority': 3, 'action': 'monitor'},
    'Likely Benign': {'color': '#388e3c', 'priority': 2, 'action': 'routine'},
    'Benign': {'color': '#4caf50', 'priority': 1, 'action': 'none'}
}

# Specialty clinical recommendations
SPECIALTY_RECOMMENDATIONS = {
    'CARDIAC': {
        'clinical_action': 'Cardiology referral for comprehensive cardiac evaluation',
        'screening': 'Echocardiogram, ECG, stress testing as indicated',
        'family_screening': 'First-degree relatives should undergo cardiac screening',
        'followup': 'Annual cardiac monitoring recommended'
    },
    'ONCOLOGY': {
        'clinical_action': 'Oncology genetics referral for cancer risk assessment',
        'screening': 'Enhanced cancer screening protocols per NCCN guidelines',
        'family_screening': 'Genetic counseling and testing for at-risk family members',
        'followup': 'Risk-based surveillance and prevention strategies'
    },
    'CDLS': {
        'clinical_action': 'Medical genetics referral for CdLS evaluation',
        'screening': 'Comprehensive developmental and growth assessment',
        'family_screening': 'Parental evaluation and genetic counseling',
        'followup': 'Multidisciplinary care coordination'
    },
    'NEUROLOGY': {
        'clinical_action': 'Neurology/genetics referral for evaluation',
        'screening': 'Neuroimaging and developmental assessment as indicated',
        'family_screening': 'Family history evaluation and genetic counseling',
        'followup': 'Specialty care coordination and monitoring'
    },
    'PHARMACOGENOMICS': {
        'clinical_action': 'Clinical pharmacist consultation for medication optimization',
        'screening': 'Drug interaction and efficacy assessment',
        'family_screening': 'Not typically indicated for pharmacogenomic variants',
        'followup': 'Medication monitoring and adjustment as needed'
    }
}

def setup_logging(sample_id):
    """Setup logging configuration"""
    log_dir = Path(LOGS_DIR)
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"clinical_report_{sample_id}.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_analysis_results(results_file):
    """Load multi-specialty analysis results"""
    try:
        if results_file.endswith('.json'):
            with open(results_file, 'r') as f:
                return json.load(f)
        elif results_file.endswith('.csv'):
            return pd.read_csv(results_file)
        else:
            raise ValueError("Unsupported file format. Use JSON or CSV.")
    except Exception as e:
        logging.error(f"Error loading results: {e}")
        return None

def classify_variant_clinical_significance(variant_data):
    """Determine clinical significance from available data"""
    
    # Check ACMG classification first
    if 'classification' in variant_data:
        return variant_data['classification']
    
    # Check ClinVar classification
    clinvar_sig = variant_data.get('clinvar_sig', '').lower()
    if 'pathogenic' in clinvar_sig:
        if 'likely' in clinvar_sig:
            return 'Likely Pathogenic'
        else:
            return 'Pathogenic'
    elif 'benign' in clinvar_sig:
        if 'likely' in clinvar_sig:
            return 'Likely Benign'
        else:
            return 'Benign'
    
    # Use actionability score to estimate significance
    score = variant_data.get('actionability_score', 0)
    if score >= 50:
        return 'Likely Pathogenic'
    elif score >= 40:
        return 'Uncertain Significance'
    elif score >= 20:
        return 'Uncertain Significance'
    else:
        return 'Likely Benign'

def prioritize_variants(variants_df):
    """Prioritize variants for clinical reporting"""
    if variants_df.empty:
        return variants_df
    
    # Add clinical significance if not present
    if 'clinical_significance' not in variants_df.columns:
        variants_df['clinical_significance'] = variants_df.apply(
            lambda row: classify_variant_clinical_significance(row.to_dict()), axis=1
        )
    
    # Add priority scores
    priority_map = {sig: data['priority'] for sig, data in CLINICAL_SIGNIFICANCE_MAPPING.items()}
    variants_df['priority_score'] = variants_df['clinical_significance'].map(priority_map).fillna(3)
    
    # Sort by priority (highest first), then actionability score
    variants_df = variants_df.sort_values(['priority_score', 'actionability_score'], ascending=[False, False])
    
    return variants_df

def generate_variant_summary_table(variants_df, max_variants=20):
    """Generate HTML table for high-priority variants"""
    if variants_df.empty:
        return "<p>No high-priority variants identified.</p>"
    
    # Filter to high-priority variants
    high_priority = variants_df[variants_df['priority_score'] >= 4].head(max_variants)
    
    if high_priority.empty:
        high_priority = variants_df.head(min(10, len(variants_df)))
    
    html = """
    <table class="variant-table">
        <thead>
            <tr>
                <th>Gene</th>
                <th>Variant</th>
                <th>Consequence</th>
                <th>Classification</th>
                <th>gnomAD AF</th>
                <th>Score</th>
                <th>Specialty</th>
                <th>Condition</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for _, variant in high_priority.iterrows():
        significance = variant.get('clinical_significance', 'Unknown')
        color = CLINICAL_SIGNIFICANCE_MAPPING.get(significance, {}).get('color', '#666666')
        
        html += f"""
            <tr>
                <td><strong>{variant.get('gene_symbol', '')}</strong></td>
                <td>{variant.get('hgvsc', '')}<br><small>{variant.get('hgvsp', '')}</small></td>
                <td>{variant.get('consequence', '')}</td>
                <td style="color: {color}; font-weight: bold;">{significance}</td>
                <td>{variant.get('gnomad_af', 0):.6f}</td>
                <td>{variant.get('actionability_score', 0)}</td>
                <td>{variant.get('specialty', '')}</td>
                <td>{variant.get('condition', variant.get('gene_condition', ''))}</td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    """
    
    return html

def generate_clinical_recommendations(variants_df):
    """Generate specialty-specific clinical recommendations"""
    if variants_df.empty:
        return {}
    
    # Group by specialty
    specialty_variants = variants_df.groupby('specialty')
    recommendations = {}
    
    for specialty, group in specialty_variants:
        if specialty in SPECIALTY_RECOMMENDATIONS:
            pathogenic_count = len(group[group['clinical_significance'].isin(['Pathogenic', 'Likely Pathogenic'])])
            high_priority_count = len(group[group.get('actionability_score', 0) >= 40])
            
            recs = SPECIALTY_RECOMMENDATIONS[specialty].copy()
            recs['variants_found'] = len(group)
            recs['pathogenic_variants'] = pathogenic_count
            recs['high_priority_variants'] = high_priority_count
            recs['urgency'] = 'immediate' if pathogenic_count > 0 else 'routine'
            
            recommendations[specialty] = recs
    
    return recommendations

def generate_family_screening_guidance(variants_df):
    """Generate family screening recommendations"""
    if variants_df.empty:
        return "No specific family screening recommendations based on current findings."
    
    # Count actionable variants by inheritance pattern
    inheritance_counts = defaultdict(int)
    for _, variant in variants_df.iterrows():
        inheritance = variant.get('gene_inheritance', variant.get('inheritance', 'Unknown'))
        significance = variant.get('clinical_significance', '')
        
        if significance in ['Pathogenic', 'Likely Pathogenic']:
            inheritance_counts[inheritance] += 1
    
    guidance = []
    
    if inheritance_counts.get('AD', 0) > 0:
        guidance.append("""
        <strong>Autosomal Dominant Variants:</strong> 50% risk for first-degree relatives.
        Genetic counseling and testing recommended for parents, siblings, and children.
        """)
    
    if inheritance_counts.get('AR', 0) > 0:
        guidance.append("""
        <strong>Autosomal Recessive Variants:</strong> Carrier testing recommended for reproductive partners.
        Genetic counseling for family planning decisions.
        """)
    
    if inheritance_counts.get('XL', 0) > 0:
        guidance.append("""
        <strong>X-linked Variants:</strong> All daughters of affected males are obligate carriers.
        Maternal relatives at risk. Genetic counseling recommended.
        """)
    
    if not guidance:
        guidance.append("Genetic counseling recommended to discuss implications of findings.")
    
    return "<br><br>".join(guidance)

def generate_html_report(variants_df, sample_id, analysis_metadata, output_file):
    """Generate comprehensive HTML clinical report"""
    
    # Prioritize variants
    variants_df = prioritize_variants(variants_df)
    
    # Generate components
    variant_table = generate_variant_summary_table(variants_df)
    recommendations = generate_clinical_recommendations(variants_df)
    family_guidance = generate_family_screening_guidance(variants_df)
    
    # Summary statistics
    total_variants = len(variants_df)
    pathogenic_count = len(variants_df[variants_df['clinical_significance'].isin(['Pathogenic', 'Likely Pathogenic'])])
    high_priority_count = len(variants_df[variants_df.get('actionability_score', 0) >= 40])
    specialties_analyzed = len(variants_df['specialty'].unique()) if 'specialty' in variants_df.columns else 0
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Genomics Report - {sample_id}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
            color: white;
            padding: 30px;
            margin: -30px -30px 30px -30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.2em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .disclaimer {{
            background: #ffeb3b;
            padding: 20px;
            border-left: 5px solid #ff9800;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .disclaimer h3 {{
            margin-top: 0;
            color: #e65100;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 5px solid #1976d2;
        }}
        .summary-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #1565c0;
            margin-bottom: 10px;
        }}
        .summary-label {{
            color: #424242;
            font-weight: 500;
        }}
        .section {{
            margin: 40px 0;
        }}
        .section h2 {{
            color: #1976d2;
            border-bottom: 2px solid #e3f2fd;
            padding-bottom: 10px;
        }}
        .variant-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        .variant-table th {{
            background: #1976d2;
            color: white;
            padding: 15px 10px;
            text-align: left;
            font-weight: 500;
        }}
        .variant-table td {{
            padding: 12px 10px;
            border-bottom: 1px solid #e0e0e0;
            vertical-align: top;
        }}
        .variant-table tbody tr:hover {{
            background-color: #f5f5f5;
        }}
        .recommendation-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}
        .recommendation-card h4 {{
            margin-top: 0;
            color: #495057;
        }}
        .urgency-immediate {{
            border-left: 5px solid #d32f2f;
        }}
        .urgency-urgent {{
            border-left: 5px solid #f57c00;
        }}
        .urgency-routine {{
            border-left: 5px solid #388e3c;
        }}
        .methodology {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
        }}
        .methodology h3 {{
            margin-top: 0;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 Clinical Genomics Report</h1>
            <p><strong>Sample ID:</strong> {sample_id}</p>
            <p><strong>Report Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            <p><strong>Analysis Type:</strong> Multi-Specialty Clinical Genomics</p>
        </div>
        
        <div class="disclaimer">
            <h3>⚠️ Important Clinical Disclaimer</h3>
            <p><strong>This is a research-grade analysis for clinical guidance only.</strong></p>
            <p><strong>All findings require confirmation by a CLIA-certified laboratory before clinical use.</strong></p>
            <p>This report should be used to guide further clinical testing and evaluation, not for diagnosis or treatment decisions.</p>
        </div>
        
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-number">{total_variants}</div>
                    <div class="summary-label">Clinical Variants</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{pathogenic_count}</div>
                    <div class="summary-label">Pathogenic/Likely Pathogenic</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{high_priority_count}</div>
                    <div class="summary-label">High Priority</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{specialties_analyzed}</div>
                    <div class="summary-label">Medical Specialties</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 High-Priority Variants</h2>
            {variant_table}
        </div>
        
        <div class="section">
            <h2>🏥 Clinical Recommendations</h2>
    """
    
    # Add specialty-specific recommendations
    if recommendations:
        for specialty, recs in recommendations.items():
            urgency_class = f"urgency-{recs['urgency']}"
            html_content += f"""
            <div class="recommendation-card {urgency_class}">
                <h4>{specialty.replace('_', ' ').title()} ({recs['variants_found']} variants)</h4>
                <p><strong>Clinical Action:</strong> {recs['clinical_action']}</p>
                <p><strong>Screening:</strong> {recs['screening']}</p>
                <p><strong>Follow-up:</strong> {recs['followup']}</p>
                <p><strong>Urgency:</strong> {recs['urgency'].title()}</p>
            </div>
            """
    else:
        html_content += "<p>No specific clinical recommendations based on current findings.</p>"
    
    # Add family screening section
    html_content += f"""
        </div>
        
        <div class="section">
            <h2>👨‍👩‍👧‍👦 Family Screening Guidance</h2>
            <div class="recommendation-card">
                {family_guidance}
            </div>
        </div>
        
        <div class="section">
            <h2>🔬 Methodology</h2>
            <div class="methodology">
                <h3>Analysis Pipeline</h3>
                <p><strong>Pipeline Version:</strong> Multi-Specialty Clinical Genomics v4.0</p>
                <p><strong>VEP Version:</strong> 114.2</p>
                <p><strong>Reference Assembly:</strong> GRCh38</p>
                <p><strong>Databases Used:</strong> gnomAD v4.1, ClinVar (current), CADD v1.7, dbNSFP v5.1a</p>
                <p><strong>Classification:</strong> ACMG/AMP 2015 guidelines with 2025 clinical standards</p>
                <p><strong>Quality Metrics:</strong> Research-grade analysis with clinical correlation required</p>
            </div>
        </div>
        
        <div class="footer">
            <p><em>Generated by Clinical Genomics Pipeline v4.0</em></p>
            <p><strong>For Research and Clinical Guidance Only - Clinical Validation Required</strong></p>
        </div>
    </div>
</body>
</html>
    """
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def generate_excel_summary(variants_df, sample_id, output_file):
    """Generate Excel summary for clinical review"""
    
    if variants_df.empty:
        # Create empty Excel file
        pd.DataFrame({'Note': ['No variants found for clinical reporting']}).to_excel(output_file, index=False)
        return output_file
    
    # Prioritize and prepare data
    variants_df = prioritize_variants(variants_df)
    
    # Create multiple sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # High-priority variants
        high_priority = variants_df[variants_df['priority_score'] >= 4]
        if not high_priority.empty:
            high_priority.to_excel(writer, sheet_name='High Priority', index=False)
        
        # All variants
        variants_df.to_excel(writer, sheet_name='All Variants', index=False)
        
        # Summary by specialty
        if 'specialty' in variants_df.columns:
            specialty_summary = variants_df.groupby('specialty').agg({
                'gene_symbol': 'count',
                'actionability_score': 'mean',
                'clinical_significance': lambda x: (x.isin(['Pathogenic', 'Likely Pathogenic'])).sum()
            }).round(2)
            specialty_summary.columns = ['Total Variants', 'Avg Score', 'Pathogenic Count']
            specialty_summary.to_excel(writer, sheet_name='Specialty Summary')
    
    return output_file

def generate_clinical_report(input_file, sample_id, output_dir, report_format='html'):
    """Main function to generate clinical report"""
    
    logger = setup_logging(sample_id)
    logger.info(f"Starting clinical report generation for sample: {sample_id}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load analysis results
    logger.info(f"Loading analysis results from: {input_file}")
    
    if input_file.endswith('.json'):
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame if needed
        if isinstance(data, dict) and 'variants' in data:
            variants_df = pd.DataFrame(data['variants'])
            analysis_metadata = {k: v for k, v in data.items() if k != 'variants'}
        else:
            variants_df = pd.DataFrame(data)
            analysis_metadata = {}
    else:
        variants_df = pd.read_csv(input_file)
        analysis_metadata = {}
    
    logger.info(f"Loaded {len(variants_df)} variants for reporting")
    
    # Generate reports
    report_files = []
    
    if report_format in ['html', 'all']:
        html_file = output_path / f"{sample_id}_clinical_report.html"
        generate_html_report(variants_df, sample_id, analysis_metadata, html_file)
        report_files.append(html_file)
        logger.info(f"HTML report generated: {html_file}")
    
    if report_format in ['excel', 'all']:
        excel_file = output_path / f"{sample_id}_clinical_summary.xlsx"
        generate_excel_summary(variants_df, sample_id, excel_file)
        report_files.append(excel_file)
        logger.info(f"Excel summary generated: {excel_file}")
    
    logger.info("Clinical report generation completed successfully")
    return report_files

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Clinical Report Generator v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate HTML report from multi-specialty results
    python3 clinical_report_generator.py results.csv SAMPLE_001 --format html
    
    # Generate both HTML and Excel reports
    python3 clinical_report_generator.py results.json SAMPLE_001 --format all
    
    # Custom output directory
    python3 clinical_report_generator.py results.csv SAMPLE_001 --output_dir /path/to/reports

Input Files:
    - CSV file from multi-specialty analysis
    - JSON file with structured variant data
    
Output Files:
    - HTML clinical report (professional formatting)
    - Excel summary (multi-sheet workbook)
        """
    )
    
    parser.add_argument('input_file', help='Analysis results file (CSV or JSON)')
    parser.add_argument('sample_id', help='Sample identifier')
    parser.add_argument('--output_dir', default=f"{BASE_DIR}/annotation_results/clinical_reports",
                       help='Output directory for reports')
    parser.add_argument('--format', choices=['html', 'excel', 'all'], default='html',
                       help='Report format to generate')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.sample_id)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Validate input file
    if not os.path.exists(args.input_file):
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)
    
    try:
        report_files = generate_clinical_report(
            args.input_file, 
            args.sample_id, 
            args.output_dir, 
            args.format
        )
        
        print("\n" + "="*70)
        print("CLINICAL REPORT GENERATION - COMPLETED")
        print("="*70)
        print(f"Sample: {args.sample_id}")
        print(f"Reports Generated:")
        for report_file in report_files:
            print(f"  - {report_file}")
        print("\nIMPORTANT:")
        print("- This is research-grade analysis for clinical guidance only")
        print("- All findings require CLIA laboratory confirmation")
        print("- Use for clinical testing strategy, not diagnosis")
        print("="*70)
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
