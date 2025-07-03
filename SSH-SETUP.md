# SSH-Key Setup für OpenMower Remote Debug

## 🔐 Sicherheitsverbesserung

Das Remote-Debug-Setup wurde auf SSH-Key-Authentifizierung umgestellt. **Keine Passwörter mehr im Code!**

## 🚀 Schnellinstallation

```bash
# 1. SSH-Key generieren (falls noch nicht vorhanden)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_openmower -N "" -C "openmower-debug@$(hostname)"

# 2. SSH-Config aktualisieren
cat >> ~/.ssh/config << EOF
Host openmower
    HostName 192.168.99.168
    User ubuntu
    IdentityFile ~/.ssh/id_rsa_openmower
    StrictHostKeyChecking no
EOF

# 3. SSH-Key auf den Pi kopieren
ssh-copy-id -i ~/.ssh/id_rsa_openmower.pub ubuntu@192.168.99.168

# 4. Verbindung testen
ssh openmower "echo 'SSH-Key funktioniert!'"
```

## ⚙️ Konfiguration

Die neue Konfiguration in `devel/debug-tools/config.py`:

```python
REMOTE_CONFIG = {
    "host": "192.168.99.168",
    "user": "ubuntu", 
    "ssh_key": "~/.ssh/id_rsa_openmower",    # SSH-Key Pfad
    "ssh_host": "openmower",                 # SSH Host aus ~/.ssh/config
    "workspace": "/home/ubuntu/open_mower_ros",
    # ... weitere Konfiguration
}
```

## 🔍 Verbindungstest

```bash
# Vollständiger Systemtest
cd devel/debug-tools
./test-connection.sh

# Einfacher SSH-Test
ssh openmower "echo 'Verbindung OK'"
```

## ✅ Vorteile

- ✅ **Sicherheit**: Keine Passwörter im Code
- ✅ **Performance**: Schnellere SSH-Verbindungen
- ✅ **Automatisierung**: Keine interaktive Passwort-Eingabe
- ✅ **Git-freundlich**: Keine sensiblen Daten in Repositories

## 🛠️ Troubleshooting

### SSH-Key wird nicht akzeptiert
```bash
# Berechtigungen prüfen
chmod 600 ~/.ssh/id_rsa_openmower
chmod 644 ~/.ssh/id_rsa_openmower.pub

# SSH-Agent verwenden
ssh-add ~/.ssh/id_rsa_openmower
```

### Host Key Verification failed
```bash
# Host Key zurücksetzen
ssh-keygen -R 192.168.99.168
ssh-keygen -R openmower
```

### Pi nicht erreichbar
```bash
# IP-Adresse in ~/.ssh/config anpassen
nano ~/.ssh/config

# Dann Konfiguration neu generieren
cd devel/debug-tools
./update-config.sh
```

## 🔄 Migration von Passwort-Setup

Falls Sie noch die alte Passwort-basierte Konfiguration haben:

1. **SSH-Keys einrichten** (siehe oben)
2. **Konfiguration aktualisieren**: `./devel/debug-tools/update-config.sh`
3. **Testen**: `./devel/debug-tools/test-connection.sh`

Das war's! 🎉
