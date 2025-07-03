#!/bin/bash

# Cleanup Script für OpenMower Remote Debug
echo "🧹 Cleaning up Remote Debug processes..."

# SSH Tunnels beenden
echo "🔌 Closing SSH tunnels..."
pkill -f "ssh.*-L.*1234" 2>/dev/null || true
pkill -f "ssh.*-L.*11311" 2>/dev/null || true

# GDB Prozesse beenden
echo "🐛 Stopping GDB processes..."
pkill -f "gdb.*openmower" 2>/dev/null || true

# Temporäre Dateien löschen
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
DEVEL_DIR="$PROJECT_ROOT/devel"

if [ -d "$DEVEL_DIR/tmp" ]; then
    echo "🗑️  Removing temporary files..."
    rm -rf "$DEVEL_DIR/tmp"
fi

if [ -d "$DEVEL_DIR/debug" ]; then
    echo "🗑️  Removing debug scripts..."
    rm -rf "$DEVEL_DIR/debug"
fi

echo "✅ Cleanup complete!"
