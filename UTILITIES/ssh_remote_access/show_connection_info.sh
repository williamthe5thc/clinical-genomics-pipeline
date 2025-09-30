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
