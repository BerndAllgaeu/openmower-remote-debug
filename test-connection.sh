#!/bin/bash
set -e

# OpenMower Remote Connection Test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Config laden
source <(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from config import REMOTE_CONFIG, get_ssh_command, get_ssh_full_command
print(f'REMOTE_HOST={REMOTE_CONFIG[\"host\"]}')
print(f'REMOTE_USER={REMOTE_CONFIG[\"user\"]}')
print(f'REMOTE_WORKSPACE={REMOTE_CONFIG[\"workspace\"]}')
print(f'SSH_CMD=\"{get_ssh_command()}\"')
print(f'SSH_FULL_CMD=\"{get_ssh_full_command()}\"')
if 'ssh_host' in REMOTE_CONFIG and REMOTE_CONFIG['ssh_host']:
    print(f'SSH_HOST={REMOTE_CONFIG[\"ssh_host\"]}')
else:
    print('SSH_HOST=')
")

QUIET=false
if [[ "$1" == "--quiet" ]]; then
    QUIET=true
fi

log() {
    if [[ "$QUIET" != "true" ]]; then
        echo "$@"
    fi
}

error() {
    echo "❌ $@" >&2
}

test_command() {
    local description="$1"
    local command="$2"
    
    log "🔍 Teste: $description"
    
    if eval "$command" >/dev/null 2>&1; then
        log "✅ $description: OK"
        return 0
    else
        error "$description: FEHLER"
        return 1
    fi
}

# Haupt-Tests
main() {
    log "🚀 OpenMower Remote Connection Test"
    log "Target: $REMOTE_USER@$REMOTE_HOST"
    
    local errors=0
    
    # 1. SSH-Key/Host Test
    if [[ -n "$SSH_HOST" ]]; then
        if ! test_command "SSH Host Konfiguration" "$SSH_FULL_CMD 'echo ok'"; then
            error "SSH Host '$SSH_HOST' nicht erreichbar"
            ((errors++))
        fi
    else
        SSH_KEY="${REMOTE_CONFIG[ssh_key]:-~/.ssh/id_rsa_openmower}"
        if ! test_command "SSH-Key verfügbar" "test -f ${SSH_KEY}"; then
            error "SSH-Key nicht gefunden: ${SSH_KEY}"
            ((errors++))
        fi
    fi
    
    # 2. Ping Test
    if ! test_command "Host erreichbar (ping)" "ping -c 1 -W 3 $REMOTE_HOST"; then
        error "Host $REMOTE_HOST ist nicht erreichbar"
        ((errors++))
    fi
    
    # 3. SSH Verbindung
    if ! test_command "SSH Verbindung" "$SSH_FULL_CMD -o ConnectTimeout=5 'echo ok'"; then
        error "SSH-Verbindung fehlgeschlagen. Prüfen Sie Benutzername/Passwort."
        ((errors++))
    fi
    
    # 4. Workspace existiert?
    if ! test_command "Remote Workspace" "$SSH_FULL_CMD 'test -d $REMOTE_WORKSPACE'"; then
        error "Workspace $REMOTE_WORKSPACE existiert nicht auf dem Remote-Host"
        ((errors++))
    fi
    
    # 5. ROS Installation
    if ! test_command "ROS Installation" "$SSH_FULL_CMD 'test -f /opt/ros/noetic/setup.bash'"; then
        error "ROS Noetic ist nicht auf dem Remote-Host installiert"
        ((errors++))
    fi
    
    # 6. GDB verfügbar?
    if ! test_command "GDB verfügbar" "$SSH_FULL_CMD 'command -v gdb'"; then
        error "GDB ist nicht auf dem Remote-Host installiert"
        ((errors++))
    fi
    
    # 7. Catkin Workspace
    if ! test_command "Catkin Workspace" "$SSH_FULL_CMD 'test -f $REMOTE_WORKSPACE/src/CMakeLists.txt'"; then
        log "⚠️  Catkin Workspace nicht initialisiert (normal bei erstem Setup)"
    fi
    
    # 8. Build-Verzeichnisse
    if ! test_command "Build-Verzeichnisse" "$SSH_FULL_CMD 'test -d $REMOTE_WORKSPACE/devel'"; then
        log "⚠️  Projekt noch nicht gebaut (normal bei erstem Setup)"
    fi
    
    if [[ $errors -eq 0 ]]; then
        log ""
        log "🎉 Alle Tests erfolgreich!"
        log "✅ Remote-Debugging sollte funktionieren"
        exit 0
    else
        log ""
        error "💥 $errors Test(s) fehlgeschlagen"
        log ""
        log "🔧 Troubleshooting:"
        log "   1. SSH-Schlüssel verwenden statt Passwort"
        log "   2. Firewall-Einstellungen prüfen"
        log "   3. ROS auf Remote-Host installieren"
        log "   4. GDB installieren: sudo apt install gdb"
        log "   5. Konfiguration prüfen: .debug/config.py"
        exit 1
    fi
}

# Script ausführen
main "$@"
