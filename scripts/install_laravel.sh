#!/bin/bash
set -e
echo "==========================================="
echo " Instalando Entorno PHP (Apache + PHP 8.3)"
echo "==========================================="
apt update
apt install -y software-properties-common curl zip unzip git
LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php -y
apt update
apt install -y php8.3 php8.3-cli php8.3-common php8.3-curl php8.3-mbstring php8.3-xml php8.3-zip php8.3-mysql php8.3-sqlite3 php8.3-bcmath php8.3-intl libapache2-mod-php8.3 apache2
systemctl disable apache2
systemctl stop apache2

curl -sS https://getcomposer.org/installer -o composer-setup.php
php composer-setup.php --install-dir=/usr/local/bin --filename=composer
rm composer-setup.php

echo "==========================================="
echo " Instalación Completa. Puedes cerrar esta ventana."
read -p "Presiona Enter para salir..."
