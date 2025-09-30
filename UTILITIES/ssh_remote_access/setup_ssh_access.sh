#!/bin/bash
#
# SSH Remote Access Setup for WSL Ubuntu
# =======================================
# Enables secure SSH access to your Clinical Genomics Pipeline from remote locations
#
# This script automates the setup of SSH server in WSL with port forwarding
# to allow remote access from other computers on your network or via internet.
#
# Author: Clinical Genomics Pipeline Team
# Version: 1.0
# Date: September 2025
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Function to check if running in WSL
check_wsl() {
    if ! grep -qi microsoft /proc/version 2>/dev/null; then
        print_error "This script must be run in WSL (Windows Subsystem for Linux)"
        exit 1
    fi
    print_success "Running in WSL environment"
}

# Function to detect WSL version
detect_wsl_version() {
    if grep -qi "WSL2" /proc/version 2>/dev/null; then
        echo "2"
    else
        echo "1"
    fi
}

# Header
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     SSH Remote Access Setup for Clinical Genomics Pipeline    ║"
echo "║                     WSL Ubuntu Configuration                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check WSL environment
print_info "Step 1: Verifying WSL environment..."
check_wsl
WSL_VERSION=$(detect_wsl_version)
print_info "Detected WSL version: ${WSL_VERSION}"
echo ""

# Step 2: Update system
print_info "Step 2: Updating system packages..."
sudo apt-get update -qq
print_success "System packages updated"
echo ""

# Step 3: Install OpenSSH Server
print_info "Step 3: Installing OpenSSH Server..."
if dpkg -l | grep -q openssh-server; then
    print_warning "OpenSSH Server already installed"
else
    sudo apt-get install -y openssh-server
    print_success "OpenSSH Server installed"
fi
echo ""

# Step 4: Configure SSH
print_info "Step 4: Configuring SSH server..."

# Backup original config
if [ ! -f /etc/ssh/sshd_config.backup ]; then
    sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
    print_info "Created backup: /etc/ssh/sshd_config.backup"
fi

# Configure SSH settings
sudo sed -i 's/#Port 22/Port 2022/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

# Add custom configuration
if ! grep -q "# Clinical Genomics Pipeline SSH Config" /etc/ssh/sshd_config; then
    sudo tee -a /etc/ssh/sshd_config > /dev/null <<EOF

# Clinical Genomics Pipeline SSH Config
# Added by setup script $(date +%Y-%m-%d)
Port 2022
ListenAddress 0.0.0.0
PasswordAuthentication yes
PubkeyAuthentication yes
PermitRootLogin no
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
EOF
    print_success "SSH configuration updated"
else
    print_warning "Custom SSH configuration already exists"
fi
echo ""

# Step 5: Start SSH service
print_info "Step 5: Starting SSH service..."
sudo service ssh start
sleep 2

# Verify SSH is running
if sudo service ssh status | grep -q "running"; then
    print_success "SSH service is running"
else
    print_error "Failed to start SSH service"
    print_info "Checking for errors..."
    sudo service ssh status
    exit 1
fi
echo ""

# Step 6: Get IP addresses
print_info "Step 6: Network configuration..."
WSL_IP=$(hostname -I | awk '{print $1}')
print_info "WSL IP Address: ${WSL_IP}"

# Try to get Windows IP
WINDOWS_IP=""
if command -v powershell.exe &> /dev/null; then
    WINDOWS_IP=$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Ethernet*','Wi-Fi*' | Where-Object {\$_.IPAddress -notlike '169.*'} | Select-Object -First 1).IPAddress" 2>/dev/null | tr -d '\r')
    if [ -n "$WINDOWS_IP" ]; then
        print_info "Windows IP Address: ${WINDOWS_IP}"
    fi
fi
echo ""

# Step 7: Test local SSH connection
print_info "Step 7: Testing local SSH connection..."
print_info "Attempting to connect to localhost..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p 2022 ${USER}@localhost "echo 'SSH connection successful!'" 2>/dev/null && print_success "Local SSH test successful!" || print_warning "Local SSH test failed (this is normal, will configure port forwarding)"
echo ""

# Step 8: Generate Windows PowerShell commands for port forwarding
print_info "Step 8: Generating Windows configuration commands..."

CONFIG_DIR="/mnt/d/Genome/UTILITIES/ssh_remote_access"
mkdir -p "${CONFIG_DIR}"

# Create Windows batch file for port forwarding
cat > "${CONFIG_DIR}/setup_port_forwarding.bat" <<EOF
@echo off
REM SSH Port Forwarding Setup for WSL
REM Run this file as Administrator in Windows

echo ===============================================
echo SSH Port Forwarding Setup for WSL
echo ===============================================
echo.

REM Get WSL IP address
for /f %%i in ('wsl hostname -I') do set WSL_IP=%%i
echo WSL IP Address: %WSL_IP%

REM Remove existing port forwarding (if any)
echo Removing existing port forwarding rules...
netsh interface portproxy delete v4tov4 listenport=2022 listenaddress=0.0.0.0 2>nul

REM Add new port forwarding rule
echo Adding port forwarding: Windows:2022 -^> WSL:%WSL_IP%:2022
netsh interface portproxy add v4tov4 listenport=2022 listenaddress=0.0.0.0 connectport=2022 connectaddress=%WSL_IP%

REM Check if rule was added
netsh interface portproxy show v4tov4 | findstr "2022"
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Port forwarding configured!
) else (
    echo ERROR: Failed to configure port forwarding
    exit /b 1
)

echo.
echo Configuring Windows Firewall...
REM Add firewall rule
netsh advfirewall firewall delete rule name="WSL SSH" 2>nul
netsh advfirewall firewall add rule name="WSL SSH" dir=in action=allow protocol=TCP localport=2022

echo.
echo ===============================================
echo Configuration Complete!
echo ===============================================
echo.
echo To connect from another computer:
echo   ssh ${USER}@%COMPUTERNAME% -p 2022
echo   OR
echo   ssh ${USER}@YOUR_WINDOWS_IP -p 2022
echo.
echo Press any key to exit...
pause >nul
EOF

chmod +x "${CONFIG_DIR}/setup_port_forwarding.bat"
print_success "Created Windows configuration script"
print_info "Location: ${CONFIG_DIR}/setup_port_forwarding.bat"
echo ""

# Create PowerShell script for auto-start
cat > "${CONFIG_DIR}/start_wsl_ssh.ps1" <<EOF
# PowerShell script to start WSL and SSH server
# Can be added to Windows Task Scheduler for auto-start on boot

Write-Host "Starting WSL and SSH server..." -ForegroundColor Cyan

# Start WSL (this also starts the default distribution)
wsl -d Ubuntu echo "WSL started"

# Start SSH service in WSL
wsl -d Ubuntu sudo service ssh start

# Check SSH status
\$status = wsl -d Ubuntu sudo service ssh status
if (\$status -match "running") {
    Write-Host "SSH service started successfully!" -ForegroundColor Green
} else {
    Write-Host "Failed to start SSH service" -ForegroundColor Red
    Write-Host \$status
    exit 1
}

# Get WSL IP
\$wslIP = wsl -d Ubuntu hostname -I
Write-Host "WSL IP Address: \$wslIP" -ForegroundColor Yellow

# Setup port forwarding
Write-Host "Setting up port forwarding..." -ForegroundColor Cyan
\$wslIP = \$wslIP.Trim()

# Remove existing rule
netsh interface portproxy delete v4tov4 listenport=2022 listenaddress=0.0.0.0 2>\$null

# Add new rule
netsh interface portproxy add v4tov4 listenport=2022 listenaddress=0.0.0.0 connectport=2022 connectaddress=\$wslIP

Write-Host "Port forwarding configured!" -ForegroundColor Green
Write-Host "You can now SSH to this computer on port 2022" -ForegroundColor Green
EOF

chmod +x "${CONFIG_DIR}/start_wsl_ssh.ps1"
print_success "Created PowerShell auto-start script"
print_info "Location: ${CONFIG_DIR}/start_wsl_ssh.ps1"
echo ""

# Create systemd service (if systemd is available)
if command -v systemctl &> /dev/null; then
    print_info "Creating systemd service for SSH auto-start..."
    
    # Note: This requires systemd support in WSL (Windows 11 or specific WSL config)
    print_warning "Systemd detected - you can enable SSH auto-start with:"
    print_info "  sudo systemctl enable ssh"
    print_info "  sudo systemctl start ssh"
fi
echo ""

# Step 9: Create convenience scripts
print_info "Step 9: Creating convenience scripts..."

# Create SSH restart script
cat > "${CONFIG_DIR}/restart_ssh.sh" <<'EOF'
#!/bin/bash
# Restart SSH service and show status
echo "Restarting SSH service..."
sudo service ssh restart
sleep 2
sudo service ssh status
EOF
chmod +x "${CONFIG_DIR}/restart_ssh.sh"

# Create connection test script
cat > "${CONFIG_DIR}/test_ssh_connection.sh" <<'EOF'
#!/bin/bash
# Test SSH connection
WSL_IP=$(hostname -I | awk '{print $1}')
echo "Testing SSH connection to ${WSL_IP}:2022..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p 2022 ${USER}@${WSL_IP} "echo 'Connection successful!'"
EOF
chmod +x "${CONFIG_DIR}/test_ssh_connection.sh"

# Create connection info script
cat > "${CONFIG_DIR}/show_connection_info.sh" <<'EOF'
#!/bin/bash
# Display connection information

echo "╔════════════════════════════════════════════════════════╗"
echo "║         SSH Connection Information                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

WSL_IP=$(hostname -I | awk '{print $1}')
echo "WSL IP Address:     ${WSL_IP}"

if command -v powershell.exe &> /dev/null; then
    WINDOWS_IP=$(powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {\$_.IPAddress -notlike '169.*' -and \$_.IPAddress -notlike '127.*'} | Select-Object -First 1).IPAddress" 2>/dev/null | tr -d '\r')
    echo "Windows IP Address: ${WINDOWS_IP}"
fi

echo ""
echo "To connect from same machine:"
echo "  ssh ${USER}@localhost -p 2022"
echo ""
echo "To connect from local network:"
echo "  ssh ${USER}@WINDOWS_IP -p 2022"
echo ""
echo "SSH Status:"
sudo service ssh status | grep "Active:"
echo ""
EOF
chmod +x "${CONFIG_DIR}/show_connection_info.sh"

print_success "Convenience scripts created"
echo ""

# Final summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! ✓                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
print_success "SSH server is configured and running!"
echo ""
print_info "Next Steps:"
echo ""
echo "1. Configure Windows Port Forwarding (REQUIRED for remote access):"
echo "   ${YELLOW}Run as Administrator in Windows PowerShell:${NC}"
echo "   cd D:\\Genome\\UTILITIES\\ssh_remote_access"
echo "   .\\setup_port_forwarding.bat"
echo ""
echo "2. Test local connection:"
echo "   ssh ${USER}@localhost -p 2022"
echo ""
echo "3. Test remote connection (from another computer on same network):"
echo "   ssh ${USER}@YOUR_WINDOWS_IP -p 2022"
echo ""
print_info "Convenience Scripts:"
echo "   Restart SSH:       bash ${CONFIG_DIR}/restart_ssh.sh"
echo "   Test Connection:   bash ${CONFIG_DIR}/test_ssh_connection.sh"
echo "   Show Info:         bash ${CONFIG_DIR}/show_connection_info.sh"
echo ""
print_warning "Security Recommendations:"
echo "   - Use SSH key authentication (see README for setup)"
echo "   - Consider changing default port 2022"
echo "   - Use strong passwords"
echo "   - Enable firewall rules appropriately"
echo "   - Review ${CONFIG_DIR}/SECURITY_GUIDE.md"
echo ""
print_info "For troubleshooting and advanced configuration, see:"
echo "   ${CONFIG_DIR}/README.md"
echo ""
print_success "Setup script completed successfully!"
echo ""
