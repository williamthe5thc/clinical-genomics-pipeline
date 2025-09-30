#!/bin/bash
# Test SSH connection
WSL_IP=$(hostname -I | awk '{print $1}')
echo "Testing SSH connection to ${WSL_IP}:2022..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p 2022 ${USER}@${WSL_IP} "echo 'Connection successful!'"
