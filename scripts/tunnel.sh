#!/bin/bash
set -e

# SSH Tunnel Setup für OpenMower Remote Debug
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"  # Von devel/debug nach workspace root

# Config laden
source <(python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/.debug')
from config import REMOTE_CONFIG
print(f'REMOTE_HOST={REMOTE_CONFIG[\"host\"]}')
print(f'REMOTE_USER={REMOTE_CONFIG[\"user\"]}')
print(f'REMOTE_PASSWORD={REMOTE_CONFIG[\"password\"]}')
")

echo "🌐 Setting up SSH tunnels for Remote Debug..."

# Prüfe ob sshpass verfügbar ist
if ! command -v sshpass >/dev/null; then
    echo "❌ sshpass nicht gefunden. Installieren: sudo apt install sshpass"
    exit 1
fi

# Tunnel für GDB Server (1234)
echo "🔧 Starting GDB tunnel (localhost:1234 -> $REMOTE_HOST:1234)..."
sshpass -p "$REMOTE_PASSWORD" ssh -o StrictHostKeyChecking=no \
    -L 1234:localhost:1234 \
    -N -f "$REMOTE_USER@$REMOTE_HOST" || true

# Tunnel für ROS Master (11311)
echo "🔧 Starting ROS Master tunnel (localhost:11311 -> $REMOTE_HOST:11311)..."
sshpass -p "$REMOTE_PASSWORD" ssh -o StrictHostKeyChecking=no \
    -L 11311:localhost:11311 \
    -N -f "$REMOTE_USER@$REMOTE_HOST" || true

echo "✅ SSH tunnels established"
echo "   GDB: localhost:1234 -> $REMOTE_HOST:1234"
echo "   ROS: localhost:11311 -> $REMOTE_HOST:11311"
echo ""
echo "💡 To stop tunnels: devel/debug/cleanup.sh"
