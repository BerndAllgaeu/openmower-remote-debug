#!/bin/bash
set -e

# VS Code Configuration Generator with Python venv setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
VENV_PATH="$WORKSPACE_ROOT/.venv"

echo "🔧 OpenMower VS Code Configuration Generator"

# Check and setup Python virtual environment
setup_venv() {
    echo "🐍 Setting up Python virtual environment..."
    
    # Check if venv exists
    if [ ! -d "$VENV_PATH" ]; then
        echo "   Creating new virtual environment at $VENV_PATH"
        python3 -m venv "$VENV_PATH"
    else
        echo "   Virtual environment already exists"
    fi
    
    # Activate venv
    source "$VENV_PATH/bin/activate"
    
    # Upgrade pip
    echo "   Upgrading pip..."
    pip install --upgrade pip >/dev/null 2>&1
    
    # Install basic requirements if they don't exist
    echo "   Installing Python dependencies..."
    pip install --quiet psutil 2>/dev/null || true
    
    echo "✅ Python environment ready"
}

# Check if we need Python venv
if command -v python3 >/dev/null 2>&1; then
    # Try to import our config module
    if ! python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from config import REMOTE_CONFIG" 2>/dev/null; then
        echo "⚠️  Python import failed, setting up virtual environment..."
        setup_venv
    fi
else
    echo "❌ Python3 not found! Please install Python 3."
    exit 1
fi

# Generate VS Code configurations
echo "🔧 Generating VS Code configurations..."
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
fi

python3 "$SCRIPT_DIR/generate-vscode.py" "$@"
echo "✅ VS Code configuration generation complete!"