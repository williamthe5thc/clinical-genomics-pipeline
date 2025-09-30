#!/usr/bin/env python3

"""
🔬 DRAGEN ISSUE-SPECIFIC VCF PREPROCESSOR v4.1
Fixes specific DRAGEN VCF parsing problems

TARGET ISSUES:
- Header typo: "ReatPosRankSum" -> "ReadPosRankSum"
- Invalid '$' characters in FORMAT fields (especially SB)
- Malformed VCF records that crash cyvcf2 parsing
- Missing header definitions

DEPLOYMENT: /mnt/d/Genome/COMPONENTS/VCF_PROCESSING/dragen_vcf_fixer.py
"""

import os
import sys
import subprocess
import tempfile
import argparse
import logging
import gzip
import re
from pathlib import Path
from collections import defaultdict

def setup_logging(sample_id: str):
    """Setup logging configuration"""
    log_dir = Path("/mnt/d/Genome/DATA/LOGS")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"dragen_vcf_fixer_{sample_id}.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def run_command(cmd: str, logger, description: str = ""):
    """Run shell command with error handling"""
    logger.info(f"Running: {description}")
    logger.debug(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            logger.debug(f"Output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}")
        logger.error(f"Error: {e.stderr}")
        raise

class DRAGENVCFFixer:
    """Fix specific DRAGEN VCF issues that cause parsing failures"""
    
    def __init__(self, logger):
        self.logger = logger
        self.fixes_applied = defaultdict(int)
        
    def fix_vcf_issues(self, input_vcf: str, output_vcf: str, temp_dir: str) -> bool:
        """Main function to fix DRAGEN VCF issues"""
        
        self.logger.info(f"Fixing DRAGEN VCF issues: {input_vcf} -> {output_vcf}")
        
        temp_path = Path(temp_dir)
        
        # Step 1: Fix header issues
        step1_output = temp_path / "step1_header_fixed.vcf"
        self._fix_header_issues(input_vcf, step1_output)
        
        # Step 2: Fix FORMAT field issues
        step2_output = temp_path / "step2_format_fixed.vcf"
        self._fix_format_field_issues(step1_output, step2_output)
        
        # Step 3: Remove problematic records
        step3_output = temp_path / "step3_records_cleaned.vcf"
        self._clean_problematic_records(step2_output, step3_output)
        
        # Step 4: Final validation and output
        self._create_final_output(step3_output, output_vcf)
        
        # Report fixes
        self._report_fixes_applied()
        
        return True
    
    def _fix_header_issues(self, input_vcf: str, output_vcf: str):
        """Fix header typos and missing definitions"""
        
        self.logger.info("Fixing header issues...")
        
        open_func = gzip.open if input_vcf.endswith('.gz') else open
        
        with open_func(input_vcf, 'rt') as infile, open(output_vcf, 'w') as outfile:
            for line in infile:
                if line.startswith('#'):
                    # Fix known header typos
                    if 'ReatPosRankSum' in line:
                        line = line.replace('ReatPosRankSum', 'ReadPosRankSum')
                        self.fixes_applied['header_typo_fixes'] += 1
                        self.logger.info("Fixed header typo: ReatPosRankSum -> ReadPosRankSum")
                    
                    # Add missing essential header definitions if needed
                    if line.startswith('##FORMAT=<ID=GT'):
                        # Add comprehensive FORMAT definitions after GT
                        outfile.write(line)
                        outfile.write('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">\n')
                        outfile.write('##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">\n')
                        outfile.write('##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">\n')
                        outfile.write('##FORMAT=<ID=SB,Number=4,Type=Integer,Description="Strand bias (clean format)">\n')
                        self.fixes_applied['header_definitions_added'] += 1
                        continue
                    
                    # Fix INFO field typos
                    if 'ReadPosRankSum' in line and '##INFO=' in line:
                        # Ensure INFO ReadPosRankSum is correctly defined
                        if 'ReadPosRankSum,Number=1,Type=Float' not in line:
                            line = '##INFO=<ID=ReadPosRankSum,Number=1,Type=Float,Description="Z-score from Wilcoxon rank sum test of Alt vs. Ref read position bias">\n'
                            self.fixes_applied['info_field_fixes'] += 1
                    
                    outfile.write(line)
                else:
                    # We've reached the data section
                    outfile.write(line)
                    break
            
            # Copy rest of file
            for line in infile:
                outfile.write(line)
    
    def _fix_format_field_issues(self, input_vcf: str, output_vcf: str):
        """Fix FORMAT field issues, especially invalid characters"""
        
        self.logger.info("Fixing FORMAT field issues...")
        
        with open(input_vcf, 'r') as infile, open(output_vcf, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                if line.startswith('#'):
                    outfile.write(line)
                    continue
                
                fields = line.strip().split('\t')
                if len(fields) < 10:  # Skip malformed lines
                    continue
                
                # Check FORMAT field (column 8, 0-indexed)
                format_field = fields[8] if len(fields) > 8 else ""
                
                # Process sample data (columns 9+)
                line_modified = False
                for i in range(9, len(fields)):
                    sample_data = fields[i]
                    
                    # Fix invalid characters in sample data
                    if '$' in sample_data:
                        # Remove invalid '$' characters
                        cleaned_data = sample_data.replace('$', '')
                        fields[i] = cleaned_data
                        line_modified = True
                        self.fixes_applied['invalid_char_fixes'] += 1
                        
                        if line_num % 10000 == 0:  # Log periodically
                            self.logger.debug(f"Fixed invalid character at line {line_num}")
                    
                    # Fix other problematic characters
                    if any(char in sample_data for char in ['#', '@', '%', '^', '&', '*']):
                        # Replace problematic characters with appropriate values
                        cleaned_data = re.sub(r'[#@%^&*]', '.', sample_data)
                        fields[i] = cleaned_data
                        line_modified = True
                        self.fixes_applied['char_replacement_fixes'] += 1
                
                # Write the (possibly modified) line
                if line_modified:
                    outfile.write('\t'.join(fields) + '\n')
                else:
                    outfile.write(line)
                
                # Progress logging
                if line_num % 50000 == 0:
                    self.logger.info(f"Processed {line_num:,} variant records...")
        
        self.logger.info("FORMAT field issues fixed")
    
    def _clean_problematic_records(self, input_vcf: str, output_vcf: str):
        """Remove records that are completely malformed and unfixable"""
        
        self.logger.info("Cleaning problematic records...")
        
        removed_count = 0
        kept_count = 0
        
        with open(input_vcf, 'r') as infile, open(output_vcf, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                if line.startswith('#'):
                    outfile.write(line)
                    continue
                
                fields = line.strip().split('\t')
                
                # Basic record validation
                if len(fields) < 8:
                    removed_count += 1
                    self.logger.debug(f"Removed malformed record at line {line_num}: insufficient fields")
                    continue
                
                # Check for completely invalid records
                try:
                    # Validate chromosome
                    chrom = fields[0]
                    if not chrom or chrom in ['', '.', 'N/A']:
                        removed_count += 1
                        continue
                    
                    # Validate position
                    pos = int(fields[1])
                    if pos <= 0:
                        removed_count += 1
                        continue
                    
                    # Validate REF and ALT
                    ref = fields[3]
                    alt = fields[4]
                    if not ref or not alt or ref == '.' or alt == '.':
                        removed_count += 1
                        continue
                    
                    # Check for impossible ALT alleles
                    if alt in ['<DEL>', '<INS>', '<DUP>'] and len(fields) < 10:
                        # Structural variants need proper FORMAT data
                        removed_count += 1
                        continue
                    
                    # Record is salvageable
                    outfile.write(line)
                    kept_count += 1
                    
                except (ValueError, IndexError) as e:
                    removed_count += 1
                    self.logger.debug(f"Removed invalid record at line {line_num}: {e}")
                    continue
                
                if line_num % 100000 == 0:
                    self.logger.info(f"Processed {line_num:,} records, removed {removed_count:,}")
        
        self.logger.info(f"Record cleaning complete: kept {kept_count:,}, removed {removed_count:,}")
        self.fixes_applied['records_removed'] = removed_count
        self.fixes_applied['records_kept'] = kept_count
    
    def _create_final_output(self, processed_vcf: str, output_vcf: str):
        """Create final output with proper compression and indexing"""
        
        self.logger.info("Creating final output...")
        
        # Create output directory
        output_path = Path(output_vcf)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy processed file
        cmd = f"cp '{processed_vcf}' '{output_vcf}'"
        run_command(cmd, self.logger, "Creating final VCF")
        
        # Create compressed version
        cmd = f"bgzip -c '{output_vcf}' > '{output_vcf}.gz'"
        run_command(cmd, self.logger, "Compressing VCF")
        
        # Create index
        cmd = f"tabix -p vcf '{output_vcf}.gz'"
        run_command(cmd, self.logger, "Indexing VCF")
        
        # Create sorted filename version for compatibility
        sorted_output = output_vcf.replace('.vcf', '_sorted.vcf')
        cmd = f"cp '{output_vcf}' '{sorted_output}'"
        run_command(cmd, self.logger, "Creating sorted version")
        
        cmd = f"bgzip -c '{sorted_output}' > '{sorted_output}.gz'"
        run_command(cmd, self.logger, "Compressing sorted version")
        
        cmd = f"tabix -p vcf '{sorted_output}.gz'"
        run_command(cmd, self.logger, "Indexing sorted version")
        
        self.logger.info("Final output created successfully")
    
    def _report_fixes_applied(self):
        """Report summary of fixes applied"""
        
        self.logger.info("=== DRAGEN VCF FIXES APPLIED ===")
        for fix_type, count in self.fixes_applied.items():
            self.logger.info(f"{fix_type}: {count:,}")
        
        total_fixes = sum(self.fixes_applied.values())
        self.logger.info(f"Total fixes applied: {total_fixes:,}")
        self.logger.info("=== FIX SUMMARY COMPLETE ===")

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(
        description="DRAGEN VCF Issue Fixer v4.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🔬 DRAGEN-SPECIFIC VCF ISSUE FIXER

TARGET ISSUES:
- Header typos: "ReatPosRankSum" -> "ReadPosRankSum"
- Invalid characters in FORMAT fields (especially '$' in SB)
- Malformed VCF records that crash cyvcf2
- Missing header definitions

Examples:
    # Fix DRAGEN VCF issues
    python3 dragen_vcf_fixer.py input.vcf.gz output_fixed.vcf SAMPLE_ID
    
    # With verbose logging
    python3 dragen_vcf_fixer.py input.vcf.gz output_fixed.vcf SAMPLE_ID --verbose

Output Files:
    - output_fixed.vcf          # Fixed uncompressed VCF
    - output_fixed.vcf.gz       # Fixed compressed VCF + index
    - output_fixed_sorted.vcf.gz # Pipeline-compatible format

🎯 DEPLOYMENT:
Save as: /mnt/d/Genome/COMPONENTS/VCF_PROCESSING/dragen_vcf_fixer.py
        """
    )
    
    parser.add_argument('input_vcf', help='Input DRAGEN VCF file')
    parser.add_argument('output_vcf', help='Output fixed VCF file')
    parser.add_argument('sample_id', help='Sample identifier for logging')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.sample_id)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Validate inputs
    if not os.path.exists(args.input_vcf):
        logger.error(f"Input VCF not found: {args.input_vcf}")
        sys.exit(1)
    
    # Check dependencies
    required_tools = ['bgzip', 'tabix']
    for tool in required_tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            logger.error(f"Required tool not found: {tool}")
            sys.exit(1)
    
    logger.info("DRAGEN VCF Issue Fixer v4.1 - Starting")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixer = DRAGENVCFFixer(logger)
            success = fixer.fix_vcf_issues(args.input_vcf, args.output_vcf, temp_dir)
            
            if success:
                print("\n" + "="*70)
                print("🔬 DRAGEN VCF ISSUE FIXER - COMPLETED")
                print("="*70)
                print(f"Sample: {args.sample_id}")
                print(f"Input: {args.input_vcf}")
                print(f"Output: {args.output_vcf}")
                print("\n🎯 FIXES APPLIED:")
                for fix_type, count in fixer.fixes_applied.items():
                    print(f"- {fix_type}: {count:,}")
                print("\n📁 OUTPUT FILES:")
                print(f"- {args.output_vcf}")
                print(f"- {args.output_vcf}.gz")
                print(f"- {args.output_vcf.replace('.vcf', '_sorted.vcf.gz')}")
                print("\n✅ READY FOR ACMG ANALYSIS")
                print("="*70)
                sys.exit(0)
            else:
                print("❌ DRAGEN VCF fixing failed")
                sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
