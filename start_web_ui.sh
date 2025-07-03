#!/bin/bash

# OpenMower Web UI Startup Script
# This script starts the web UI using Docker on the Raspberry Pi

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "Starting OpenMower Web UI..."
echo "Workspace: $WORKSPACE_ROOT"

# Check if we're running on the Pi (can be skipped for local testing)
if [[ "$1" != "--local" ]] && ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "Warning: This script is intended to run on a Raspberry Pi"
    echo "Use --local flag to run anyway"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if web directory exists
if [ ! -d "$WORKSPACE_ROOT/web" ]; then
    echo "Error: Web directory not found at $WORKSPACE_ROOT/web"
    echo "Make sure you're running this from the correct workspace"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    echo "Please install Docker first: https://docs.docker.com/engine/install/"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Warning: docker-compose not found, trying docker compose"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running"
    echo "Please start Docker first: sudo systemctl start docker"
    exit 1
fi

# Navigate to docker directory
DOCKER_DIR="$WORKSPACE_ROOT/docker/development"
if [ ! -d "$DOCKER_DIR" ]; then
    echo "Error: Docker directory not found at $DOCKER_DIR"
    exit 1
fi

cd "$DOCKER_DIR"

echo "Using Docker directory: $DOCKER_DIR"

# Stop any existing containers
echo "Stopping existing containers..."
$DOCKER_COMPOSE down nginx mosquitto 2>/dev/null || true

# Pull latest images if requested
if [[ "$1" == "--pull" ]] || [[ "$2" == "--pull" ]]; then
    echo "Pulling latest Docker images..."
    $DOCKER_COMPOSE pull nginx mosquitto
fi

# Start only the web UI and MQTT services
echo "Starting web UI (nginx) and MQTT broker..."
$DOCKER_COMPOSE up -d nginx mosquitto

# Wait a moment for containers to start
echo "Waiting for containers to start..."
sleep 3

# Check if containers are running
NGINX_RUNNING=false
MQTT_RUNNING=false

if docker ps --format "table {{.Names}}" | grep -q "nginx_server"; then
    NGINX_RUNNING=true
    LOCAL_IP=$(hostname -I | awk '{print $1}' | head -n1)
    echo "✅ Web UI is running on port 8080"
    echo "   Access it at: http://${LOCAL_IP}:8080"
    echo "   Or via localhost: http://localhost:8080"
else
    echo "❌ Failed to start web UI (nginx)"
fi

if docker ps --format "table {{.Names}}" | grep -q "mosquitto_broker"; then
    MQTT_RUNNING=true
    echo "✅ MQTT broker is running on port 1883"
else
    echo "⚠️  MQTT broker failed to start"
fi

# Show container status
echo ""
echo "Container status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(nginx_server|mosquitto_broker|NAMES)"

# Show logs if something failed
if [ "$NGINX_RUNNING" = false ]; then
    echo ""
    echo "Nginx container logs:"
    docker logs nginx_server 2>/dev/null || echo "No logs available"
fi

if [ "$MQTT_RUNNING" = false ]; then
    echo ""
    echo "Mosquitto container logs:"
    docker logs mosquitto_broker 2>/dev/null || echo "No logs available"
fi

echo ""
if [ "$NGINX_RUNNING" = true ]; then
    echo "🎉 Web UI startup complete!"
    echo ""
    echo "Commands:"
    echo "  Stop services: cd '$DOCKER_DIR' && $DOCKER_COMPOSE down"
    echo "  View logs:     cd '$DOCKER_DIR' && $DOCKER_COMPOSE logs -f"
    echo "  Restart:       cd '$DOCKER_DIR' && $DOCKER_COMPOSE restart nginx mosquitto"
else
    echo "❌ Web UI failed to start properly"
    echo "Check the logs above for more information"
    exit 1
fi
