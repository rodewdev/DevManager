#!/bin/bash
set -e
echo "==========================================="
echo " Instalando Redis Server"
echo "==========================================="
apt update
apt install -y redis-server
systemctl disable redis-server
systemctl stop redis-server
echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
