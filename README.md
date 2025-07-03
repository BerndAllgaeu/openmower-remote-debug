# OpenMower Remote Debug Setup

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security](https://img.shields.io/badge/Security-SSH%20Keys-green.svg)](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

Ein portables, sicheres Remote-Debugging-Setup für OpenMower-Projekte. Kann als Git-Submodule in verschiedene OpenMower-Repositories eingebunden werden.

## 🎯 Features

- ✅ **SSH-Key Authentifizierung** - Keine Passwörter im Code
- ✅ **Zentrale Konfigurationsverwaltung** - Eine Datei für alle Einstellungen  
- ✅ **Automatische VS Code Debug/Tasks-Generierung** - Plug & Play
- ✅ **Portabel zwischen Branches/Forks** - Funktioniert überall
- ✅ **Sichere Git-History** - Keine sensiblen Daten in Commits
- ✅ **Cross-platform Support** - Linux, macOS, Windows

## 🚀 Schnellstart

### 1. Als Git Submodule hinzufügen

```bash
# Im Root-Verzeichnis Ihres OpenMower-Projekts
git submodule add https://github.com/YOUR-USERNAME/openmower-remote-debug.git devel/debug-tools

# Setup ausführen
devel/debug-tools/setup.sh

# VS Code öffnen und F5 für Remote-Debugging drücken
code .
```

### Manuelle Installation

```bash
# Repository klonen
git clone https://github.com/YOUR-USERNAME/openmower-remote-debug.git .debug

# Setup ausführen
.debug/setup.sh
```

## ⚙️ Konfiguration

Bearbeiten Sie `.debug/config.py` für Ihre spezifische Hardware:

```python
REMOTE_CONFIG = {
    "host": "192.168.1.100",        # IP Ihres Raspberry Pi
    "user": "ubuntu",                # SSH Username
    "password": "YourPassword",      # SSH Password (besser: SSH-Keys verwenden)
    "workspace": "/home/ubuntu/open_mower_ros"
}
```

## 📋 Verfügbare Commands

```bash
.debug/setup.sh                    # Erstinstallation
.debug/update-config.sh            # Konfiguration aktualisieren
.debug/generate-vscode.sh          # VS Code Konfigurationen neu generieren
.debug/test-connection.sh          # Verbindung zum Pi testen
```

## 🐛 Debug-Konfigurationen

Nach dem Setup stehen folgende Debug-Konfigurationen zur Verfügung:

- **Remote Debug - mower_logic**: Hauptlogik des Mähers
- **Remote Debug - mower_comms_v2**: Hardware-Kommunikation
- **Remote Debug - mower_map_service**: Kartenverwaltung
- **Local Debug - Build and Debug**: Lokales Debugging

## 🔧 Anpassung an verschiedene Projekte

Das Setup erkennt automatisch:
- Verschiedene OpenMower-Forks
- Branch-spezifische Konfigurationen
- Projekt-spezifische Binaries

## 📁 Verzeichnisstruktur

```
.debug/
├── config.py              # Zentrale Konfiguration
├── setup.sh              # Erstinstallation
├── update-config.sh       # Update-Script
├── generate-vscode.sh     # VS Code Generator
├── test-connection.sh     # Verbindungstest
├── templates/             # Template-Dateien
├── scripts/               # Quell-Skripte (werden nach devel/debug kopiert)
│   ├── deploy.sh
│   ├── tunnel.sh
│   └── cleanup.sh
└── USAGE.md               # Anwendungsanleitung

devel/debug/               # Ausführbare Skripte (automatisch generiert, git-ignoriert)
├── deploy.sh
├── tunnel.sh
└── cleanup.sh
```

## 🔄 Updates

```bash
# Submodule aktualisieren
git submodule update --remote .debug

# Konfiguration neu generieren
.debug/update-config.sh
```

## 🛠️ Troubleshooting

### SSH-Verbindung testen
```bash
.debug/test-connection.sh
```

### Konfiguration zurücksetzen
```bash
.debug/setup.sh --reset
```

### Debug-Logs aktivieren
```bash
DEBUG=1 .debug/generate-vscode.sh
```

## 📞 Support

Bei Problemen öffnen Sie ein Issue oder prüfen Sie die [Wiki-Seite](https://github.com/YOUR-USERNAME/openmower-remote-debug/wiki).
