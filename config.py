#!/usr/bin/env python3
"""
OpenMower Remote Debug Configuration

Zentrale Konfigurationsdatei für Remote-Debugging Setup.
Diese Datei wird von allen Scripts verwendet.
"""

import os

# ============================================================================
# ZENTRALE KONFIGURATION - Hier alle Parameter anpassen
# ============================================================================

REMOTE_CONFIG = {
    # Raspberry Pi Konfiguration
    "host": "192.168.1.100",                    # IP-Adresse des Pi (anpassen!)
    "user": "ubuntu",                            # SSH-Benutzername
    "ssh_key": "~/.ssh/id_rsa_openmower",        # SSH-Key Pfad
    "ssh_host": "openmower",                     # SSH Host aus ~/.ssh/config
    "workspace": "/home/ubuntu/open_mower_ros",  # Workspace-Pfad auf dem Pi
    
    # ROS Konfiguration
    "ros_master_uri": "http://192.168.1.100:11311",
    "ros_pi_ip": "192.168.1.100",
    "ros_dev_ip": "192.168.1.200",
    
    # Debug Programme (nur existierende Binaries)
    "debug_programs": [
        {"name": "mower_logic", "path": "mower_logic/mower_logic"},
        {"name": "mower_comms_v2", "path": "mower_comms_v2/mower_comms_v2"},
        {"name": "mower_map_service", "path": "mower_map/mower_map_service"},
        {"name": "monitoring", "path": "mower_logic/monitoring"},
        {"name": "mower_comms_v1", "path": "mower_comms_v1/mower_comms_v1"},
        # open_mower ist ein Launch-Package, kein Binary - nicht als Debug-Ziel
    ]
}

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
    
    # Packages ohne ausführbare Binaries (nur Launch-Files, Messages, etc.)
    excluded_packages = ["open_mower", "mower_msgs", "mower_utils"]
    
    detected_programs = []
    
    if os.path.exists(src_dir):
        for item in os.listdir(src_dir):
            item_path = os.path.join(src_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.') and item not in excluded_packages:
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
