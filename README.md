# DevManager 🚀

Un gestor e instalador de entornos de desarrollo local increíblemente rápido, elegante y moderno para Linux (Ubuntu/Mint/Debian). Olvídate de configuraciones interminables en la terminal; instala y gestiona tus lenguajes y bases de datos con un solo clic.

Es la alternativa definitiva y Open Source a herramientas de pago como Laravel Herd, Valet o DBngin, construida nativamente para Linux.

![DevManager Icon](icon.jpg)

## ✨ Características

- **Diseño Nativo y Elegante:** Interfaz moderna en Modo Oscuro, con soporte para bandeja del sistema (System Tray).
- **Instalación de un Clic:** Instala las versiones "Current LTS" de las herramientas más demandadas sin tocar la terminal.
- **Gestión Inteligente:** Detecta automáticamente qué tienes instalado en tu sistema.
- **Pestañas Separadas:**
  - **Servicios:** Apache & PHP 8.3, MariaDB, PostgreSQL, MongoDB, Redis.
  - **Compiladores:** Node.js 22, Go (Golang), Rust (Rustup), Python 3.13.

## 📦 Requisitos Previos

Dado que DevManager usa la tecnología nativa de ventanas de Linux (GTK3), necesitas asegurarte de tener las librerías base instaladas. Abre tu terminal y ejecuta:

```bash
sudo apt update
sudo apt install -y python3-gi gir1.2-gtk-3.0 gir1.2-vte-2.91 gir1.2-ayatanaappindicator3-0.1 git
```

## 🚀 Instalación Automática

1. Clona este repositorio en tu computadora:
```bash
git clone https://github.com/rodewdev/Devmanager.git
cd devmanager
```

2. Ejecuta el instalador mágico:
```bash
sudo ./install.sh
```

¡Eso es todo! Ahora puedes buscar **"DevManager"** en el menú de aplicaciones de tu sistema, o anclarlo a tu barra de tareas.

## 🔄 Actualizaciones

DevManager cuenta con un botón nativo en la bandeja del sistema (clic derecho en el ícono de la barra de tareas > "Actualizar DevManager") que bajará las últimas mejoras automáticamente desde GitHub.

## 🤝 Contribuciones y Open Source

Este proyecto es 100% libre. Si te gusta, ¡déjan una estrellita ⭐ en GitHub! Las contribuciones de la comunidad son súper bienvenidas.
