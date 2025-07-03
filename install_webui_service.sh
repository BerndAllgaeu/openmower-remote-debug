#!/bin/bash

# OpenMower Web UI Service Installation Script
# This script installs the web UI as a systemd service

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/openmower-webui.service"
SERVICE_NAME="openmower-webui"

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root (use sudo)"
    exit 1
fi

echo "Installing OpenMower Web UI as systemd service..."

# Check if service file exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo "Error: Service file not found at $SERVICE_FILE"
    exit 1
fi

# Stop service if it's running
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Stopping existing service..."
    systemctl stop "$SERVICE_NAME"
fi

# Copy service file
echo "Installing service file..."
cp "$SERVICE_FILE" "/etc/systemd/system/"

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

# Enable service
echo "Enabling service..."
systemctl enable "$SERVICE_NAME"

# Start service
echo "Starting service..."
systemctl start "$SERVICE_NAME"

# Check status
sleep 2
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "✅ Service installed and started successfully"
    echo ""
    echo "Service commands:"
    echo "  Status:  sudo systemctl status $SERVICE_NAME"
    echo "  Start:   sudo systemctl start $SERVICE_NAME" 
    echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
    echo "  Restart: sudo systemctl restart $SERVICE_NAME"
    echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
    echo ""
    echo "The web UI will now start automatically on boot."
else
    echo "❌ Service failed to start"
    echo "Check logs with: sudo journalctl -u $SERVICE_NAME"
    exit 1
fi
