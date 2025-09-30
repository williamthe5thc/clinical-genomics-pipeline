#!/bin/bash
#
# Quick Start Guide for Clinical Genomics Pipeline Utilities
# ===========================================================
# Interactive setup wizard for all utilities
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}║     Clinical Genomics Pipeline - Utilities Quick Start       ║${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "This wizard will help you set up:"
echo "  1. VCF Downloader - Download samples from URLs/Excel"
echo "  2. SSH Remote Access - Access pipeline from anywhere"
echo "  3. Email Notifications - Get alerts when analyses complete"
echo ""
read -p "Press Enter to begin setup..."

# ============================================================================
# Step 1: Verify Installation
# ============================================================================
clear
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 1: Verifying Installation${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

cd /mnt/d/Genome/UTILITIES

# Make scripts executable
echo "Making scripts executable..."
bash make_executable.sh 2>/dev/null
echo ""

# Run verification
echo "Running system verification..."
echo ""
bash verify_utilities.sh

echo ""
read -p "Press Enter to continue..."

# ============================================================================
# Step 2: VCF Downloader Setup
# ============================================================================
clear
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 2: VCF Downloader Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo "The VCF Downloader helps you download genomic files from:"
echo "  • Individual URLs"
echo "  • Excel spreadsheets with multiple download links"
echo "  • Public databases and collaborator servers"
echo ""

read -p "Do you want to test the VCF Downloader? (y/n): " TEST_VCF

if [ "$TEST_VCF" = "y" ] || [ "$TEST_VCF" = "Y" ]; then
    echo ""
    echo "Testing VCF Downloader..."
    cd vcf_downloader
    
    # Check if Python packages are installed
    if python3 -c "import requests, pandas" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Python packages installed"
        echo ""
        echo "Example commands:"
        echo ""
        echo "1. Download single VCF:"
        echo "   python3 vcf_downloader.py --url https://example.com/sample.vcf.gz"
        echo ""
        echo "2. Download from Excel file:"
        echo "   python3 vcf_downloader.py --excel download_list.xlsx"
        echo ""
        echo "3. See template file:"
        echo "   cat example_download_list.csv"
        echo ""
    else
        echo -e "${RED}✗${NC} Missing Python packages"
        echo ""
        read -p "Install required packages now? (y/n): " INSTALL_PACKAGES
        if [ "$INSTALL_PACKAGES" = "y" ]; then
            pip install requests pandas openpyxl
        fi
    fi
    
    cd ..
fi

echo ""
read -p "Press Enter to continue..."

# ============================================================================
# Step 3: SSH Remote Access Setup
# ============================================================================
clear
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 3: SSH Remote Access Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo "SSH Remote Access allows you to:"
echo "  • Access your pipeline from home, lab, or while traveling"
echo "  • Monitor long-running analyses remotely"
echo "  • Collaborate with remote team members"
echo "  • Run analyses from your laptop"
echo ""

read -p "Do you want to setup SSH Remote Access? (y/n): " SETUP_SSH

if [ "$SETUP_SSH" = "y" ] || [ "$SETUP_SSH" = "Y" ]; then
    echo ""
    echo -e "${YELLOW}Important:${NC} This will install and configure OpenSSH server."
    read -p "Continue? (y/n): " CONFIRM_SSH
    
    if [ "$CONFIRM_SSH" = "y" ]; then
        cd ssh_remote_access
        bash setup_ssh_access.sh
        cd ..
        
        echo ""
        echo -e "${GREEN}✓${NC} SSH setup complete!"
        echo ""
        echo -e "${YELLOW}Next step:${NC} Configure Windows port forwarding"
        echo "  1. Open PowerShell as Administrator"
        echo "  2. Run: cd D:\\Genome\\UTILITIES\\ssh_remote_access"
        echo "  3. Run: .\\setup_port_forwarding.bat"
        echo ""
    fi
fi

echo ""
read -p "Press Enter to continue..."

# ============================================================================
# Step 4: Email Notifications Setup
# ============================================================================
clear
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 4: Email Notifications Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Email Notifications will send you alerts when:"
echo "  • VEP annotation completes (~3 hours for whole genome)"
echo "  • Pipeline finishes successfully"
echo "  • Pipeline encounters an error"
echo ""
echo "This is especially useful for:"
echo "  • Overnight/weekend runs"
echo "  • Batch processing multiple samples"
echo "  • Remote monitoring"
echo ""

read -p "Do you want to setup Email Notifications? (y/n): " SETUP_EMAIL

if [ "$SETUP_EMAIL" = "y" ] || [ "$SETUP_EMAIL" = "Y" ]; then
    if [ -d "email_notifications" ]; then
        cd email_notifications
        bash setup_email_notifications.sh
        cd ..
    else
        echo -e "${YELLOW}⚠${NC} Email notifications directory not found"
        echo "This feature may not be available in your installation"
    fi
fi

echo ""
read -p "Press Enter to continue..."

# ============================================================================
# Final Summary
# ============================================================================
clear
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}║                    Setup Complete! ✓                          ║${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Your utilities are now ready to use!"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}Quick Reference Commands${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}VCF Downloader:${NC}"
echo "  python3 vcf_downloader/vcf_downloader.py --url https://example.com/file.vcf.gz"
echo "  python3 vcf_downloader/vcf_downloader.py --excel download_list.xlsx"
echo ""
echo -e "${YELLOW}SSH Remote Access:${NC}"
echo "  ssh YOUR_USERNAME@localhost -p 2022  (test local)"
echo "  ssh YOUR_USERNAME@YOUR_IP -p 2022     (remote access)"
echo "  bash ssh_remote_access/show_connection_info.sh"
echo ""
echo -e "${YELLOW}Email Notifications:${NC}"
echo "  bash email_notifications/test_email_integration.sh"
echo "  (Automatically sent during pipeline runs)"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Example Workflow:${NC}"
echo ""
echo "1. Download VCFs from collaborator:"
echo "   python3 vcf_downloader/vcf_downloader.py --excel samples.xlsx"
echo ""
echo "2. Connect remotely (if away from computer):"
echo "   ssh user@server -p 2022"
echo ""
echo "3. Start pipeline in screen session:"
echo "   screen -S analysis"
echo "   cd /mnt/d/Genome"
echo "   bash clinical_genomics_pipeline.sh batch DATA/downloaded_vcfs/ 8"
echo "   # Press Ctrl+A then D to detach"
echo ""
echo "4. Receive email when complete!"
echo ""
echo "5. Download results:"
echo "   scp -P 2022 -r user@server:/mnt/d/Genome/DATA/RESULTS/ ./"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "  Main README:    cat UTILITIES/README.md"
echo "  VCF Downloader: cat vcf_downloader/README.md"
echo "  SSH Access:     cat ssh_remote_access/README.md"
echo "  Security:       cat ssh_remote_access/SECURITY_GUIDE.md"
echo ""
echo -e "${YELLOW}Troubleshooting:${NC}"
echo "  Verify setup:   bash verify_utilities.sh"
echo "  Check logs:     Check individual utility log files"
echo ""
echo -e "${GREEN}Happy analyzing! 🧬${NC}"
echo ""
