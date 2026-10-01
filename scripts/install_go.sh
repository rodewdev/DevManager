#!/bin/bash
set -e
echo "==========================================="
echo " Instalando Go (Última versión)"
echo "==========================================="
apt update
apt install -y software-properties-common
add-apt-repository -y ppa:longsleep/golang-backports
apt update
apt install -y golang-go
echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
