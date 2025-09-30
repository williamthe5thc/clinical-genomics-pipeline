#!/bin/bash
#
# Make Utility Scripts Executable
# ================================
# Ensures all utility scripts have correct permissions
#

echo "Setting executable permissions for utility scripts..."

# VCF Downloader
chmod +x /mnt/d/Genome/UTILITIES/vcf_downloader/vcf_downloader.py
echo "✓ vcf_downloader.py"

# SSH Remote Access
chmod +x /mnt/d/Genome/UTILITIES/ssh_remote_access/setup_ssh_access.sh
chmod +x /mnt/d/Genome/UTILITIES/ssh_remote_access/restart_ssh.sh
chmod +x /mnt/d/Genome/UTILITIES/ssh_remote_access/test_ssh_connection.sh
chmod +x /mnt/d/Genome/UTILITIES/ssh_remote_access/show_connection_info.sh
chmod +x /mnt/d/Genome/UTILITIES/ssh_remote_access/setup_port_forwarding.bat
chmod +x /mnt/d/Genome/UTILITIES/ssh_remote_access/start_wsl_ssh.ps1
echo "✓ ssh_remote_access scripts"

echo ""
echo "All utility scripts are now executable!"
