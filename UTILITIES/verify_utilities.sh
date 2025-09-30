#!/bin/bash
#
# Utilities Suite Verification Script
# ====================================
# Verifies that all utilities are properly installed and configured
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
}

print_check() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Main verification
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     Clinical Genomics Pipeline - Utilities Verification      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"

ISSUES_FOUND=0

# ============================================================================
# 1. VCF Downloader Verification
# ============================================================================
print_header "1. VCF Downloader"

# Check if Python is available
if command -v python3 &> /dev/null; then
    print_check 0 "Python 3 installed"
    PYTHON_VERSION=$(python3 --version)
    print_info "Version: $PYTHON_VERSION"
else
    print_check 1 "Python 3 not found"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check required Python packages
echo ""
echo "Python packages:"
for package in requests pandas openpyxl; do
    if python3 -c "import $package" 2>/dev/null; then
        print_check 0 "$package installed"
    else
        print_check 1 "$package not installed"
        print_warning "Install with: pip install $package"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
done

# Check if vcf_downloader.py exists and is executable
echo ""
if [ -f "/mnt/d/Genome/UTILITIES/vcf_downloader/vcf_downloader.py" ]; then
    print_check 0 "vcf_downloader.py exists"
    
    if [ -x "/mnt/d/Genome/UTILITIES/vcf_downloader/vcf_downloader.py" ]; then
        print_check 0 "vcf_downloader.py is executable"
    else
        print_check 1 "vcf_downloader.py not executable"
        print_warning "Run: chmod +x /mnt/d/Genome/UTILITIES/vcf_downloader/vcf_downloader.py"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    print_check 1 "vcf_downloader.py not found"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check output directory
if [ -d "/mnt/d/Genome/DATA/downloaded_vcfs" ]; then
    print_check 0 "Output directory exists"
else
    print_warning "Output directory will be created automatically"
fi

# ============================================================================
# 2. SSH Remote Access Verification
# ============================================================================
print_header "2. SSH Remote Access"

# Check if OpenSSH server is installed
if dpkg -l | grep -q openssh-server; then
    print_check 0 "OpenSSH Server installed"
else
    print_check 1 "OpenSSH Server not installed"
    print_warning "Run: sudo apt-get install openssh-server"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check if SSH service is running
if sudo service ssh status &> /dev/null; then
    if sudo service ssh status | grep -q "running"; then
        print_check 0 "SSH service is running"
        
        # Check if listening on port 2022
        if sudo netstat -tulpn 2>/dev/null | grep -q ":2022"; then
            print_check 0 "SSH listening on port 2022"
        elif sudo netstat -tulpn 2>/dev/null | grep -q ":22"; then
            print_warning "SSH listening on port 22 (default port)"
            print_info "Consider configuring custom port 2022"
        fi
    else
        print_check 1 "SSH service not running"
        print_warning "Run: sudo service ssh start"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    print_warning "SSH service not configured"
fi

# Check SSH scripts
echo ""
echo "SSH scripts:"
SCRIPTS=("setup_ssh_access.sh" "restart_ssh.sh" "test_ssh_connection.sh" "show_connection_info.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "/mnt/d/Genome/UTILITIES/ssh_remote_access/$script" ]; then
        print_check 0 "$script exists"
    else
        print_check 1 "$script not found"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
done

# Check WSL version
echo ""
WSL_VERSION=$(grep -qi "WSL2" /proc/version 2>/dev/null && echo "2" || echo "1")
print_info "WSL Version: $WSL_VERSION"

if [ "$WSL_VERSION" = "2" ]; then
    print_warning "WSL2 requires port forwarding configuration on Windows"
    print_info "Run: D:\\Genome\\UTILITIES\\ssh_remote_access\\setup_port_forwarding.bat"
fi

# Get WSL IP
WSL_IP=$(hostname -I | awk '{print $1}')
print_info "WSL IP Address: $WSL_IP"

# ============================================================================
# 3. Email Notifications Verification
# ============================================================================
print_header "3. Email Notifications"

# Check if email notification files exist
if [ -d "/mnt/d/Genome/UTILITIES/email_notifications" ]; then
    print_check 0 "Email notifications directory exists"
    
    if [ -f "/mnt/d/Genome/UTILITIES/email_notifications/email_config.json" ]; then
        print_check 0 "Email configuration file exists"
        
        # Check if configured
        if grep -q '"smtp_server": "smtp.gmail.com"' /mnt/d/Genome/UTILITIES/email_notifications/email_config.json 2>/dev/null; then
            print_info "Email notifications appear configured"
            print_warning "Test with: bash email_notifications/test_email_integration.sh"
        else
            print_warning "Email notifications not configured"
            print_info "Run: bash email_notifications/setup_email_notifications.sh"
        fi
    else
        print_warning "Email configuration not found"
        print_info "Run: bash email_notifications/setup_email_notifications.sh"
    fi
else
    print_check 1 "Email notifications directory not found"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# ============================================================================
# 4. General Checks
# ============================================================================
print_header "4. General System Checks"

# Check internet connectivity
echo "Testing internet connectivity..."
if ping -c 1 8.8.8.8 &> /dev/null; then
    print_check 0 "Internet connection available"
else
    print_check 1 "No internet connection"
    print_warning "Required for VCF downloads and remote access"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check disk space
AVAILABLE_SPACE=$(df -h /mnt/d | awk 'NR==2 {print $4}')
print_info "Available disk space on /mnt/d: $AVAILABLE_SPACE"

# Check if main pipeline exists
echo ""
if [ -f "/mnt/d/Genome/PIPELINES/VCF_PIPELINE/clinical_genomics_pipeline.sh" ]; then
    print_check 0 "Main pipeline found"
else
    print_warning "Main pipeline not found at expected location"
fi

# ============================================================================
# Summary
# ============================================================================
print_header "Verification Summary"

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✓ All utilities verified successfully!              ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Download VCFs: python vcf_downloader/vcf_downloader.py --help"
    echo "  2. Remote access: bash ssh_remote_access/setup_ssh_access.sh"
    echo "  3. Email alerts:  bash email_notifications/setup_email_notifications.sh"
else
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠ $ISSUES_FOUND issue(s) found - see details above        ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Common fixes:"
    echo "  • Install Python packages: pip install requests pandas openpyxl"
    echo "  • Install SSH: sudo apt-get install openssh-server"
    echo "  • Make scripts executable: bash make_executable.sh"
    echo "  • Run setup scripts in each utility directory"
fi

echo ""
echo "Full documentation: /mnt/d/Genome/UTILITIES/README.md"
echo ""
