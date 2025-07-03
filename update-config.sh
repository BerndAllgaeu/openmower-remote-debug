#!/bin/bash
set -e

# OpenMower Remote Debug Configuration Update
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 OpenMower Remote Debug - Konfiguration aktualisieren"

# Konfiguration validieren
echo "📋 Validiere Konfiguration..."
if ! python3 "$SCRIPT_DIR/config.py"; then
    echo "❌ Konfigurationsfehler. Bitte config.py bearbeiten."
    exit 1
fi

# VS Code Konfigurationen neu generieren
echo "⚙️  Regeneriere VS Code Konfigurationen..."
"$SCRIPT_DIR/generate-vscode.sh"

# Verbindungstest (optional)
echo "🔍 Teste Verbindung..."
if "$SCRIPT_DIR/test-connection.sh" --quiet; then
    echo "✅ Verbindung erfolgreich"
else
    echo "⚠️  Verbindungstest fehlgeschlagen"
fi

echo ""
echo "🎉 Konfiguration erfolgreich aktualisiert!"
echo ""
echo "📋 Änderungen wirksam nach:"
echo "   - VS Code neustarten (falls geöffnet)"
echo "   - F5 für Remote-Debugging"
