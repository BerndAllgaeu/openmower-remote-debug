# Änderungsprotokoll: Debug-Skripte in devel/ verschieben

## 🎯 Ziel erreicht
Debug-Skripte werden jetzt im `devel/`-Ordner abgelegt, der bereits in `.gitignore` steht. Dadurch gibt es keine versehentlichen Commits von ausführbaren Skripten mehr.

## ✅ Was geändert wurde

### 1. **Neue Verzeichnisstruktur**
```
Vorher:                    Nachher:
.debug/scripts/           .debug/scripts/          (Quell-Skripte)
├── deploy.sh             ├── deploy.sh
├── tunnel.sh       →     ├── tunnel.sh
└── cleanup.sh            └── cleanup.sh

                          devel/debug/             (Ausführbare Kopien, git-ignoriert)
                          ├── deploy.sh
                          ├── tunnel.sh
                          └── cleanup.sh
```

### 2. **Geänderte Dateien**
- **`.debug/config.py`**: Neue Funktionen `get_debug_scripts_dir()` und `get_temp_dir()`
- **`.debug/generate-vscode.py`**: Kopiert Skripte automatisch nach `devel/debug/`
- **`.debug/setup.sh`**: Verwendet `devel/` für temporäre Dateien
- **`.debug/scripts/*.sh`**: Angepasste Pfad-Logik für neue Struktur
- **`.vscode/tasks.json`**: Verweist auf `devel/debug/`-Skripte
- **`.gitignore`**: Entfernung der `.debug/tmp/` Einträge (nicht mehr nötig)

### 3. **Automatischer Workflow**
1. **Quell-Skripte** bleiben in `.debug/scripts/` (versioniert)
2. **Ausführbare Kopien** werden nach `devel/debug/` kopiert (git-ignoriert)
3. **VS Code Tasks** verwenden die Kopien aus `devel/debug/`
4. **Cleanup** entfernt sowohl `devel/debug/` als auch `devel/tmp/`

## 🚀 Vorteile

✅ **Keine versehentlichen Commits**: `devel/` ist bereits in `.gitignore`
✅ **Saubere Repository-Struktur**: Nur Source-Dateien werden versioniert
✅ **Automatische Aktualisierung**: Skripte werden bei jeder Config-Generierung aktualisiert
✅ **Backward-Kompatibilität**: Setup funktioniert weiterhin in anderen Projekten
✅ **Build-Integration**: Nutzt existierende catkin-Struktur

## 🔧 Wie es funktioniert

1. **Setup/Update**: `generate-vscode.py` kopiert `.debug/scripts/*.sh` → `devel/debug/`
2. **VS Code Tasks**: Verwenden absolute Pfade zu `devel/debug/`-Skripten
3. **Git Ignorierung**: `devel/` ist bereits in `.gitignore`, automatische Ignorierung
4. **Cleanup**: Entfernt komplettes `devel/debug/` und `devel/tmp/`

## 🎯 Ergebnis

- **Keine .gitignore-Änderungen nötig**: Nutzt existierende `devel/`-Ignorierung
- **Keine versehentlichen Commits**: Ausführbare Skripte sind automatisch ignoriert
- **Portabilität erhalten**: Setup funktioniert in allen OpenMower-Projekten
- **Saubere Trennung**: Source vs. Ausführbare Dateien klar getrennt

Das Setup ist jetzt noch robuster und vermeidet jegliche Commit-Probleme! 🎉
