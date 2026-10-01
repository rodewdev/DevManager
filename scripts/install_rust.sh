#!/bin/bash
set -e
echo "==========================================="
echo " Instalando Rust (Vía rustup)"
echo "==========================================="
if [ "$EUID" -eq 0 ]; then
  echo "Por favor no corras este script como root. Rustup se instala a nivel de usuario."
  sleep 3
  exit 1
fi
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
echo "==========================================="
echo " Instalación Completa."
echo " Reinicia tu terminal o cierra tu sesión para actualizar el PATH."
echo "==========================================="
read -p "Presiona Enter para salir..."
