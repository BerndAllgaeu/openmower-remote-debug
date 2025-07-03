#!/usr/bin/env python3
"""
VS Code Konfigurationsgenerator für OpenMower Remote Debug

Generiert launch.json und tasks.json basierend auf der zentralen Konfiguration.
"""

import json
import os
import sys

# Config importieren
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import REMOTE_CONFIG, get_project_root, get_vscode_dir, get_ros_environment, get_ssh_command, get_rsync_command, detect_project_binaries, get_debug_scripts_dir

def get_ssh_pipe_args():
    """Erstellt SSH pipe args für VS Code Remote Debug."""
    if "ssh_host" in REMOTE_CONFIG and REMOTE_CONFIG["ssh_host"]:
        # Verwende SSH Host aus ~/.ssh/config
        return [REMOTE_CONFIG["ssh_host"]]
    else:
        # Direkte SSH-Verbindung mit Key
        ssh_key = REMOTE_CONFIG.get("ssh_key", "~/.ssh/id_rsa_openmower")
        return [
            "-i", ssh_key,
            "-o", "StrictHostKeyChecking=no",
            f"{REMOTE_CONFIG['user']}@{REMOTE_CONFIG['host']}"
        ]

def generate_remote_debug_config(name, program_path):
    """Generiert eine Remote-Debug-Konfiguration."""
    ros_env = get_ros_environment()
    
    return {
        "name": f"Remote Debug - {name}",
        "type": "cppdbg",
        "request": "launch",
        "program": f"{REMOTE_CONFIG['workspace']}/devel/lib/{program_path}",
        "cwd": REMOTE_CONFIG['workspace'],
        "environment": [
            {"name": k, "value": v} for k, v in ros_env.items()
        ],
        "MIMode": "gdb",
        "miDebuggerPath": "/usr/bin/gdb",
        "pipeTransport": {
            "pipeCwd": "${workspaceFolder}",
            "pipeProgram": "ssh",
            "pipeArgs": get_ssh_pipe_args(),
            "debuggerPath": "/usr/bin/gdb"
        },
        "sourceFileMap": {
            REMOTE_CONFIG['workspace']: "${workspaceFolder}"
        },
        "setupCommands": [
            {
                "description": "Enable pretty-printing for gdb",
                "text": "-enable-pretty-printing",
                "ignoreFailures": True
            }
        ]
    }

def generate_launch_json():
    """Generiert die komplette launch.json."""
    programs = detect_project_binaries()
    
    # Remote Debug Konfigurationen
    remote_configs = [
        generate_remote_debug_config(prog["name"], prog["path"])
        for prog in programs
    ]
    
    # Lokale Debug Konfiguration
    local_config = {
        "name": "Local Debug - Build and Debug",
        "type": "cppdbg",
        "request": "launch",
        "program": "${workspaceFolder}/devel/lib/mower_logic/mower_logic",
        "args": [],
        "stopAtEntry": False,
        "cwd": "${workspaceFolder}",
        "environment": [
            {"name": "ROS_MASTER_URI", "value": "http://localhost:11311"},
            {"name": "ROS_IP", "value": "127.0.0.1"}
        ],
        "externalConsole": False,
        "MIMode": "gdb",
        "setupCommands": [
            {
                "description": "Enable pretty-printing for gdb",
                "text": "-enable-pretty-printing",
                "ignoreFailures": True
            }
        ],
        "preLaunchTask": "Build OpenMower Workspace",
        "miDebuggerPath": "/usr/bin/gdb"
    }
    
    # Remote ROS Environment
    remote_env_config = {
        "name": "Remote ROS Environment",
        "type": "cppdbg",
        "request": "launch",
        "program": "/bin/bash",
        "args": ["-c", f"export ROS_MASTER_URI={REMOTE_CONFIG['ros_master_uri']} && export ROS_IP={REMOTE_CONFIG['ros_dev_ip']} && bash"],
        "stopAtEntry": False,
        "cwd": "${workspaceFolder}",
        "environment": [
            {"name": "ROS_MASTER_URI", "value": REMOTE_CONFIG['ros_master_uri']},
            {"name": "ROS_IP", "value": REMOTE_CONFIG['ros_dev_ip']}
        ],
        "externalConsole": True,
        "MIMode": "gdb"
    }
    
    return {
        "version": "0.2.0",
        "configurations": remote_configs + [local_config, remote_env_config]
    }

def generate_tasks_json():
    """Generiert die komplette tasks.json."""
    ssh_base = get_ssh_command()
    rsync_base = get_rsync_command()
    
    return {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Build OpenMower Workspace",
                "type": "shell",
                "command": "source /opt/ros/noetic/setup.bash && catkin_make",
                "group": {"kind": "build", "isDefault": True},
                "options": {"cwd": "${workspaceFolder}"}
            },
            {
                "label": "Clean Build",
                "type": "shell",
                "command": "rm -rf build devel && source /opt/ros/noetic/setup.bash && catkin_make",
                "group": "build",
                "options": {"cwd": "${workspaceFolder}"}
            },
            {
                "label": "Sync Source to Pi",
                "type": "shell",
                "command": f"{rsync_base} ${{workspaceFolder}}/ {REMOTE_CONFIG['user']}@{REMOTE_CONFIG['host']}:{REMOTE_CONFIG['workspace']}/",
                "group": "build",
                "options": {"cwd": "${workspaceFolder}"}
            },
            {
                "label": "Remote Build on Pi",
                "type": "shell",
                "command": f"{ssh_base} 'cd {REMOTE_CONFIG['workspace']} && source /opt/ros/noetic/setup.bash && catkin_make'",
                "group": "build",
                "dependsOn": "Sync Source to Pi"
            },
            {
                "label": "Deploy to Raspberry Pi",
                "type": "shell",
                "command": f"{get_debug_scripts_dir()}/deploy.sh",
                "group": "build",
                "options": {"cwd": "${workspaceFolder}"},
                "dependsOn": "Build OpenMower Workspace"
            },
            {
                "label": "Start ROS Master on Pi",
                "type": "shell",
                "command": f"{ssh_base} 'export ROS_MASTER_URI=http://{REMOTE_CONFIG['host']}:11311 && export ROS_IP={REMOTE_CONFIG['host']} && roscore'",
                "group": "test",
                "isBackground": True
            },
            {
                "label": "Launch OpenMower on Pi",
                "type": "shell",
                "command": f"{ssh_base} 'cd {REMOTE_CONFIG['workspace']} && source devel/setup.bash && source ~/mower_config.sh && export ROS_MASTER_URI=http://{REMOTE_CONFIG['host']}:11311 && export ROS_IP={REMOTE_CONFIG['host']} && roslaunch open_mower open_mower.launch'",
                "group": "test",
                "isBackground": True
            },
            {
                "label": "Monitor ROS Topics",
                "type": "shell",
                "command": f"export ROS_MASTER_URI=http://{REMOTE_CONFIG['host']}:11311 && export ROS_IP={REMOTE_CONFIG['ros_dev_ip']} && rostopic list",
                "group": "test"
            },
            {
                "label": "Install Dependencies on Pi",
                "type": "shell",
                "command": f"{ssh_base} 'cd {REMOTE_CONFIG['workspace']} && source /opt/ros/noetic/setup.bash && rosdep update && rosdep install --from-paths src --ignore-src --default-yes'",
                "group": "build"
            },
            {
                "label": "Setup SSH Tunnels",
                "type": "shell",
                "command": f"{get_debug_scripts_dir()}/tunnel.sh",
                "group": "test",
                "options": {"cwd": "${workspaceFolder}"}
            },
            {
                "label": "Cleanup Remote Debug",
                "type": "shell",
                "command": f"{get_debug_scripts_dir()}/cleanup.sh",
                "group": "test",
                "options": {"cwd": "${workspaceFolder}"}
            },
            {
                "label": "Test Remote Connection",
                "type": "shell",
                "command": "./.debug/test-connection.sh",
                "group": "test",
                "options": {"cwd": "${workspaceFolder}"}
            }
        ]
    }

def copy_debug_scripts():
    """Kopiert Debug-Skripte in den devel/debug Ordner."""
    import shutil
    
    debug_dir = get_debug_scripts_dir()
    script_source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
    
    # Sicherstellen, dass Quell-Verzeichnis existiert
    if not os.path.exists(script_source_dir):
        print(f"⚠️  Script-Verzeichnis nicht gefunden: {script_source_dir}")
        return False
    
    # Skripte kopieren
    scripts_copied = 0
    for script_file in os.listdir(script_source_dir):
        if script_file.endswith('.sh'):
            src = os.path.join(script_source_dir, script_file)
            dst = os.path.join(debug_dir, script_file)
            shutil.copy2(src, dst)
            os.chmod(dst, 0o755)  # Ausführbar machen
            scripts_copied += 1
    
    print(f"📁 {scripts_copied} Debug-Skripte nach {debug_dir} kopiert")
    return True

def write_json_file(filepath, data, description):
    """Schreibt JSON-Daten in eine Datei."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"✅ {description}: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Schreiben von {description}: {e}")
        return False

def main():
    """Hauptfunktion."""
    print("🔧 Generiere VS Code Konfigurationen...")
    
    vscode_dir = get_vscode_dir()
    os.makedirs(vscode_dir, exist_ok=True)
    
    # Debug-Skripte in devel/ kopieren
    copy_debug_scripts()
    
    # Konfigurationen generieren
    launch_config = generate_launch_json()
    tasks_config = generate_tasks_json()
    
    # Dateien schreiben
    success = True
    success &= write_json_file(
        os.path.join(vscode_dir, "launch.json"),
        launch_config,
        "Debug-Konfiguration"
    )
    success &= write_json_file(
        os.path.join(vscode_dir, "tasks.json"),
        tasks_config,
        "Tasks-Konfiguration"
    )
    
    if success:
        print("\n🎉 VS Code Konfigurationen erfolgreich generiert!")
        print(f"\nKonfiguration für:")
        print(f"  Host: {REMOTE_CONFIG['host']}")
        print(f"  User: {REMOTE_CONFIG['user']}")
        print(f"  Workspace: {REMOTE_CONFIG['workspace']}")
        
        programs = detect_project_binaries()
        print(f"\nVerfügbare Debug-Programme ({len(programs)}):")
        for prog in programs:
            print(f"  - {prog['name']}")
            
    else:
        print("\n❌ Fehler beim Generieren der Konfigurationen!")
        sys.exit(1)

if __name__ == "__main__":
    main()
