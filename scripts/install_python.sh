#!/bin/bash
set -e
echo "==========================================="
echo " Instalando Python 3.13 (Deadsnakes PPA)"
echo "==========================================="
apt update
apt install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.13 python3.13-venv python3.13-dev
echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
