#!/bin/bash
# Restart SSH service and show status
echo "Restarting SSH service..."
sudo service ssh restart
sleep 2
sudo service ssh status
