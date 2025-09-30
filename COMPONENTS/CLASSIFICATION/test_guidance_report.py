#!/usr/bin/env python3
"""
Test the enhanced report with clinical guidance
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_report_with_guidance import EnhancedReportWithGuidance

def main():
    print("🧪 Testing Enhanced Report with Clinical Guidance")
    print("=" * 70)
    
    # Find latest results
    results_base = Path(__file__).parent.parent.parent / "DATA" / "RESULTS" / "VCF_ANALYSIS" / "individuals"
    
    if len(sys.argv) >= 4:
        csv_file = Path(sys.argv[1])
        sample_id = sys.argv[2]
        output_dir = Path(sys.argv[3])
    elif results_base.exists():
        sample_dirs = sorted([d for d in results_base.iterdir() if d.is_dir()], 
                           key=lambda x: x.stat().st_mtime, reverse=True)
        
        csv_file = None
        for sd in sample_dirs:
            ca = sd / "clinical_analysis"
            csvs = list(ca.glob("*_ENHANCED_VARIANTS.csv"))
            if csvs:
                csv_file = csvs[0]
                sample_id = sd.name
                output_dir = ca
                break
        
        if not csv_file:
            print("❌ No results found")
            print("Usage: python test_guidance_report.py <csv_file> <sample_id> <output_dir>")
            sys.exit(1)
        
        print(f"✅ Found: {sample_id}")
        print(f"📁 CSV: {csv_file.name}")
    else:
        print("Usage: python test_guidance_report.py <csv_file> <sample_id> <output_dir>")
        sys.exit(1)
    
    print()
    print("🎯 Generating report with ACTUAL clinical guidance...")
    print()
    
    generator = EnhancedReportWithGuidance(str(csv_file), sample_id, str(output_dir))
    generator.load_data()
    html_file = generator.generate_enhanced_html_with_guidance()
    
    if html_file:
        print()
        print("=" * 70)
        print("🎉 SUCCESS! Report with Clinical Guidance Generated")
        print("=" * 70)
        print()
        print(f"📄 Report Location: {html_file}")
        print()
        print("✨ This report now includes:")
        print("   • Plain English explanation of 'actionable'")
        print("   • Specific appointments to schedule (with timeframes)")
        print("   • Exact tests you need")
        print("   • Medications to avoid")
        print("   • Lifestyle changes required")
        print("   • Family screening recommendations")
        print("   • Expected outcomes with/without treatment")
        print("   • Helpful resources and websites")
        print()
        print("🌐 Open in browser to see the difference!")
        print()
    else:
        print("❌ Failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
