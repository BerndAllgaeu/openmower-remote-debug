#!/usr/bin/env python3
"""
OpenMower Remote Debug Configuration

Central configuration file for remote debugging setup.
This file is used by all scripts.

Setup:
1. Copy config_local.py.template to config_local.py
2. Adapt config_local.py to your environment
3. config_local.py is automatically ignored by Git
"""

import os

# ============================================================================
# PROJECT-SPECIFIC CONFIGURATION (tracked in Git)
# ============================================================================

# Debug Programs (correct binary paths from devel/lib/)
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
    # open_mower is a launch package, not a binary - excluded
]

# Packages without executable binaries (only launch files, etc.)
EXCLUDED_PACKAGES = ["open_mower", "mower_msgs", "mower_utils", "mower_map"]

# ============================================================================
# DEFAULT VALUES (can be overridden in config_local.py)
# ============================================================================

DEFAULT_CONFIG = {
    # Connection details
    "host": "192.168.1.100",
    "user": "openmower",
    "workspace": "/home/openmower/openmower_ros",
    
    # SSH settings
    "ssh_key": "~/.ssh/id_rsa_openmower",
    "ssh_host": "",  # Optional: use SSH host from ~/.ssh/config
    
    # ROS Configuration
    "ros_master_uri": "http://192.168.1.100:11311",
    "ros_pi_ip": "192.168.1.100",
    "ros_dev_ip": "192.168.1.200",
}

# ============================================================================
# CONFIGURATION LOADING AND MERGING
# ============================================================================

def load_config(verbose=False):
    """
    Loads configuration from config_local.py if available,
    otherwise uses default values.
    """
    config = DEFAULT_CONFIG.copy()
    
    try:
        # Try to import local configuration
        from config_local import LOCAL_CONFIG
        config.update(LOCAL_CONFIG)
        if verbose:
            print("✅ Local configuration loaded from config_local.py")
    except ImportError:
        if verbose:
            print("⚠️  config_local.py not found - using default values")
            print("   Tip: cp config_local.py.template config_local.py")
    except Exception as e:
        if verbose:
            print(f"❌ Error loading config_local.py: {e}")
            print("   Using default values")
    
    # Add debug programs
    config["debug_programs"] = DEBUG_PROGRAMS
    
    return config

# Load global configuration
REMOTE_CONFIG = load_config()

# ============================================================================
# AUTOMATIC DETECTION - Usually no need to change
# ============================================================================

def get_project_root():
    """Determines the root directory of the OpenMower project."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up until we find src/ or CMakeLists.txt
    while current_dir != "/":
        if (os.path.exists(os.path.join(current_dir, "src")) and 
            os.path.exists(os.path.join(current_dir, "CMakeLists.txt"))):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # Fallback: If we're in devel/debug-tools, go two levels up
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir.endswith("devel/debug-tools"):
        return os.path.dirname(os.path.dirname(script_dir))
    
    # Fallback: Parent directory of debug-tools folder
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_vscode_dir():
    """Determines the .vscode directory."""
    return os.path.join(get_project_root(), ".vscode")

def get_debug_scripts_dir():
    """Determines directory for debug scripts (in devel/ folder)."""
    debug_dir = os.path.join(get_project_root(), "devel", "debug")
    os.makedirs(debug_dir, exist_ok=True)
    return debug_dir

def get_temp_dir():
    """Determines temporary directory for debug files."""
    temp_dir = os.path.join(get_project_root(), "devel", "tmp")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def get_ros_environment():
    """Determines ROS environment variables."""
    return {
        "ROS_MASTER_URI": REMOTE_CONFIG["ros_master_uri"],
        "ROS_IP": REMOTE_CONFIG["ros_pi_ip"],
        "ROS_PACKAGE_PATH": f"{REMOTE_CONFIG['workspace']}/src:/opt/ros/noetic/share",
        "LD_LIBRARY_PATH": f"{REMOTE_CONFIG['workspace']}/devel/lib:/opt/ros/noetic/lib",
        "CMAKE_PREFIX_PATH": f"{REMOTE_CONFIG['workspace']}/devel:/opt/ros/noetic",
        "PYTHONPATH": f"{REMOTE_CONFIG['workspace']}/devel/lib/python3/dist-packages:/opt/ros/noetic/lib/python3/dist-packages"
    }

def get_ssh_command():
    """Creates SSH base command with SSH key."""
    if "ssh_host" in REMOTE_CONFIG and REMOTE_CONFIG["ssh_host"]:
        # Use SSH host from ~/.ssh/config
        return f"ssh {REMOTE_CONFIG['ssh_host']}"
    else:
        # Direct SSH connection with key
        ssh_key = REMOTE_CONFIG.get("ssh_key", "~/.ssh/id_rsa_openmower")
        return f"ssh -i {ssh_key} -o StrictHostKeyChecking=no {REMOTE_CONFIG['user']}@{REMOTE_CONFIG['host']}"

def get_ssh_full_command(extra_args=""):
    """Creates full SSH command for script usage."""
    if "ssh_host" in REMOTE_CONFIG and REMOTE_CONFIG["ssh_host"]:
        # Use SSH host from ~/.ssh/config - already includes user and host
        return f"ssh {extra_args} {REMOTE_CONFIG['ssh_host']}" if extra_args else f"ssh {REMOTE_CONFIG['ssh_host']}"
    else:
        # Direct SSH connection with key
        ssh_key = REMOTE_CONFIG.get("ssh_key", "~/.ssh/id_rsa_openmower")
        base_cmd = f"ssh -i {ssh_key} -o StrictHostKeyChecking=no"
        if extra_args:
            base_cmd += f" {extra_args}"
        return f"{base_cmd} {REMOTE_CONFIG['user']}@{REMOTE_CONFIG['host']}"

def get_rsync_command():
    """Creates rsync base command with SSH key."""
    if "ssh_host" in REMOTE_CONFIG and REMOTE_CONFIG["ssh_host"]:
        # Use SSH host from ~/.ssh/config - only need 'ssh' in -e parameter
        return f"rsync -avz --exclude='build/' --exclude='devel/' --exclude='.git/' -e 'ssh'"
    else:
        # Direct SSH connection with key
        ssh_key = REMOTE_CONFIG.get("ssh_key", "~/.ssh/id_rsa_openmower")
        ssh_cmd = f"ssh -i {ssh_key} -o StrictHostKeyChecking=no"
        return f"rsync -avz --exclude='build/' --exclude='devel/' --exclude='.git/' -e '{ssh_cmd}'"

# ============================================================================
# PROJECT-SPECIFIC DETECTION
# ============================================================================

def detect_project_binaries():
    """Detects available binaries in the project automatically."""
    project_root = get_project_root()
    src_dir = os.path.join(project_root, "src")
    
    detected_programs = []
    
    if os.path.exists(src_dir):
        for item in os.listdir(src_dir):
            item_path = os.path.join(src_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.') and item not in EXCLUDED_PACKAGES:
                # Check if it's a ROS package (CMakeLists.txt + package.xml)
                if (os.path.exists(os.path.join(item_path, "CMakeLists.txt")) and
                    os.path.exists(os.path.join(item_path, "package.xml"))):
                    
                    # Add standard binary if not in config
                    if not any(p["name"] == item for p in REMOTE_CONFIG["debug_programs"]):
                        detected_programs.append({
                            "name": item,
                            "path": f"{item}/{item}"
                        })
    
    return REMOTE_CONFIG["debug_programs"] + detected_programs

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validates the configuration."""
    errors = []
    
    # Check required fields
    required_fields = ["host", "user", "workspace"]
    for field in required_fields:
        if not REMOTE_CONFIG.get(field):
            errors.append(f"REMOTE_CONFIG['{field}'] is required")
    
    # Check IP format roughly
    host = REMOTE_CONFIG.get("host", "")
    if host and not (host.count(".") == 3 or ":" in host):
        errors.append(f"Host '{host}' doesn't seem to be a valid IP/hostname")
    
    return errors

if __name__ == "__main__":
    # Test configuration when run directly
    REMOTE_CONFIG = load_config(verbose=True)
    errors = validate_config()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration is valid")
        
    print(f"\nProject Root: {get_project_root()}")
