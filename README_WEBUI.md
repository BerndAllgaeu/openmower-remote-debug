# OpenMower Web UI Management Scripts

This directory contains scripts to manage the OpenMower Web UI service on the Raspberry Pi.

## Prerequisites

- Docker and docker-compose installed on the Raspberry Pi
- OpenMower ROS workspace properly set up
- Web UI files available in the `web/` directory

## Scripts

### `start_web_ui.sh`
Starts the OpenMower Web UI using Docker containers (nginx + mosquitto).

**Usage:**
```bash
# On Raspberry Pi
./start_web_ui.sh

# For local testing (skips Pi detection)
./start_web_ui.sh --local

# Pull latest Docker images before starting
./start_web_ui.sh --pull
```

**What it does:**
- Validates environment (Docker, web files, etc.)
- Stops any existing containers
- Starts nginx (port 8080) and mosquitto (port 1883) containers
- Shows access URLs and container status

### `stop_web_ui.sh`
Stops the Web UI Docker containers.

**Usage:**
```bash
./stop_web_ui.sh
```

### `install_webui_service.sh`
Installs the Web UI as a systemd service for automatic startup.

**Usage:**
```bash
# Must be run as root
sudo ./install_webui_service.sh
```

**What it does:**
- Installs systemd service file to `/etc/systemd/system/openmower-webui.service`
- Enables automatic startup on boot
- Starts the service immediately

**Service Management:**
```bash
# Check service status
sudo systemctl status openmower-webui

# Start/stop service
sudo systemctl start openmower-webui
sudo systemctl stop openmower-webui

# Restart service
sudo systemctl restart openmower-webui

# View service logs
sudo journalctl -u openmower-webui -f

# Disable automatic startup
sudo systemctl disable openmower-webui
```

## Web UI Access

Once running, the Web UI is accessible at:
- `http://<raspberry-pi-ip>:8080` (from any device on the network)
- `http://localhost:8080` (from the Pi itself)

## MQTT Broker

The scripts also start an MQTT broker (Mosquitto) on port 1883, which is used by the OpenMower system for communication.

## Troubleshooting

### Container Issues
```bash
# View container logs
cd /path/to/open_mower_ros/docker/development
docker-compose logs nginx
docker-compose logs mosquitto

# Restart containers
docker-compose restart nginx mosquitto

# Force recreate containers
docker-compose down
docker-compose up -d nginx mosquitto
```

### Docker Issues
```bash
# Check Docker status
sudo systemctl status docker

# Start Docker if stopped
sudo systemctl start docker

# Check available images
docker images

# Remove old containers
docker container prune
```

### Network Issues
```bash
# Check if ports are in use
sudo netstat -tlnp | grep :8080
sudo netstat -tlnp | grep :1883

# Test web UI from Pi
curl -I http://localhost:8080

# Check firewall (if applicable)
sudo ufw status
```

## Directory Structure

```
devel/debug-tools/
├── start_web_ui.sh          # Main startup script
├── stop_web_ui.sh           # Stop script
├── install_webui_service.sh # Service installer
├── openmower-webui.service  # Systemd service template
└── README_WEBUI.md          # This documentation
```

## Notes

- The scripts are designed to be run from the debug-tools directory
- They automatically detect the workspace root and navigate to the correct Docker directory
- The systemd service assumes the workspace is at `/home/ubuntu/open_mower_ros/`
- The Web UI is a Flutter web application served by nginx
- MQTT communication is handled by the Mosquitto broker
