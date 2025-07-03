# Remote-Debug Setup für andere OpenMower-Projekte

## 🎯 Übersicht

Das `.debug/`-Verzeichnis ist jetzt ein portables Remote-Debugging-Setup, das Sie in anderen OpenMower-Projekten wiederverwenden können.

## 🚀 Setup für neues Projekt

### Methode 1: Als Git Submodule (Empfohlen)

```bash
# 1. In Ihr neues OpenMower-Projekt wechseln
cd /path/to/your/other-openmower-project

# 2. Remote-Debug als Submodule hinzufügen
git submodule add /home/bernd/dev/open_mower_ros/.debug .debug

# 3. Konfiguration anpassen
nano .debug/config.py

# 4. Setup ausführen
.debug/setup.sh
```

### Methode 2: Manuell kopieren

```bash
# 1. Debug-Setup kopieren
cp -r /home/bernd/dev/open_mower_ros/.debug /path/to/new-project/

# 2. Konfiguration anpassen
cd /path/to/new-project
nano .debug/config.py

# 3. Setup ausführen
.debug/setup.sh
```

## ⚙️ Konfiguration für verschiedene Projekte

Bearbeiten Sie `.debug/config.py` für jedes Projekt:

```python
REMOTE_CONFIG = {
    # Unterschiedliche Pi für verschiedene Projekte
    "host": "192.168.1.100",           # Pi #1 für Projekt A
    # "host": "192.168.1.101",         # Pi #2 für Projekt B
    
    "user": "ubuntu",
    "password": "YourPassword",
    "workspace": "/home/ubuntu/open_mower_ros",
    
    # Projekt-spezifische Programme
    "debug_programs": [
        {"name": "mower_logic", "path": "mower_logic/mower_logic"},
        # Weitere Programme für spezielle Forks...
    ]
}
```

## 🔄 Branch-Wechsel Workflow

```bash
# 1. Branch wechseln
git checkout feature-branch

# 2. Konfiguration aktualisieren (falls nötig)
nano .debug/config.py

# 3. VS Code Konfigurationen neu generieren
.debug/update-config.sh

# 4. Debuggen wie gewohnt
# F5 in VS Code
```

## 📁 Was passiert beim Setup

1. **Automatische Erkennung**: Erkennt alle ROS-Packages im `src/`-Verzeichnis
2. **VS Code Integration**: Generiert `launch.json` und `tasks.json`
3. **Verbindungstest**: Prüft SSH-Verbindung und Abhängigkeiten
4. **Flexible Konfiguration**: Anpassbar für verschiedene Hardware-Setups

## 🛠️ Anpassung für Community-Forks

Viele OpenMower-Community-Forks haben verschiedene Package-Namen oder zusätzliche Komponenten:

```python
# Beispiel für Fork mit zusätzlichen Packages
"debug_programs": [
    {"name": "mower_logic", "path": "mower_logic/mower_logic"},
    {"name": "custom_driver", "path": "custom_driver/custom_driver"},
    {"name": "ai_navigation", "path": "ai_navigation/navigator"},
]
```

## 🎯 Vorteile dieses Setups

- ✅ **Portabel**: Funktioniert in jedem OpenMower-Projekt
- ✅ **Versioniert**: Git-Integration für Änderungsverfolgung
- ✅ **Konsistent**: Gleiche Debug-Erfahrung überall
- ✅ **Flexibel**: Anpassbar für verschiedene Hardware/Software-Setups
- ✅ **Wartbar**: Zentrale Konfiguration, Updates propagieren automatisch

## 💡 Pro-Tipps

1. **SSH-Keys verwenden**: Sicherer als Passwörter
   ```bash
   ssh-keygen -t rsa
   ssh-copy-id ubuntu@192.168.1.100
   # Dann Passwort aus config.py entfernen
   ```

2. **Mehrere Pi's**: Verschiedene IPs für verschiedene Projekte
3. **Branch-spezifische Configs**: Verschiedene Setups für Feature-Branches
4. **Team-Setup**: Submodule für gemeinsame Debug-Konfiguration im Team

Das Setup ist jetzt komplett portabel und ready für verschiedene OpenMower-Projekte! 🎉
