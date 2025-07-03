#!/bin/bash
set -e

# VS Code Konfigurationsgenerator Wrapper
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Generiere VS Code Konfigurationen..."
python3 "$SCRIPT_DIR/generate-vscode.py" "$@"