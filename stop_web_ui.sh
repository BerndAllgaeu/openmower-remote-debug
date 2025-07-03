#!/bin/bash

# OpenMower Web UI Stop Script
# This script stops the web UI Docker containers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "Stopping OpenMower Web UI..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Navigate to docker directory
DOCKER_DIR="$WORKSPACE_ROOT/docker/development"
if [ ! -d "$DOCKER_DIR" ]; then
    echo "Error: Docker directory not found at $DOCKER_DIR"
    exit 1
fi

cd "$DOCKER_DIR"

echo "Stopping containers..."
$DOCKER_COMPOSE down nginx mosquitto

echo "✅ Web UI services stopped"

# Show remaining containers (if any)
REMAINING=$(docker ps --format "table {{.Names}}" | grep -E "(nginx_server|mosquitto_broker)" || true)
if [ -n "$REMAINING" ]; then
    echo "⚠️  Some containers are still running:"
    echo "$REMAINING"
else
    echo "All web UI containers have been stopped"
fi
