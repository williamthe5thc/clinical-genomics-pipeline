# PowerShell script to start WSL and SSH server
# Can be added to Windows Task Scheduler for auto-start on boot

Write-Host "Starting WSL and SSH server..." -ForegroundColor Cyan

# Start WSL (this also starts the default distribution)
wsl -d Ubuntu echo "WSL started"

# Start SSH service in WSL
wsl -d Ubuntu sudo service ssh start

# Check SSH status
$status = wsl -d Ubuntu sudo service ssh status
if ($status -match "running") {
    Write-Host "SSH service started successfully!" -ForegroundColor Green
} else {
    Write-Host "Failed to start SSH service" -ForegroundColor Red
    Write-Host $status
    exit 1
}

# Get WSL IP
$wslIP = wsl -d Ubuntu hostname -I
Write-Host "WSL IP Address: $wslIP" -ForegroundColor Yellow

# Setup port forwarding
Write-Host "Setting up port forwarding..." -ForegroundColor Cyan
$wslIP = $wslIP.Trim()

# Remove existing rule
netsh interface portproxy delete v4tov4 listenport=2022 listenaddress=0.0.0.0 2>$null

# Add new rule
netsh interface portproxy add v4tov4 listenport=2022 listenaddress=0.0.0.0 connectport=2022 connectaddress=$wslIP

Write-Host "Port forwarding configured!" -ForegroundColor Green
Write-Host "You can now SSH to this computer on port 2022" -ForegroundColor Green
