# Setup-Anleitung für lokale Konfiguration

Das OpenMower Remote Debug Setup nutzt jetzt ein Template-System für lokale Konfigurationen.

## Erste Einrichtung

1. **Template kopieren:**
   ```bash
   cd devel/debug-tools
   cp config_local.py.template config_local.py
   ```

2. **Lokale Einstellungen anpassen:**
   ```bash
   nano config_local.py
   ```
   
   Passe folgende Werte an deine Umgebung an:
   - `host`: IP-Adresse deines Raspberry Pi
   - `ros_master_uri`: ROS Master URI mit deiner Pi-IP
   - `ros_pi_ip`: Pi IP für ROS-Kommunikation
   - `ros_dev_ip`: IP deines Entwicklungsrechners

3. **SSH-Setup durchführen:**
   Siehe `SSH-SETUP.md` für detaillierte Anweisungen

4. **VS Code Konfigurationen generieren:**
   ```bash
   ./generate-vscode.sh
   ```

## Struktur

```
devel/debug-tools/
├── config.py                    # Haupt-Konfiguration (im Git)
├── config_local.py.template     # Template für lokale Einstellungen (im Git)  
├── config_local.py              # Deine lokalen Einstellungen (git-ignored)
├── generate-vscode.py           # VS Code Generator
└── ...
```

## Vorteile

✅ **Git-sauber**: Keine lokalen IPs in der Git-History
✅ **Team-freundlich**: Jeder kann eigene `config_local.py` haben  
✅ **Einfache Commits**: Keine IP-Bereinigung nötig
✅ **Fallback**: Funktioniert auch ohne `config_local.py`

## Fehlerbehebung

- **"config_local.py nicht gefunden"**: Führe Schritt 1 aus
- **"SSH-Verbindung fehlgeschlagen"**: Prüfe SSH-Setup (siehe SSH-SETUP.md)
- **"Binary nicht gefunden"**: Führe `catkin_make` auf dem Pi aus
