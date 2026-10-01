#!/bin/bash
set -e
echo "==========================================="
echo " Instalando PostgreSQL Server"
echo "==========================================="
apt update
apt install -y postgresql postgresql-contrib
systemctl disable postgresql
systemctl stop postgresql
echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
