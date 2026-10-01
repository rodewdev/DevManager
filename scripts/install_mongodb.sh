#!/bin/bash
set -e
echo "==========================================="
echo " Instalando MongoDB Community Server"
echo "==========================================="
apt update
apt install -y curl gnupg
curl -fsSL https://pgp.mongodb.com/server-9.0.asc | gpg -o /usr/share/keyrings/mongodb-server-9.0.gpg --dearmor --yes
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-9.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/9.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-9.0.list
apt update
apt install -y mongodb-org
systemctl disable mongod || true
systemctl stop mongod || true

mkdir -p /etc/systemd/system/mongod.service.d/
cat << 'INNEREOF' > /etc/systemd/system/mongod.service.d/override.conf
[Service]
Environment="GLIBC_TUNABLES="
UnsetEnvironment=GLIBC_TUNABLES
INNEREOF
systemctl daemon-reload

echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
