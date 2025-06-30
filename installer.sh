#!/bin/bash

# PyHund standard Linux Installer Script
# Authors: Nate Mount

echo "[PyHund:Installer ~] Executing PyHund Installer Script..."

# copy files into users local bin directory
echo "[PyHund:Installer ~] Copying PyHund files to /usr/local/bin..."
cp -r PyHund /usr/local/bin/PyHund
if [ $? -ne 0 ]; then
    echo "[PyHund:Installer ~] Error copying files to /usr/local/bin. Please check permissions."
    exit 1
fi
echo "[PyHund:Installer ~] Files copied successfully."

# Build sh script for PyHund
echo "[PyHund:Installer ~] Creating PyHund executable script..."
cat << 'EOF' > /usr/local/bin/pyhund
#!/bin/bash
# PyHund executable script
PYHUND_DIR="/usr/local/bin/PyHund"
if [ -d "$PYHUND_DIR" ]; then
    exec python3 "$PYHUND_DIR/__main__.py" "$@"
else
    echo "PyHund directory not found. Please ensure PyHund is installed correctly."
    exit 1
fi
EOF

# Make the script executable
chmod 777 /usr/local/bin/pyhund

# print success message
echo "[PyHund:Installer ~] PyHund installation completed successfully!"
echo "[PyHund:Installer ~] You can now run PyHund by typing 'pyhund' in your terminal."