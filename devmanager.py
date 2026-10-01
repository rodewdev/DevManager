#!/usr/bin/env python3
import sys
import os
import subprocess
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
    HAS_TRAY = True
except ValueError:
    HAS_TRAY = False

from gi.repository import Gtk, GLib, Vte, Gdk, GdkPixbuf

class ModernAppWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        
        self.is_dark_mode = True
        self.settings = Gtk.Settings.get_default()
        
        self.set_default_size(650, 680)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.icon_path = os.path.join(self.base_dir, "icon.jpg")
        
        if os.path.exists(self.icon_path):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.icon_path, 64, 64, True)
                self.set_icon(pixbuf)
            except Exception:
                pass

        self.css_provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), 
            self.css_provider, 
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        self.set_titlebar(hb)

        # Botón para cambiar de tema (Sol/Luna)
        self.theme_btn = Gtk.Button()
        self.theme_btn.set_tooltip_text("Cambiar Tema")
        self.theme_btn.connect("clicked", self.toggle_theme)
        hb.pack_end(self.theme_btn)

        # Stack para las pestañas
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)
        
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)
        hb.set_custom_title(stack_switcher)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)
        vbox.pack_start(self.stack, True, True, 0)

        # Definición de items
        self.items = [
            {"type": "service", "id": "apache2", "name": "PHP & Apache Stack", "desc": "Apache, PHP 8.3 & Composer", "bins": ["apache2", "php"], "script": "scripts/install_laravel.sh", "icon": "🌐", "root": True},
            {"type": "service", "id": "db", "name": "MariaDB Server", "desc": "SQL Database Engine", "bins": ["mariadb", "mysql"], "script": "scripts/install_mariadb.sh", "icon": "🗄️", "root": True},
            {"type": "service", "id": "postgresql", "name": "PostgreSQL", "desc": "Advanced Relational Database", "bins": ["psql"], "script": "scripts/install_postgresql.sh", "icon": "🐘", "root": True},
            {"type": "service", "id": "mongod", "name": "MongoDB", "desc": "NoSQL Document Database", "bins": ["mongod"], "script": "scripts/install_mongodb.sh", "icon": "🍃", "root": True},
            {"type": "service", "id": "redis-server", "name": "Redis", "desc": "In-Memory Cache & Queue", "bins": ["redis-server"], "script": "scripts/install_redis.sh", "icon": "⚡", "root": True},
            
            {"type": "language", "id": "node", "name": "Node.js (LTS)", "desc": "JavaScript Runtime & NPM", "bins": ["node", "npm"], "script": "scripts/install_node.sh", "icon": "🟩", "root": True},
            {"type": "language", "id": "go", "name": "Go (Golang)", "desc": "Latest Go Compiler", "bins": ["go"], "script": "scripts/install_go.sh", "icon": "🐹", "root": True},
            {"type": "language", "id": "rust", "name": "Rust (rustup)", "desc": "Safe Systems Language", "bins": ["cargo", "rustc"], "script": "scripts/install_rust.sh", "icon": "🦀", "root": False},
            {"type": "language", "id": "python", "name": "Python 3.13", "desc": "Latest Python via Deadsnakes", "bins": ["python3.13"], "script": "scripts/install_python.sh", "icon": "🐍", "root": True}
        ]

        self.widgets_map = {}

        box_serv = self.create_page("service")
        self.stack.add_titled(box_serv, "services", "Servicios Locales")

        box_lang = self.create_page("language")
        self.stack.add_titled(box_lang, "languages", "Compiladores")

        if HAS_TRAY:
            self.connect("delete-event", self.on_delete_event)
            self.setup_tray()
        else:
            self.connect("destroy", Gtk.main_quit)

        self.apply_theme()
        self.refresh_status()
        GLib.timeout_add_seconds(2, self.refresh_status)

    def apply_theme(self):
        self.settings.set_property("gtk-application-prefer-dark-theme", self.is_dark_mode)
        
        if self.is_dark_mode:
            self.theme_btn.set_image(Gtk.Image.new_from_icon_name("weather-clear-symbolic", Gtk.IconSize.BUTTON))
            css = b"""
            window { background-color: #121212; color: #ffffff; }
            headerbar { background-color: #1e1e1e; border-bottom: 1px solid #2d2d2d; padding: 8px; }
            .card-list { background-color: #1a1a1a; border-radius: 16px; border: 1px solid #2d2d2d; }
            list row { padding: 8px; border-bottom: 1px solid #252525; transition: all 0.2s ease; }
            list row:hover { background-color: #242424; }
            list row:last-child { border-bottom: none; }
            .service-name { font-size: 16px; font-weight: 700; color: #ffffff; }
            .service-desc { font-size: 13px; color: #a0a0a0; }
            .service-desc-running { font-size: 13px; color: #10b981; font-weight: 700; }
            .service-desc-stopped { font-size: 13px; color: #ef4444; font-weight: 700; }
            .service-desc-installed { font-size: 13px; color: #3b82f6; font-weight: 700; }
            .btn-install { background-color: #2563eb; color: white; border-radius: 12px; font-weight: 800; padding: 6px 20px; border: 1px solid #1d4ed8; }
            .btn-install:hover { background-color: #3b82f6; }
            switch { border-radius: 14px; }
            switch:checked { background-color: #10b981; }
            """
        else:
            self.theme_btn.set_image(Gtk.Image.new_from_icon_name("weather-clear-night-symbolic", Gtk.IconSize.BUTTON))
            css = b"""
            window { background-color: #f4f5f7; color: #111827; }
            headerbar { background-color: #ffffff; border-bottom: 1px solid #e5e7eb; padding: 8px; }
            .card-list { background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            list row { padding: 8px; border-bottom: 1px solid #f3f4f6; transition: all 0.2s ease; }
            list row:hover { background-color: #f9fafb; }
            list row:last-child { border-bottom: none; }
            .service-name { font-size: 16px; font-weight: 700; color: #111827; }
            .service-desc { font-size: 13px; color: #6b7280; }
            .service-desc-running { font-size: 13px; color: #10b981; font-weight: 700; }
            .service-desc-stopped { font-size: 13px; color: #ef4444; font-weight: 700; }
            .service-desc-installed { font-size: 13px; color: #3b82f6; font-weight: 700; }
            .btn-install { background-image: linear-gradient(to bottom, #3b82f6, #2563eb); color: white; border-radius: 12px; font-weight: 800; padding: 6px 20px; border: 1px solid #1d4ed8; }
            .btn-install:hover { background-image: linear-gradient(to bottom, #60a5fa, #3b82f6); }
            switch { border-radius: 14px; }
            """
        self.css_provider.load_from_data(css)

    def toggle_theme(self, widget):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def create_page(self, item_type):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_margin_top(25)
        scrolled.set_margin_bottom(25)
        scrolled.set_margin_start(35)
        scrolled.set_margin_end(35)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        listbox.get_style_context().add_class("card-list")
        
        for item in [i for i in self.items if i["type"] == item_type]:
            row = Gtk.ListBoxRow()
            hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
            hb.set_margin_top(15)
            hb.set_margin_bottom(15)
            hb.set_margin_start(18)
            hb.set_margin_end(18)
            
            icon_lbl = Gtk.Label(label=f"<span size='30000'>{item['icon']}</span>")
            icon_lbl.set_use_markup(True)
            icon_lbl.set_valign(Gtk.Align.CENTER)
            hb.pack_start(icon_lbl, False, False, 0)
            
            vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            vb.set_valign(Gtk.Align.CENTER)
            
            name_lbl = Gtk.Label(label=item["name"])
            name_lbl.set_xalign(0.0)
            name_lbl.get_style_context().add_class("service-name")
            
            desc_lbl = Gtk.Label(label=item["desc"])
            desc_lbl.set_xalign(0.0)
            desc_lbl.get_style_context().add_class("service-desc")
            
            vb.pack_start(name_lbl, False, False, 0)
            vb.pack_start(desc_lbl, False, False, 0)
            hb.pack_start(vb, True, True, 0)
            
            stack = Gtk.Stack()
            stack.set_valign(Gtk.Align.CENTER)
            
            switch = Gtk.Switch()
            switch.set_valign(Gtk.Align.CENTER)
            switch.connect("notify::active", self.on_switch_toggled, item)
            sw_box = Gtk.Box()
            sw_box.pack_start(switch, False, False, 0)
            stack.add_named(sw_box, "switch")
            
            install_btn = Gtk.Button(label="Instalar")
            install_btn.get_style_context().add_class("btn-install")
            install_btn.set_valign(Gtk.Align.CENTER)
            install_btn.connect("clicked", self.on_install_clicked, item)
            stack.add_named(install_btn, "btn")
            
            installed_lbl = Gtk.Label(label="✔️ Instalado")
            installed_lbl.get_style_context().add_class("service-desc-installed")
            stack.add_named(installed_lbl, "ready")

            hb.pack_end(stack, False, False, 0)
            row.add(hb)
            listbox.add(row)

            self.widgets_map[item["id"]] = {
                "desc_lbl": desc_lbl,
                "switch": switch,
                "stack": stack,
                "base_desc": item["desc"],
                "ignore_toggle": False
            }
            
        scrolled.add(listbox)
        return scrolled
        
    def setup_tray(self):
        self.indicator = AppIndicator.Indicator.new(
            "devmanager",
            self.icon_path if os.path.exists(self.icon_path) else "applications-development",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu()
        
        item_show = Gtk.MenuItem()
        box_show = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_show.pack_start(Gtk.Image.new_from_icon_name("window-new-symbolic", Gtk.IconSize.MENU), False, False, 0)
        box_show.pack_start(Gtk.Label(label="Mostrar Panel Principal"), False, False, 0)
        item_show.add(box_show)
        item_show.connect("activate", self.show_app)
        menu.append(item_show)
        
        item_update = Gtk.MenuItem()
        box_update = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_update.pack_start(Gtk.Image.new_from_icon_name("software-update-available-symbolic", Gtk.IconSize.MENU), False, False, 0)
        box_update.pack_start(Gtk.Label(label="Actualizar DevManager"), False, False, 0)
        item_update.add(box_update)
        item_update.connect("activate", self.update_app)
        menu.append(item_update)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        item_quit = Gtk.MenuItem()
        box_quit = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_quit.pack_start(Gtk.Image.new_from_icon_name("application-exit-symbolic", Gtk.IconSize.MENU), False, False, 0)
        box_quit.pack_start(Gtk.Label(label="Salir Completamente"), False, False, 0)
        item_quit.add(box_quit)
        item_quit.connect("activate", self.quit_app)
        menu.append(item_quit)
        
        menu.show_all()
        self.indicator.set_menu(menu)

    def on_delete_event(self, widget, event):
        self.hide()
        return True

    def show_app(self, widget):
        self.show_all()
        self.present()

    def update_app(self, widget):
        subprocess.run(["pkexec", "sh", "-c", "cd /opt/devmanager && git pull && chmod +x devmanager.py"])
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Actualización Completada")
        dialog.format_secondary_text("Se ha actualizado DevManager a la última versión. Por favor, reinicia la aplicación.")
        dialog.run()
        dialog.destroy()

    def quit_app(self, widget):
        Gtk.main_quit()

    def get_bin_path(self, b):
        paths = os.environ["PATH"].split(":")
        paths.append(os.path.expanduser("~/.cargo/bin"))
        paths.append("/usr/local/go/bin")
        for p in paths:
            exe = os.path.join(p, b)
            if os.path.isfile(exe) and os.access(exe, os.X_OK):
                return True
        return False

    def is_installed(self, bins):
        for b in bins:
            if self.get_bin_path(b): return True
        return False

    def resolve_db_service(self):
        if subprocess.run(["systemctl", "is-active", "--quiet", "mariadb"]).returncode == 0: return "mariadb"
        if subprocess.run(["systemctl", "is-active", "--quiet", "mysql"]).returncode == 0: return "mysql"
        return "mariadb"

    def get_state(self, item):
        if not self.is_installed(item["bins"]): return "not_installed"
        if item["type"] == "language": return "installed"
        
        svc = self.resolve_db_service() if item["id"] == "db" else item["id"]
        return "running" if subprocess.run(["systemctl", "is-active", "--quiet", svc]).returncode == 0 else "stopped"

    def refresh_status(self):
        for item in self.items:
            i_id = item["id"]
            state = self.get_state(item)
            w = self.widgets_map[i_id]
            lbl = w["desc_lbl"]
            sw = w["switch"]
            stack = w["stack"]

            lbl.get_style_context().remove_class("service-desc-running")
            lbl.get_style_context().remove_class("service-desc-stopped")
            lbl.get_style_context().remove_class("service-desc")

            if state == "not_installed":
                lbl.set_text("No instalado en el sistema")
                lbl.get_style_context().add_class("service-desc")
                stack.set_visible_child_name("btn")
            elif state == "installed":
                lbl.set_text(w['base_desc'])
                lbl.get_style_context().add_class("service-desc")
                stack.set_visible_child_name("ready")
            else:
                stack.set_visible_child_name("switch")
                w["ignore_toggle"] = True
                if state == "running":
                    lbl.set_text(f"{w['base_desc']} • Corriendo 🟢")
                    lbl.get_style_context().add_class("service-desc-running")
                    sw.set_active(True)
                else:
                    lbl.set_text(f"{w['base_desc']} • Detenido 🔴")
                    lbl.get_style_context().add_class("service-desc-stopped")
                    sw.set_active(False)
                w["ignore_toggle"] = False
        return True

    def on_switch_toggled(self, switch, gparam, item):
        w = self.widgets_map[item["id"]]
        if w["ignore_toggle"]: return
        
        is_active = switch.get_active()
        svc = self.resolve_db_service() if item["id"] == "db" else item["id"]
        action = "start" if is_active else "stop"
        
        switch.set_sensitive(False)
        subprocess.run(["pkexec", "systemctl", action, svc])
        switch.set_sensitive(True)
        self.refresh_status()

    def on_install_clicked(self, widget, item):
        dialog = Gtk.Dialog(parent=self, flags=0)
        dialog.set_default_size(700, 450)
        
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        hb.props.title = f"Instalando {item['name']}"
        dialog.set_titlebar(hb)
        
        vte = Vte.Terminal()
        vte.set_scrollback_lines(-1)
        vte.set_colors(foreground=Gdk.RGBA(0.9, 0.9, 0.9, 1.0), background=Gdk.RGBA(0.1, 0.1, 0.1, 1.0), palette=[])
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.add(vte)
        dialog.get_content_area().pack_start(scrolled, True, True, 0)
        
        script_path = os.path.join(self.base_dir, item["script"])
        
        cmd = ["/usr/bin/pkexec", "bash", script_path] if item["root"] else ["bash", script_path]
        
        try:
            vte.spawn_sync(Vte.PtyFlags.DEFAULT, None, cmd, None, GLib.SpawnFlags.DEFAULT, None, None, None)
        except Exception as e:
            print("Error:", e)
            
        vte.connect("child-exited", lambda term, status: dialog.destroy())
        dialog.show_all()
        dialog.run()
        dialog.destroy()
        self.refresh_status()

if __name__ == "__main__":
    app = ModernAppWindow()
    app.show_all()
    Gtk.main()
