# OpenMower Remote Debug Setup

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security](https://img.shields.io/badge/Security-SSH%20Keys-green.svg)](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

A portable, secure remote debugging setup for OpenMower projects. Can be integrated as a Git submodule into various OpenMower repositories.

## 🎯 Features

- ✅ **SSH Key Authentication** - No passwords in code
- ✅ **Template-based Configuration** - Local settings separated from Git
- ✅ **Automatic VS Code Debug/Tasks Generation** - Plug & Play
- ✅ **Portable across Branches/Forks** - Works everywhere
- ✅ **Clean Git History** - No sensitive data in commits
- ✅ **Cross-platform Support** - Linux, macOS, Windows
- ✅ **Comprehensive Binary Detection** - All OpenMower programs supported

## 🚀 Quick Start

### Method 1: As Git Submodule (Recommended)

```bash
# In your OpenMower project root directory
git submodule add https://github.com/BerndAllgaeu/openmower-remote-debug.git devel/debug-tools

# Setup local configuration
cd devel/debug-tools
cp config_local.py.template config_local.py
nano config_local.py  # Edit with your Pi's IP and settings

# Generate VS Code configurations
./generate-vscode.sh

# Open VS Code and press F5 for remote debugging
code .
```

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/BerndAllgaeu/openmower-remote-debug.git devel/debug-tools

# Setup local configuration
cd devel/debug-tools
cp config_local.py.template config_local.py
nano config_local.py  # Edit with your network settings
```

## ⚙️ Configuration

The setup uses a template-based configuration system:

### Files Structure
```
devel/debug-tools/
├── config.py                    # Main logic + project settings (Git tracked)
├── config_local.py.template     # Template for local settings (Git tracked)
├── config_local.py              # Your local network settings (Git ignored)
├── SETUP.md                     # Setup instructions
└── SSH-SETUP.md                 # SSH configuration guide
```

### Local Configuration

Edit `config_local.py` with your specific network settings:

```python
LOCAL_CONFIG = {
    # Raspberry Pi Connection
    "host": "192.168.1.100",                    # Your Pi's IP address
    "user": "ubuntu",                            # SSH username
    "ssh_key": "~/.ssh/id_rsa_openmower",        # SSH key path
    "ssh_host": "openmower",                     # SSH host from ~/.ssh/config
    "workspace": "/home/ubuntu/open_mower_ros",  # Workspace path on Pi
    
    # ROS Network Configuration
    "ros_master_uri": "http://192.168.1.100:11311",  # ROS Master URI
    "ros_pi_ip": "192.168.1.100",                     # Pi IP for ROS
    "ros_dev_ip": "192.168.1.200",                    # Development machine IP
}
```

## � Available Debug Programs

After setup, the following debug configurations are available:

### Core Programs
- **mower_logic** - Main mower logic
- **mower_comms_v1/v2** - Hardware communication
- **mower_map_service** - Map management
- **monitoring** - System monitoring

### Simulation & Planning
- **mower_simulation** - Mower simulation
- **slic3r_coverage_planner** - Path planning

### XBot Framework
- **xbot_positioning** - GPS positioning
- **xbot_monitoring** - System monitoring
- **xbot_remote** - Remote control

### Hardware Drivers
- **driver_gps_node** - GPS driver
- **xesc_driver_node** - ESC driver

## 📋 Commands

```bash
./generate-vscode.sh            # Generate VS Code configurations
./test-connection.sh            # Test connection to Pi
python3 config.py               # Validate configuration
```

## 🔐 SSH Setup

See [SSH-SETUP.md](SSH-SETUP.md) for detailed SSH key configuration.

Quick SSH setup:
```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_openmower

# Copy to Pi
ssh-copy-id -i ~/.ssh/id_rsa_openmower.pub ubuntu@YOUR_PI_IP

# Test connection
ssh -i ~/.ssh/id_rsa_openmower ubuntu@YOUR_PI_IP
```

## 🔄 Updates

```bash
# Update submodule
git submodule update --remote devel/debug-tools

# Regenerate configurations
devel/debug-tools/generate-vscode.sh
```

## 🛠️ Troubleshooting

### Connection Issues
```bash
./test-connection.sh           # Test SSH connection
```

### Missing config_local.py
```bash
cp config_local.py.template config_local.py
nano config_local.py          # Edit with your settings
```

### Binary not found
```bash
# On your Pi
cd /home/ubuntu/open_mower_ros
source /opt/ros/noetic/setup.bash
catkin_make
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test with multiple OpenMower projects
4. Submit a pull request

## 📞 Support

- Create an issue for bugs or feature requests
- Check [SETUP.md](SETUP.md) for detailed setup instructions
- See [SSH-SETUP.md](SSH-SETUP.md) for SSH configuration help

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.
