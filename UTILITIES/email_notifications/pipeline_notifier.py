#!/usr/bin/env python3
"""
Clinical Genomics Pipeline Email Notification System
Sends completion notifications for VEP annotation and other pipeline stages
"""

import smtplib
import os
import sys
import argparse
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

class PipelineNotifier:
    def __init__(self, config_file=None):
        """Initialize email notifier with configuration"""
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file):
        """Load email configuration from file or environment variables"""
        config = {}
        
        # Try to load from config file first
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                print(f"✅ Loaded email config from {config_file}")
                return config
            except Exception as e:
                print(f"⚠️  Warning: Could not load config file {config_file}: {e}")
        
        # Fall back to environment variables
        config = {
            'smtp_server': os.getenv('PIPELINE_SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('PIPELINE_SMTP_PORT', '587')),
            'email_user': os.getenv('PIPELINE_EMAIL_USER'),
            'email_password': os.getenv('PIPELINE_EMAIL_PASSWORD'),
            'recipient_email': os.getenv('PIPELINE_RECIPIENT_EMAIL'),
            'sender_name': os.getenv('PIPELINE_SENDER_NAME', 'Clinical Genomics Pipeline'),
            'enable_notifications': os.getenv('PIPELINE_EMAIL_ENABLED', 'true').lower() == 'true'
        }
        
        return config
    
    def validate_config(self):
        """Validate email configuration"""
        required_fields = ['email_user', 'email_password', 'recipient_email']
        missing = [field for field in required_fields if not self.config.get(field)]
        
        if missing:
            print(f"❌ Missing email configuration: {', '.join(missing)}")
            print("   Please set environment variables or create config file:")
            print("   PIPELINE_EMAIL_USER, PIPELINE_EMAIL_PASSWORD, PIPELINE_RECIPIENT_EMAIL")
            return False
        return True
    
    def format_duration(self, start_time, end_time):
        """Format duration between timestamps"""
        try:
            import re
            
            # Handle different time formats from your pipeline
            time_formats = [
                "%a %b %d %H:%M:%S %Z %Y",  # Standard format from 'date' command
                "%Y-%m-%d %H:%M:%S",        # Your log format
                "%a %b %d %H:%M:%S %Y",     # Without timezone
                "%m/%d/%Y %H:%M:%S"         # Alternative format
            ]
            
            start_dt = None
            end_dt = None
            
            # Try to parse start time
            for fmt in time_formats:
                try:
                    if isinstance(start_time, str):
                        # Clean up the time string
                        clean_start = start_time.strip()
                        start_dt = datetime.datetime.strptime(clean_start, fmt)
                        break
                except ValueError:
                    continue
            
            # Try to parse end time
            for fmt in time_formats:
                try:
                    if isinstance(end_time, str):
                        clean_end = end_time.strip()
                        end_dt = datetime.datetime.strptime(clean_end, fmt)
                        break
                except ValueError:
                    continue
            
            if start_dt and end_dt:
                duration = end_dt - start_dt
                total_seconds = int(duration.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if hours > 0:
                    return f"{hours}h {minutes}m {seconds}s"
                elif minutes > 0:
                    return f"{minutes}m {seconds}s"
                else:
                    return f"{seconds}s"
        except Exception as e:
            print(f"⚠️  Duration calculation failed: {e}")
            
        return "Unknown duration"
    
    def send_vep_completion_notification(self, sample_id, start_time, end_time, 
                                       output_file, file_size, variant_count, 
                                       success=True, error_message=None):
        """Send VEP completion notification"""
        
        if not self.config.get('enable_notifications', True):
            print("📧 Email notifications disabled")
            return True
            
        if not self.validate_config():
            return False
        
        # Calculate duration
        duration = self.format_duration(start_time, end_time)
        
        # Determine subject and status
        if success:
            subject = f"✅ VEP Annotation Completed - {sample_id}"
            status_emoji = "✅"
            status_text = "COMPLETED SUCCESSFULLY"
            status_color = "#28a745"
        else:
            subject = f"❌ VEP Annotation Failed - {sample_id}"
            status_emoji = "❌"
            status_text = "FAILED"
            status_color = "#dc3545"
        
        # Create beautiful HTML email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f8f9fa; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, {status_color}, {status_color}dd); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
                .header h2 {{ margin: 10px 0 0 0; font-size: 18px; font-weight: 400; opacity: 0.9; }}
                .content {{ padding: 30px; }}
                .status-badge {{ display: inline-block; padding: 10px 20px; border-radius: 25px; background-color: {status_color}; color: white; font-weight: bold; margin-bottom: 25px; font-size: 14px; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 25px 0; }}
                .info-item {{ padding: 20px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid {status_color}; }}
                .info-label {{ font-weight: 600; color: #495057; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
                .info-value {{ color: #212529; font-size: 18px; margin-top: 8px; font-weight: 500; }}
                .summary-box {{ background: linear-gradient(135deg, #e3f2fd, #f3e5f5); border-radius: 10px; padding: 25px; margin: 25px 0; border-left: 5px solid #2196f3; }}
                .summary-box h3 {{ margin: 0 0 15px 0; color: #1976d2; font-size: 18px; }}
                .summary-box p {{ margin: 8px 0; color: #424242; }}
                .footer {{ text-align: center; padding: 25px; background-color: #f8f9fa; color: #6c757d; font-size: 14px; }}
                .error-box {{ background-color: #ffebee; border: 2px solid #f44336; color: #c62828; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .metrics {{ display: flex; justify-content: space-around; background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .metric {{ text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: {status_color}; }}
                .metric-label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{status_emoji} Clinical Genomics Pipeline</h1>
                    <h2>VEP Annotation {status_text}</h2>
                </div>
                <div class="content">
                    <div class="status-badge">{status_text}</div>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Sample ID</div>
                            <div class="info-value">{sample_id}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Processing Time</div>
                            <div class="info-value">{duration}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Started</div>
                            <div class="info-value">{start_time}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Completed</div>
                            <div class="info-value">{end_time}</div>
                        </div>
                    </div>
                    
                    {f'''
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">{variant_count:,}</div>
                            <div class="metric-label">Variants</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{file_size}</div>
                            <div class="metric-label">File Size</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">VCF</div>
                            <div class="metric-label">Output Format</div>
                        </div>
                    </div>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Output File</div>
                            <div class="info-value">{os.path.basename(output_file) if output_file else "N/A"}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Pipeline Stage</div>
                            <div class="info-value">VEP v114.2</div>
                        </div>
                    </div>
                    ''' if success else ''}
                    
                    {f'<div class="error-box"><strong>🚨 Error Details:</strong><br><br>{error_message}</div>' if error_message else ''}
                    
                    <div class="summary-box">
                        <h3>🧬 Pipeline Information</h3>
                        <p><strong>System:</strong> Clinical Genomics Pipeline v114.2</p>
                        <p><strong>Location:</strong> /mnt/d/Genome (WSL Ubuntu 22.04)</p>
                        <p><strong>Assembly:</strong> GRCh38</p>
                        <p><strong>Databases:</strong> gnomAD v4.1, ClinVar September 2025</p>
                        <p><strong>Next Steps:</strong> {('Multi-specialty analysis across 22 medical specialties will begin automatically' if success else 'Please check logs in /mnt/d/Genome/logs/ and restart pipeline')}</p>
                    </div>
                </div>
                <div class="footer">
                    <p><strong>Clinical Genomics Pipeline Notification System</strong></p>
                    <p>Generated on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
                    <p style="font-size: 12px; margin-top: 15px; color: #999;">
                        This is an automated notification. Research-grade analysis requires clinical validation.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version for email clients that don't support HTML
        text_content = f"""
═══════════════════════════════════════════════════════════════
         CLINICAL GENOMICS PIPELINE NOTIFICATION
═══════════════════════════════════════════════════════════════

{status_emoji} STATUS: {status_text}

SAMPLE DETAILS:
   Sample ID: {sample_id}
   Processing Time: {duration}
   Started: {start_time}
   Completed: {end_time}

"""
        
        if success:
            text_content += f"""
RESULTS:
   Output File: {os.path.basename(output_file) if output_file else "N/A"}
   File Size: {file_size if file_size else "N/A"}
   Variant Count: {variant_count:,} variants
   Pipeline Stage: VEP v114.2 Annotation

NEXT STEPS:
   ✓ Multi-specialty analysis will begin automatically
   ✓ Results will cover 22 medical specialties (626 genes)
   ✓ Clinical report will be generated upon completion
"""
        else:
            text_content += f"""
ERROR DETAILS:
   {error_message}

REQUIRED ACTIONS:
   1. Check log files in /mnt/d/Genome/logs/
   2. Review VEP configuration and input files
   3. Restart pipeline after resolving issues
"""
        
        text_content += f"""

SYSTEM INFORMATION:
   Pipeline: Clinical Genomics Pipeline v114.2
   Location: /mnt/d/Genome (WSL Ubuntu 22.04)
   Assembly: GRCh38
   Databases: gnomAD v4.1, ClinVar September 2025

═══════════════════════════════════════════════════════════════
Generated: {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
NOTE: Research-grade analysis requires clinical validation
═══════════════════════════════════════════════════════════════
        """
        
        return self.send_email(subject, text_content, html_content)
    
    def send_email(self, subject, text_content, html_content=None):
        """Send email notification"""
        try:
            # Create message
            if html_content:
                msg = MIMEMultipart('alternative')
                msg.attach(MIMEText(text_content, 'plain'))
                msg.attach(MIMEText(html_content, 'html'))
            else:
                msg = MIMEText(text_content)
            
            msg['Subject'] = subject
            msg['From'] = f"{self.config['sender_name']} <{self.config['email_user']}>"
            msg['To'] = self.config['recipient_email']
            
            # Connect to server and send email
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['email_user'], self.config['email_password'])
                server.send_message(msg)
            
            print(f"📧 Email notification sent successfully to {self.config['recipient_email']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email notification: {e}")
            print(f"    Check your email configuration and network connection")
            return False

def main():
    parser = argparse.ArgumentParser(description='Send pipeline completion notifications')
    parser.add_argument('--type', choices=['vep_completion', 'vep_failure'], required=True,
                       help='Type of notification to send')
    parser.add_argument('--sample-id', required=True, help='Sample identifier')
    parser.add_argument('--start-time', required=True, help='Pipeline start time')
    parser.add_argument('--end-time', help='Pipeline end time (current time if not provided)')
    parser.add_argument('--output-file', help='Output VCF file path')
    parser.add_argument('--file-size', help='Output file size')
    parser.add_argument('--variant-count', type=int, help='Number of variants processed')
    parser.add_argument('--error-message', help='Error message for failure notifications')
    parser.add_argument('--config', help='Path to email configuration file')
    
    args = parser.parse_args()
    
    # Initialize notifier
    notifier = PipelineNotifier(args.config)
    
    # Set end time to current if not provided
    end_time = args.end_time if args.end_time else datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    
    # Send appropriate notification
    if args.type == 'vep_completion':
        success = notifier.send_vep_completion_notification(
            sample_id=args.sample_id,
            start_time=args.start_time,
            end_time=end_time,
            output_file=args.output_file,
            file_size=args.file_size,
            variant_count=args.variant_count or 0,
            success=True
        )
    elif args.type == 'vep_failure':
        success = notifier.send_vep_completion_notification(
            sample_id=args.sample_id,
            start_time=args.start_time,
            end_time=end_time,
            output_file=args.output_file,
            file_size=args.file_size,
            variant_count=args.variant_count or 0,
            success=False,
            error_message=args.error_message
        )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
