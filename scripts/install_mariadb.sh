#!/bin/bash
set -e
echo "==========================================="
echo " Instalando MariaDB Server"
echo "==========================================="
apt update
apt install -y mariadb-server
systemctl disable mariadb
systemctl stop mariadb
echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
