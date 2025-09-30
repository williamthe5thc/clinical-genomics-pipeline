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
echo   ssh william@%COMPUTERNAME% -p 2022
echo   OR
echo   ssh william@YOUR_WINDOWS_IP -p 2022
echo.
echo Press any key to exit...
pause >nul
