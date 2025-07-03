# Setup Guide for Local Configuration

The OpenMower Remote Debug Setup now uses a template-based configuration system for local settings.

## Initial Setup

1. **Copy template:**
   ```bash
   cd devel/debug-tools
   cp config_local.py.template config_local.py
   ```

2. **Edit local settings:**
   ```bash
   nano config_local.py
   ```
   
   Adapt the following values to your environment:
   - `host`: IP address of your Raspberry Pi
   - `ros_master_uri`: ROS Master URI with your Pi's IP
   - `ros_pi_ip`: Pi IP for ROS communication
   - `ros_dev_ip`: IP of your development machine

3. **Setup SSH:**
   See `SSH-SETUP.md` for detailed instructions

4. **Generate VS Code configurations:**
   ```bash
   ./generate-vscode.sh
   ```

## Structure

```
devel/debug-tools/
├── config.py                    # Main configuration (in Git)
├── config_local.py.template     # Template for local settings (in Git)  
├── config_local.py              # Your local settings (git-ignored)
├── generate-vscode.py           # VS Code generator
└── ...
```

## Benefits

✅ **Git-clean**: No local IPs in Git history
✅ **Team-friendly**: Each developer can have their own `config_local.py`
✅ **Easy commits**: No IP sanitization needed
✅ **Fallback**: Works even without `config_local.py`

## Troubleshooting

- **"config_local.py not found"**: Execute step 1
- **"SSH connection failed"**: Check SSH setup (see SSH-SETUP.md)
- **"Binary not found"**: Run `catkin_make` on the Pi
