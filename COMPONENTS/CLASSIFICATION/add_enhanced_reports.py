#!/usr/bin/env python3
"""
Quick Integration Script - Add Enhanced Reports to Existing Pipeline
This modifies comprehensive_gene_analyzer.py to automatically generate enhanced HTML reports
"""

import sys
from pathlib import Path

def add_enhanced_reporting():
    """Add enhanced reporting capability to comprehensive_gene_analyzer.py"""
    
    analyzer_file = Path(__file__).parent / "comprehensive_gene_analyzer.py"
    
    if not analyzer_file.exists():
        print(f"❌ Could not find {analyzer_file}")
        return False
    
    print(f"📝 Reading {analyzer_file}...")
    with open(analyzer_file, 'r') as f:
        content = f.read()
    
    # Check if already integrated
    if 'enhanced_report_integration' in content:
        print("✅ Enhanced reporting already integrated!")
        return True
    
    # Add import at the top of the file (after other imports)
    import_statement = "\n# Enhanced HTML report generation\ntry:\n    from enhanced_report_integration import integrate_enhanced_report\n    ENHANCED_REPORTS_AVAILABLE = True\nexcept ImportError:\n    ENHANCED_REPORTS_AVAILABLE = False\n    print('ℹ️  Enhanced reports not available (enhanced_report_integration.py not found)')\n"
    
    # Find the location to insert (after the cyvcf2 import)
    if "import cyvcf2" in content:
        content = content.replace("import cyvcf2", f"import cyvcf2{import_statement}")
    else:
        print("⚠️  Could not find import location, adding at beginning")
        content = import_statement + "\n" + content
    
    # Find the generate_all_reports method and add enhanced report generation
    if "def generate_all_reports(self):" in content:
        enhanced_call = """
        
        # Generate enhanced HTML report if available
        if ENHANCED_REPORTS_AVAILABLE:
            try:
                csv_file = self.output_dir / f"{self.sample_id}_ENHANCED_VARIANTS.csv"
                if csv_file.exists():
                    integrate_enhanced_report(str(csv_file), self.sample_id, str(self.output_dir))
            except Exception as e:
                print(f"⚠️  Could not generate enhanced report: {e}")
        """
        
        # Insert after the _generate_interactive_html call
        if 'self._generate_interactive_html()' in content:
            content = content.replace(
                'self._generate_interactive_html()',
                f'self._generate_interactive_html(){enhanced_call}'
            )
        else:
            print("⚠️  Could not find insertion point for enhanced report call")
    
    # Backup original file
    backup_file = analyzer_file.parent / f"{analyzer_file.name}.backup"
    print(f"💾 Creating backup: {backup_file}")
    with open(backup_file, 'w') as f:
        with open(analyzer_file, 'r') as original:
            f.write(original.read())
    
    # Write modified file
    print(f"✍️  Writing enhanced version...")
    with open(analyzer_file, 'w') as f:
        f.write(content)
    
    print("✅ Enhanced reporting integrated successfully!")
    print(f"   Backup saved to: {backup_file}")
    print("\n🎉 Next time you run your pipeline, it will automatically generate:")
    print("   • Standard reports (CSV, HTML)")
    print("   • Enhanced modern HTML report with interactive features")
    
    return True

if __name__ == "__main__":
    print("🚀 Enhanced Report Integration Script")
    print("=" * 60)
    print("\nThis script will modify comprehensive_gene_analyzer.py to")
    print("automatically generate enhanced HTML reports.\n")
    
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        success = add_enhanced_reporting()
        if success:
            print("\n" + "=" * 60)
            print("✅ Integration complete!")
            print("\nYou can now run your pipeline normally and it will")
            print("automatically generate the enhanced HTML reports.")
            print("\nTo test immediately, run:")
            print("  python test_enhanced_report.py")
        else:
            print("\n❌ Integration failed. Check error messages above.")
            sys.exit(1)
    else:
        print("❌ Integration cancelled.")
        sys.exit(0)
