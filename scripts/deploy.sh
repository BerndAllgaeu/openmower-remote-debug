#!/bin/bash
set -e

# OpenMower Deployment Script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"  # Von devel/debug nach workspace root

# Config laden
source <(python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/.debug')
from config import REMOTE_CONFIG, get_rsync_command, get_ssh_command
print(f'RSYNC_CMD=\"{get_rsync_command()}\"')
print(f'SSH_CMD=\"{get_ssh_command()}\"')
print(f'REMOTE_HOST={REMOTE_CONFIG[\"host\"]}')
print(f'REMOTE_USER={REMOTE_CONFIG[\"user\"]}')
print(f'REMOTE_WORKSPACE={REMOTE_CONFIG[\"workspace\"]}')
")

PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"  # Von devel/debug nach workspace root

echo "🚀 Deploying OpenMower to $REMOTE_USER@$REMOTE_HOST"

# 1. Lokaler Build
echo "🔨 Building locally..."
cd "$PROJECT_ROOT"
source /opt/ros/noetic/setup.bash && catkin_make

# 2. Sync zum Pi
echo "📡 Syncing to Pi..."
eval "$RSYNC_CMD $PROJECT_ROOT/ $REMOTE_USER@$REMOTE_HOST:$REMOTE_WORKSPACE/"

# 3. Remote Build
echo "🔨 Building on Pi..."
eval "$SSH_CMD 'cd $REMOTE_WORKSPACE && source /opt/ros/noetic/setup.bash && catkin_make'"

echo "✅ Deployment complete!"
