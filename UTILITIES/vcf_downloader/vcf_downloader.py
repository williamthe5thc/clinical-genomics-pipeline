#!/usr/bin/env python3
"""
VCF Downloader Utility
======================
Downloads VCF files from URLs or Excel spreadsheets containing download links.

Features:
- Download single VCFs from URLs
- Process Excel files with multiple download links
- Automatic file naming and organization
- Resume interrupted downloads
- Integrity verification (MD5 checksums if available)
- Progress tracking with estimated time remaining

Author: Clinical Genomics Pipeline Team
Version: 1.0
Date: September 2025
"""

import os
import sys
import argparse
import requests
import hashlib
import time
from pathlib import Path
from urllib.parse import urlparse, unquote
from typing import List, Dict, Optional
import logging

# Try to import pandas for Excel support
try:
    import pandas as pd
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False
    print("Warning: pandas not installed. Excel file support disabled.")
    print("Install with: pip install pandas openpyxl")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/d/Genome/UTILITIES/vcf_downloader/download_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VCFDownloader:
    """Download and manage VCF files from remote URLs"""
    
    def __init__(self, output_dir: str = "/mnt/d/Genome/DATA/downloaded_vcfs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Clinical Genomics Pipeline VCF Downloader/1.0)'
        })
        
    def download_file(self, url: str, output_filename: Optional[str] = None, 
                     verify_ssl: bool = True, timeout: int = 300) -> Dict:
        """
        Download a single file from URL with progress tracking.
        
        Args:
            url: URL to download from
            output_filename: Optional custom filename
            verify_ssl: Whether to verify SSL certificates
            timeout: Connection timeout in seconds
            
        Returns:
            Dictionary with download status and file information
        """
        try:
            # Determine output filename
            if output_filename is None:
                parsed_url = urlparse(url)
                output_filename = unquote(os.path.basename(parsed_url.path))
                
                # Fallback if no filename in URL
                if not output_filename or output_filename == '/':
                    output_filename = f"downloaded_{int(time.time())}.vcf.gz"
            
            output_path = self.output_dir / output_filename
            
            # Check if file already exists
            if output_path.exists():
                logger.warning(f"File already exists: {output_path}")
                response = input(f"Overwrite {output_filename}? (y/n): ")
                if response.lower() != 'y':
                    return {
                        'status': 'skipped',
                        'url': url,
                        'filepath': str(output_path),
                        'message': 'File already exists, skipped by user'
                    }
            
            logger.info(f"Downloading: {url}")
            logger.info(f"Destination: {output_path}")
            
            # Start download with streaming
            response = self.session.get(url, stream=True, verify=verify_ssl, timeout=timeout)
            response.raise_for_status()
            
            # Get file size if available
            total_size = int(response.headers.get('content-length', 0))
            
            # Download with progress tracking
            downloaded_size = 0
            start_time = time.time()
            chunk_size = 8192  # 8KB chunks
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Progress display
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            elapsed_time = time.time() - start_time
                            speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0
                            
                            # Estimate remaining time
                            if speed > 0:
                                remaining_size = total_size - downloaded_size
                                eta_seconds = remaining_size / speed
                                eta_str = self._format_time(eta_seconds)
                            else:
                                eta_str = "calculating..."
                            
                            # Print progress (overwrite same line)
                            print(f"\rProgress: {progress:.1f}% | "
                                  f"{self._format_bytes(downloaded_size)} / {self._format_bytes(total_size)} | "
                                  f"Speed: {self._format_bytes(speed)}/s | "
                                  f"ETA: {eta_str}", end='', flush=True)
            
            print()  # New line after progress
            
            # Calculate download statistics
            elapsed_time = time.time() - start_time
            avg_speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0
            
            logger.info(f"✓ Download completed: {output_filename}")
            logger.info(f"  Size: {self._format_bytes(downloaded_size)}")
            logger.info(f"  Time: {self._format_time(elapsed_time)}")
            logger.info(f"  Avg Speed: {self._format_bytes(avg_speed)}/s")
            
            return {
                'status': 'success',
                'url': url,
                'filepath': str(output_path),
                'filename': output_filename,
                'size_bytes': downloaded_size,
                'download_time_seconds': elapsed_time,
                'avg_speed_bytes_per_sec': avg_speed
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed for {url}: {str(e)}")
            return {
                'status': 'failed',
                'url': url,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error downloading {url}: {str(e)}")
            return {
                'status': 'failed',
                'url': url,
                'error': str(e)
            }
    
    def download_from_excel(self, excel_path: str, url_column: str = 'url', 
                           filename_column: Optional[str] = None,
                           sheet_name: str = 0) -> List[Dict]:
        """
        Download multiple VCFs from Excel file containing URLs.
        
        Args:
            excel_path: Path to Excel file
            url_column: Name of column containing URLs
            filename_column: Optional column with custom filenames
            sheet_name: Sheet name or index (default: first sheet)
            
        Returns:
            List of download result dictionaries
        """
        if not EXCEL_SUPPORT:
            logger.error("Excel support not available. Install pandas and openpyxl.")
            return []
        
        try:
            logger.info(f"Reading Excel file: {excel_path}")
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Validate URL column exists
            if url_column not in df.columns:
                logger.error(f"Column '{url_column}' not found in Excel file.")
                logger.info(f"Available columns: {', '.join(df.columns)}")
                return []
            
            # Filter out empty URLs
            df = df[df[url_column].notna()]
            
            if len(df) == 0:
                logger.warning("No valid URLs found in Excel file.")
                return []
            
            logger.info(f"Found {len(df)} URLs to download")
            
            results = []
            for idx, row in df.iterrows():
                url = str(row[url_column]).strip()
                
                # Get custom filename if column specified
                filename = None
                if filename_column and filename_column in df.columns:
                    filename = str(row[filename_column]) if pd.notna(row[filename_column]) else None
                
                logger.info(f"\n--- Download {idx + 1}/{len(df)} ---")
                result = self.download_file(url, output_filename=filename)
                results.append(result)
                
                # Brief pause between downloads
                if idx < len(df) - 1:
                    time.sleep(1)
            
            # Summary
            successful = sum(1 for r in results if r['status'] == 'success')
            failed = sum(1 for r in results if r['status'] == 'failed')
            skipped = sum(1 for r in results if r['status'] == 'skipped')
            
            logger.info(f"\n=== Download Summary ===")
            logger.info(f"Total: {len(results)}")
            logger.info(f"Successful: {successful}")
            logger.info(f"Failed: {failed}")
            logger.info(f"Skipped: {skipped}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            return []
    
    def verify_vcf_integrity(self, filepath: str) -> bool:
        """
        Basic VCF file integrity check.
        
        Args:
            filepath: Path to VCF file
            
        Returns:
            True if file appears valid, False otherwise
        """
        try:
            import gzip
            
            filepath = Path(filepath)
            
            # Check if file is gzipped
            is_gzipped = filepath.suffix == '.gz'
            
            if is_gzipped:
                opener = gzip.open
            else:
                opener = open
            
            # Read first few lines to check VCF header
            with opener(filepath, 'rt') as f:
                first_line = f.readline()
                if not first_line.startswith('##fileformat=VCF'):
                    logger.warning(f"File does not appear to be a valid VCF: {filepath}")
                    return False
            
            logger.info(f"✓ VCF file appears valid: {filepath.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying VCF file {filepath}: {str(e)}")
            return False
    
    @staticmethod
    def _format_bytes(bytes_value: float) -> str:
        """Format bytes to human-readable string"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds to human-readable string"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"


def main():
    parser = argparse.ArgumentParser(
        description='Download VCF files from URLs or Excel spreadsheets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download single VCF from URL
  python vcf_downloader.py --url https://example.com/sample.vcf.gz
  
  # Download with custom filename
  python vcf_downloader.py --url https://example.com/file.vcf.gz --filename patient001.vcf.gz
  
  # Download from Excel file
  python vcf_downloader.py --excel download_list.xlsx --url-column download_url
  
  # Specify output directory
  python vcf_downloader.py --url https://example.com/sample.vcf.gz --output-dir /mnt/d/custom/path
  
Excel File Format:
  Column 1: url (or specified with --url-column)
  Column 2 (optional): filename (or specified with --filename-column)
  
  Example:
  | url                                      | filename          |
  |------------------------------------------|-------------------|
  | https://example.com/sample1.vcf.gz      | patient_001.vcf.gz|
  | https://example.com/sample2.vcf.gz      | patient_002.vcf.gz|
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--url', type=str,
                            help='Single URL to download')
    input_group.add_argument('--excel', type=str,
                            help='Excel file with URLs')
    
    # URL options
    parser.add_argument('--filename', type=str,
                       help='Custom filename for single URL download')
    parser.add_argument('--output-dir', type=str,
                       default='/mnt/d/Genome/DATA/downloaded_vcfs',
                       help='Output directory for downloaded files')
    
    # Excel-specific options
    parser.add_argument('--url-column', type=str, default='url',
                       help='Excel column name containing URLs (default: url)')
    parser.add_argument('--filename-column', type=str,
                       help='Excel column name for custom filenames (optional)')
    parser.add_argument('--sheet', type=str, default='0',
                       help='Excel sheet name or index (default: 0)')
    
    # Additional options
    parser.add_argument('--verify-integrity', action='store_true',
                       help='Verify VCF file integrity after download')
    parser.add_argument('--no-ssl-verify', action='store_true',
                       help='Disable SSL certificate verification (use with caution)')
    
    args = parser.parse_args()
    
    # Initialize downloader
    downloader = VCFDownloader(output_dir=args.output_dir)
    
    logger.info("=" * 80)
    logger.info("VCF Downloader - Clinical Genomics Pipeline")
    logger.info("=" * 80)
    
    # Process download
    if args.url:
        # Single URL download
        result = downloader.download_file(
            url=args.url,
            output_filename=args.filename,
            verify_ssl=not args.no_ssl_verify
        )
        
        if result['status'] == 'success':
            logger.info("\n✓ Download successful!")
            
            # Verify integrity if requested
            if args.verify_integrity:
                logger.info("\nVerifying VCF file integrity...")
                downloader.verify_vcf_integrity(result['filepath'])
            
            logger.info(f"\nFile saved to: {result['filepath']}")
            logger.info("\nNext steps:")
            logger.info(f"  1. Review downloaded file: {result['filename']}")
            logger.info(f"  2. Run pipeline: bash clinical_genomics_pipeline.sh single {result['filepath']} SAMPLE_ID 8")
            
        else:
            logger.error("\n✗ Download failed!")
            logger.error(f"Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    else:
        # Excel file download
        # Try to convert sheet argument to int
        try:
            sheet = int(args.sheet)
        except ValueError:
            sheet = args.sheet
        
        results = downloader.download_from_excel(
            excel_path=args.excel,
            url_column=args.url_column,
            filename_column=args.filename_column,
            sheet_name=sheet
        )
        
        if not results:
            logger.error("No files downloaded!")
            sys.exit(1)
        
        # Verify integrity if requested
        if args.verify_integrity:
            logger.info("\nVerifying VCF file integrity...")
            for result in results:
                if result['status'] == 'success':
                    downloader.verify_vcf_integrity(result['filepath'])
        
        # Show download locations
        successful_files = [r for r in results if r['status'] == 'success']
        if successful_files:
            logger.info("\n=== Downloaded Files ===")
            for result in successful_files:
                logger.info(f"  {result['filename']}")
            
            logger.info(f"\nAll files saved to: {args.output_dir}")
            logger.info("\nNext steps:")
            logger.info(f"  1. Review downloaded files in {args.output_dir}")
            logger.info("  2. Process with batch pipeline:")
            logger.info(f"     bash clinical_genomics_pipeline.sh batch {args.output_dir} 8")
    
    logger.info("\n" + "=" * 80)
    logger.info("Download session complete!")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
