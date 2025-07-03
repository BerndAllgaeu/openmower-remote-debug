#!/bin/bash
set -e

# OpenMower Remote Debug Setup
# Dieses Script richtet das Remote-Debugging für OpenMower-Projekte ein

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VSCODE_DIR="$PROJECT_ROOT/.vscode"

echo "🚀 OpenMower Remote Debug Setup"
echo "Project Root: $PROJECT_ROOT"
echo "VS Code Dir: $VSCODE_DIR"

# Hilfe anzeigen
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --reset     Entfernt bestehende Konfiguration und startet neu"
    echo "  --test      Führt nur Verbindungstest durch"
    echo "  --help      Zeigt diese Hilfe an"
    echo ""
    echo "Beispiele:"
    echo "  $0                    # Normale Installation"
    echo "  $0 --reset          # Konfiguration zurücksetzen"
    echo "  $0 --test           # Nur Verbindung testen"
}

# Parameter verarbeiten
RESET_CONFIG=false
TEST_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --reset)
            RESET_CONFIG=true
            shift
            ;;
        --test)
            TEST_ONLY=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "❌ Unbekannte Option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Konfiguration validieren
echo "📋 Validiere Konfiguration..."
if ! python3 "$SCRIPT_DIR/config.py"; then
    echo "❌ Konfigurationsfehler. Bitte config.py bearbeiten."
    exit 1
fi

# Nur Test durchführen
if [ "$TEST_ONLY" = true ]; then
    echo "🔍 Führe Verbindungstest durch..."
    exec "$SCRIPT_DIR/test-connection.sh"
fi

# Reset durchführen
if [ "$RESET_CONFIG" = true ]; then
    echo "🗑️  Entferne bestehende Konfiguration..."
    rm -f "$VSCODE_DIR/launch.json"
    rm -f "$VSCODE_DIR/tasks.json"
    rm -rf "$PROJECT_ROOT/devel/debug"
    rm -rf "$PROJECT_ROOT/devel/tmp"
    echo "✅ Konfiguration zurückgesetzt"
fi

# VS Code Verzeichnis erstellen
echo "📁 Erstelle VS Code Verzeichnis..."
mkdir -p "$VSCODE_DIR"

# Abhängigkeiten prüfen
echo "🔧 Prüfe Abhängigkeiten..."

# sshpass installieren falls nicht vorhanden
if ! command -v sshpass >/dev/null 2>&1; then
    echo "📦 Installiere sshpass..."
    if command -v apt >/dev/null 2>&1; then
        sudo apt update && sudo apt install -y sshpass
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y sshpass
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --noconfirm sshpass
    else
        echo "❌ Konnte sshpass nicht automatisch installieren."
        echo "   Bitte installieren Sie sshpass manuell für Ihr System."
        exit 1
    fi
fi

# Python-Module prüfen
echo "🐍 Prüfe Python-Module..."
python3 -c "import json" 2>/dev/null || {
    echo "❌ Python3 json-Modul nicht verfügbar"
    exit 1
}

# VS Code Konfigurationen generieren
echo "⚙️  Generiere VS Code Konfigurationen..."
"$SCRIPT_DIR/generate-vscode.sh"

# Hilfsskripte ausführbar machen
echo "🔧 Bereite Hilfsskripte vor..."
chmod +x "$SCRIPT_DIR"/*.sh
chmod +x "$SCRIPT_DIR/scripts"/*.sh 2>/dev/null || true

# Verbindungstest durchführen
echo "🔍 Teste Verbindung zum Remote-Host..."
if "$SCRIPT_DIR/test-connection.sh" --quiet; then
    echo "✅ Verbindung erfolgreich"
else
    echo "⚠️  Verbindungstest fehlgeschlagen (Setup trotzdem fortgesetzt)"
fi

# .gitignore aktualisieren
echo "📝 Aktualisiere .gitignore..."
GITIGNORE="$PROJECT_ROOT/.gitignore"
if [ -f "$GITIGNORE" ]; then
    # Da wir jetzt devel/ verwenden, keine zusätzlichen .gitignore-Einträge nötig
    # devel/ ist bereits ignoriert
    echo "✅ devel/ ist bereits in .gitignore (Debug-Skripte automatisch ignoriert)"
fi

echo ""
echo "🎉 Setup erfolgreich abgeschlossen!"
echo ""
echo "📋 Nächste Schritte:"
echo "   1. VS Code öffnen: code ."
echo "   2. Eine .cpp-Datei öffnen und Breakpoint setzen (F9)"
echo "   3. Debug starten: F5 → 'Remote Debug - mower_logic' auswählen"
echo ""
echo "⚙️  Konfiguration anpassen:"
echo "   - Bearbeiten: .debug/config.py"
echo "   - Neu generieren: .debug/update-config.sh"
echo ""
echo "🔧 Verfügbare Commands:"
echo "   .debug/update-config.sh     # Konfiguration aktualisieren"
echo "   .debug/test-connection.sh   # Verbindung testen"
echo "   .debug/generate-vscode.sh   # VS Code neu generieren"
echo ""
echo "📖 Weitere Hilfe: .debug/README.md"
