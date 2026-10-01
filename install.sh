#!/bin/bash
set -e

echo "🚀 Instalando DevManager..."

# Crear directorio de instalación
INSTALL_DIR="/opt/devmanager"
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r ./* "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/devmanager.py"
sudo chmod +x "$INSTALL_DIR/scripts/"*.sh

# Crear symlink en bin
sudo ln -sf "$INSTALL_DIR/devmanager.py" /usr/local/bin/devmanager

# Crear acceso directo para el menú de inicio
DESKTOP_FILE="/usr/share/applications/devmanager.desktop"
sudo bash -c "cat > $DESKTOP_FILE" << EOL
[Desktop Entry]
Version=1.0
Name=DevManager
Comment=Gestor de Entornos de Desarrollo
Exec=/usr/local/bin/devmanager
Icon=$INSTALL_DIR/icon.jpg
Terminal=false
Type=Application
Categories=Development;
EOL

echo "✅ ¡Instalación completa!"
echo "Ahora puedes buscar 'DevManager' en tu menú de aplicaciones."
