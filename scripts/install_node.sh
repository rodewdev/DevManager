#!/bin/bash
set -e
echo "==========================================="
echo " Instalando Node.js (LTS Current) y NPM"
echo "==========================================="
apt update
apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt install -y nodejs
rm nodesource_setup.sh
echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
