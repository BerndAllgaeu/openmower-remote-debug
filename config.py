#!/usr/bin/env python3
"""
OpenMower Remote Debug Configuration

Zentrale Konfigurationsdatei für Remote-Debugging Setup.
Diese Datei wird von allen Scripts verwendet.

Setup:
1. Kopiere config_local.py.template nach config_local.py
2. Passe config_local.py an deine Umgebung an
3. config_local.py wird automatisch von Git ignoriert
"""

import os

# ============================================================================
# PROJEKT-SPEZIFISCHE KONFIGURATION (im Git)
# ============================================================================

# Debug Programme (korrekte Binary-Pfade aus devel/lib/)
DEBUG_PROGRAMS = [
    {"name": "mower_logic", "path": "mower_logic/mower_logic"},
    {"name": "mower_comms_v2", "path": "mower_comms_v2/mower_comms_v2"},
    {"name": "mower_map_service", "path": "mower_map/mower_map_service"},
    {"name": "monitoring", "path": "mower_logic/monitoring"},
    {"name": "mower_comms_v1", "path": "mower_comms_v1/mower_comms_v1"},
    {"name": "mower_simulation", "path": "mower_simulation/mower_simulation"},
    {"name": "xbot_positioning", "path": "xbot_positioning/xbot_positioning"},
    {"name": "xbot_monitoring", "path": "xbot_monitoring/xbot_monitoring"},
    {"name": "xbot_remote", "path": "xbot_remote/xbot_remote"},
    {"name": "slic3r_coverage_planner", "path": "slic3r_coverage_planner/slic3r_coverage_planner"},
    {"name": "driver_gps_node", "path": "xbot_driver_gps/driver_gps_node"},
    {"name": "xesc_driver_node", "path": "xesc_driver/xesc_driver_node"},
    # open_mower ist ein Launch-Package, kein Binary - entfernt
]

# Packages ohne ausführbare Binaries (nur Launch-Files, etc.)
EXCLUDED_PACKAGES = ["open_mower", "mower_msgs", "mower_utils", "mower_map"]

# ============================================================================
# DEFAULT-KONFIGURATION (Fallback wenn config_local.py fehlt)
# ============================================================================

DEFAULT_CONFIG = {
    # Raspberry Pi Konfiguration
    "host": "192.168.1.100",                    # IP-Adresse des Pi
    "user": "ubuntu",                            # SSH-Benutzername
    "ssh_key": "~/.ssh/id_rsa_openmower",        # SSH-Key Pfad
    "ssh_host": "openmower",                     # SSH Host aus ~/.ssh/config
    "workspace": "/home/ubuntu/open_mower_ros",  # Workspace-Pfad auf dem Pi
    
    # ROS Konfiguration
    "ros_master_uri": "http://192.168.1.100:11311",
    "ros_pi_ip": "192.168.1.100",
    "ros_dev_ip": "192.168.1.200",
}

# ============================================================================
# KONFIGURATION LADEN UND MERGEN
# ============================================================================

def load_config():
    """
    Lädt die Konfiguration aus config_local.py falls vorhanden,
    sonst werden die Default-Werte verwendet.
    """
    config = DEFAULT_CONFIG.copy()
    
    try:
        # Versuche lokale Konfiguration zu importieren
        from config_local import LOCAL_CONFIG
        config.update(LOCAL_CONFIG)
        print("✅ Lokale Konfiguration aus config_local.py geladen")
    except ImportError:
        print("⚠️  config_local.py nicht gefunden - verwende Default-Werte")
        print("   Tipp: cp config_local.py.template config_local.py")
    except Exception as e:
        print(f"❌ Fehler beim Laden von config_local.py: {e}")
        print("   Verwende Default-Werte")
    
    # Debug-Programme hinzufügen
    config["debug_programs"] = DEBUG_PROGRAMS
    
    return config

# Globale Konfiguration laden
REMOTE_CONFIG = load_config()

# ============================================================================
# AUTOMATISCHE ERKENNUNG - Normalerweise nicht ändern
# ============================================================================

def get_project_root():
    """Ermittelt das Root-Verzeichnis des OpenMower-Projekts."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Gehe nach oben bis wir src/ oder CMakeLists.txt finden
    while current_dir != "/":
        if (os.path.exists(os.path.join(current_dir, "src")) and 
            os.path.exists(os.path.join(current_dir, "CMakeLists.txt"))):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # Fallback: Wenn wir in devel/debug-tools sind, gehe zwei Ebenen hoch
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir.endswith("devel/debug-tools"):
        return os.path.dirname(os.path.dirname(script_dir))
    
    # Fallback: Parent-Verzeichnis vom debug-tools-Ordner
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_vscode_dir():
    """Ermittelt das .vscode-Verzeichnis."""
    return os.path.join(get_project_root(), ".vscode")

def get_debug_scripts_dir():
    """Ermittelt das Verzeichnis für Debug-Skripte (im devel/-Ordner)."""
    debug_dir = os.path.join(get_project_root(), "devel", "debug")
    os.makedirs(debug_dir, exist_ok=True)
    return debug_dir

def get_temp_dir():
    """Ermittelt das temporäre Verzeichnis für Debug-Dateien."""
    temp_dir = os.path.join(get_project_root(), "devel", "tmp")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def get_ros_environment():
    """Ermittelt ROS-Umgebungsvariablen."""
    return {
        "ROS_MASTER_URI": REMOTE_CONFIG["ros_master_uri"],
        "ROS_IP": REMOTE_CONFIG["ros_pi_ip"],
        "ROS_PACKAGE_PATH": f"{REMOTE_CONFIG['workspace']}/src:/opt/ros/noetic/share",
        "LD_LIBRARY_PATH": f"{REMOTE_CONFIG['workspace']}/devel/lib:/opt/ros/noetic/lib",
        "CMAKE_PREFIX_PATH": f"{REMOTE_CONFIG['workspace']}/devel:/opt/ros/noetic",
        "PYTHONPATH": f"{REMOTE_CONFIG['workspace']}/devel/lib/python3/dist-packages:/opt/ros/noetic/lib/python3/dist-packages"
    }

def get_ssh_command():
    """Erstellt SSH-Basis-Kommando mit SSH-Key."""
    if "ssh_host" in REMOTE_CONFIG and REMOTE_CONFIG["ssh_host"]:
        # Verwende SSH Host aus ~/.ssh/config
        return f"ssh {REMOTE_CONFIG['ssh_host']}"
    else:
        # Direkte SSH-Verbindung mit Key
        ssh_key = REMOTE_CONFIG.get("ssh_key", "~/.ssh/id_rsa_openmower")
        return f"ssh -i {ssh_key} -o StrictHostKeyChecking=no {REMOTE_CONFIG['user']}@{REMOTE_CONFIG['host']}"

def get_rsync_command():
    """Erstellt rsync-Basis-Kommando mit SSH-Key."""
    if "ssh_host" in REMOTE_CONFIG and REMOTE_CONFIG["ssh_host"]:
        # Verwende SSH Host aus ~/.ssh/config
        ssh_cmd = f"ssh {REMOTE_CONFIG['ssh_host']}"
    else:
        # Direkte SSH-Verbindung mit Key
        ssh_key = REMOTE_CONFIG.get("ssh_key", "~/.ssh/id_rsa_openmower")
        ssh_cmd = f"ssh -i {ssh_key} -o StrictHostKeyChecking=no"
    
    return f"rsync -avz --exclude='build/' --exclude='devel/' --exclude='.git/' -e '{ssh_cmd}'"

# ============================================================================
# PROJEKT-SPEZIFISCHE ERKENNUNG
# ============================================================================

def detect_project_binaries():
    """Erkennt verfügbare Binaries im Projekt automatisch."""
    project_root = get_project_root()
    src_dir = os.path.join(project_root, "src")
    
    detected_programs = []
    
    if os.path.exists(src_dir):
        for item in os.listdir(src_dir):
            item_path = os.path.join(src_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.') and item not in EXCLUDED_PACKAGES:
                # Prüfe ob es ein ROS-Package ist (CMakeLists.txt + package.xml)
                if (os.path.exists(os.path.join(item_path, "CMakeLists.txt")) and
                    os.path.exists(os.path.join(item_path, "package.xml"))):
                    
                    # Füge Standard-Binary hinzu wenn nicht in config
                    if not any(p["name"] == item for p in REMOTE_CONFIG["debug_programs"]):
                        detected_programs.append({
                            "name": item,
                            "path": f"{item}/{item}"
                        })
    
    return REMOTE_CONFIG["debug_programs"] + detected_programs

# ============================================================================
# VALIDIERUNG
# ============================================================================

def validate_config():
    """Validiert die Konfiguration."""
    errors = []
    
    # Pflichtfelder prüfen
    required_fields = ["host", "user", "workspace"]
    for field in required_fields:
        if not REMOTE_CONFIG.get(field):
            errors.append(f"REMOTE_CONFIG['{field}'] ist erforderlich")
    
    # IP-Format grob prüfen
    host = REMOTE_CONFIG.get("host", "")
    if host and not (host.count(".") == 3 or ":" in host):
        errors.append(f"Host '{host}' scheint keine gültige IP/Hostname zu sein")
    
    return errors

if __name__ == "__main__":
    # Konfiguration testen
    errors = validate_config()
    if errors:
        print("❌ Konfigurationsfehler:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Konfiguration ist gültig")
        
    print(f"\nProjekt-Root: {get_project_root()}")
    print(f"VS Code Dir: {get_vscode_dir()}")
    print(f"Remote Host: {REMOTE_CONFIG['host']}")
    print(f"Erkannte Programme: {len(detect_project_binaries())}")
    for prog in detect_project_binaries():
        print(f"  - {prog['name']}")
