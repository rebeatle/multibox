"""
WoW Multiboxing GUI
Interfaz gráfica usando Tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from multibox_engine import WoWMultiboxEngine
import threading

class WoWMultiboxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(" Multiboxing Control Panel - Vanilla")
        self.root.geometry("1000x800")  # Ventana más grande
        self.root.resizable(True, True)
        
        # Maximizar ventana automáticamente (opcional)
        # self.root.state('zoomed')  # Windows
        # self.root.attributes('-zoomed', True)  # Linux
        
        # Colores
        self.bg_dark = "#1a1a2e"
        self.bg_medium = "#16213e"
        self.bg_light = "#0f3460"
        self.accent = "#e94560"
        self.accent_green = "#2ecc71"
        self.accent_blue = "#3498db"
        self.text_color = "#ffffff"
        
        # Configurar estilo
        self.configure_styles()
        
        # Inicializar engine
        self.engine = WoWMultiboxEngine()
        
        # Configurar callbacks
        self.engine.on_status_change = self.update_status
        self.engine.on_windows_updated = self.update_windows_list
        self.engine.on_log_message = self.add_log_message
        
        # Crear interfaz
        self.create_widgets()
        
        # Iniciar engine
        self.engine.find_wow_windows()
        self.engine.start_keyboard_listener()
        
        # Actualizar status inicial
        self.update_status()
        
        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def configure_styles(self):
        """Configura los estilos de la interfaz"""
        self.root.configure(bg=self.bg_dark)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para frames
        style.configure("Dark.TFrame", background=self.bg_dark)
        style.configure("Medium.TFrame", background=self.bg_medium)
        
        # Estilo para labels
        style.configure("Title.TLabel", 
                       background=self.bg_dark, 
                       foreground=self.text_color,
                       font=('Arial', 16, 'bold'))
        
        style.configure("Subtitle.TLabel",
                       background=self.bg_medium,
                       foreground=self.text_color,
                       font=('Arial', 12, 'bold'))
        
        style.configure("Normal.TLabel",
                       background=self.bg_medium,
                       foreground=self.text_color,
                       font=('Arial', 10))
        
        # Estilo para botones
        style.configure("Action.TButton",
                       font=('Arial', 10, 'bold'),
                       padding=10)
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Canvas para scroll
        canvas = tk.Canvas(self.root, bg=self.bg_dark, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        # Frame principal dentro del canvas
        main_frame = ttk.Frame(canvas, style="Dark.TFrame")
        
        # Configurar scroll
        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empacar canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actualizar región de scroll cuando cambie el tamaño
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        main_frame.bind("<Configure>", configure_scroll)
        
        # Permitir scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="WoW Multiboxing Control Panel",
                               style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame,
                                   text="Servidor Privado - Vanilla Edition",
                                   style="Normal.TLabel")
        subtitle_label.pack(pady=(0, 10))
        
        # Frame superior (Status + Ventanas)
        top_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        top_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Columna izquierda - Status y controles
        left_column = ttk.Frame(top_frame, style="Medium.TFrame")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_status_panel(left_column)
        self.create_controls_panel(left_column)
        
        # Columna derecha - Lista de ventanas
        right_column = ttk.Frame(top_frame, style="Medium.TFrame")
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_windows_panel(right_column)
        
        # Frame medio - Comandos rápidos
        middle_frame = ttk.Frame(main_frame, style="Medium.TFrame")
        middle_frame.pack(fill=tk.X, pady=5)
        
        self.create_commands_panel(middle_frame)
        
        # Frame inferior - Configuración y Log
        bottom_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.create_config_panel(bottom_frame)
        self.create_log_panel(bottom_frame)
    
    def create_status_panel(self, parent):
        """Crea el panel de estado"""
        frame = ttk.LabelFrame(parent, text="Estado del Sistema", style="Medium.TFrame")
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Status labels
        status_frame = ttk.Frame(frame, style="Medium.TFrame")
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Multiboxing status
        ttk.Label(status_frame, text="Multiboxing:", style="Normal.TLabel").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.status_multibox = ttk.Label(status_frame, text="INACTIVO", style="Normal.TLabel", foreground=self.accent)
        self.status_multibox.grid(row=0, column=1, sticky=tk.E, pady=2)
        
        # Replicación status
        ttk.Label(status_frame, text="Replicación:", style="Normal.TLabel").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.status_replication = ttk.Label(status_frame, text="ACTIVA", style="Normal.TLabel", foreground=self.accent_green)
        self.status_replication.grid(row=1, column=1, sticky=tk.E, pady=2)
        
        # Solo Main status
        ttk.Label(status_frame, text="Modo Solo Main:", style="Normal.TLabel").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.status_solo_main = ttk.Label(status_frame, text="OFF", style="Normal.TLabel", foreground="#888888")
        self.status_solo_main.grid(row=2, column=1, sticky=tk.E, pady=2)
        
        # Ventanas detectadas
        ttk.Label(status_frame, text="Ventanas:", style="Normal.TLabel").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.status_windows = ttk.Label(status_frame, text="0", style="Normal.TLabel", foreground=self.accent_blue)
        self.status_windows.grid(row=3, column=1, sticky=tk.E, pady=2)
        
        status_frame.columnconfigure(1, weight=1)
    
    def create_controls_panel(self, parent):
        """Crea el panel de controles"""
        frame = ttk.LabelFrame(parent, text="Controles Principales", style="Medium.TFrame")
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        controls_frame = ttk.Frame(frame, style="Medium.TFrame")
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botón Activar/Desactivar
        self.btn_toggle = tk.Button(controls_frame, 
                                     text="⏵ ACTIVAR (F12)",
                                     command=self.toggle_active,
                                     bg=self.accent_green,
                                     fg="white",
                                     font=('Arial', 11, 'bold'),
                                     height=2,
                                     relief=tk.RAISED,
                                     cursor="hand2")
        self.btn_toggle.pack(fill=tk.X, pady=5)
        
        # Botón Pausar
        self.btn_pause = tk.Button(controls_frame,
                                    text="⏸ PAUSAR (F10)",
                                    command=self.toggle_pause,
                                    bg="#f39c12",
                                    fg="white",
                                    font=('Arial', 10, 'bold'),
                                    relief=tk.RAISED,
                                    cursor="hand2")
        self.btn_pause.pack(fill=tk.X, pady=5)
        
        # Botón Solo Main
        self.btn_solo_main = tk.Button(controls_frame,
                                        text="🎯 MODO SOLO MAIN (F7)",
                                        command=self.toggle_solo_main,
                                        bg="#34495e",
                                        fg="white",
                                        font=('Arial', 10, 'bold'),
                                        relief=tk.RAISED,
                                        cursor="hand2")
        self.btn_solo_main.pack(fill=tk.X, pady=5)
        
        # Botón Refrescar
        btn_refresh = tk.Button(controls_frame,
                               text="🔄 REFRESCAR VENTANAS (F11)",
                               command=self.refresh_windows,
                               bg=self.accent_blue,
                               fg="white",
                               font=('Arial', 10, 'bold'),
                               relief=tk.RAISED,
                               cursor="hand2")
        btn_refresh.pack(fill=tk.X, pady=5)
    
    def create_windows_panel(self, parent):
        """Crea el panel de lista de ventanas"""
        frame = ttk.LabelFrame(parent, text="Ventanas de WoW", style="Medium.TFrame")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox con scrollbar
        list_frame = ttk.Frame(frame, style="Medium.TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.windows_listbox = tk.Listbox(list_frame,
                                          yscrollcommand=scrollbar.set,
                                          bg=self.bg_light,
                                          fg=self.text_color,
                                          font=('Courier', 9),
                                          selectbackground=self.accent,
                                          height=10)
        self.windows_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.windows_listbox.yview)
        
        # Botón establecer como main
        btn_set_main = tk.Button(frame,
                                text="⭐ Establecer como MAIN",
                                command=self.set_selected_as_main,
                                bg="#9b59b6",
                                fg="white",
                                font=('Arial', 10, 'bold'),
                                cursor="hand2")
        btn_set_main.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def create_commands_panel(self, parent):
        """Crea el panel de comandos rápidos"""
        frame = ttk.LabelFrame(parent, text="Comandos Rápidos", style="Medium.TFrame")
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        commands_frame = ttk.Frame(frame, style="Medium.TFrame")
        commands_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Follow
        follow_frame = ttk.Frame(commands_frame, style="Medium.TFrame")
        follow_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(follow_frame, text="Follow:", style="Normal.TLabel", width=8).pack(side=tk.LEFT)
        self.entry_follow = tk.Entry(follow_frame, bg=self.bg_light, fg=self.text_color, 
                                     font=('Arial', 10), insertbackground='white')
        self.entry_follow.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_follow.insert(0, self.engine.config["follow_target"])
        
        btn_follow = tk.Button(follow_frame, text="Enviar (F9)", command=self.send_follow,
                              bg=self.accent_blue, fg="white", font=('Arial', 9, 'bold'),
                              cursor="hand2")
        btn_follow.pack(side=tk.LEFT, padx=5)
        
        # Assist
        assist_frame = ttk.Frame(commands_frame, style="Medium.TFrame")
        assist_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(assist_frame, text="Assist:", style="Normal.TLabel", width=8).pack(side=tk.LEFT)
        self.entry_assist = tk.Entry(assist_frame, bg=self.bg_light, fg=self.text_color,
                                     font=('Arial', 10), insertbackground='white')
        self.entry_assist.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_assist.insert(0, self.engine.config["assist_target"])
        
        btn_assist = tk.Button(assist_frame, text="Enviar (F8)", command=self.send_assist,
                              bg=self.accent, fg="white", font=('Arial', 9, 'bold'),
                              cursor="hand2")
        btn_assist.pack(side=tk.LEFT, padx=5)
    
    def create_config_panel(self, parent):
        """Crea el panel de configuración"""
        frame = ttk.LabelFrame(parent, text="Configuración", style="Medium.TFrame")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        config_frame = ttk.Frame(frame, style="Medium.TFrame")
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Blacklist
        blacklist_frame = ttk.Frame(config_frame, style="Medium.TFrame")
        blacklist_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(blacklist_frame, text="Blacklist:", style="Normal.TLabel", width=12).pack(side=tk.LEFT)
        self.entry_blacklist = tk.Entry(blacklist_frame, bg=self.bg_light, fg=self.text_color,
                                        font=('Arial', 10), insertbackground='white')
        self.entry_blacklist.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        blacklist_str = ','.join(self.engine.config["blacklisted_keys"])
        self.entry_blacklist.insert(0, blacklist_str)
        
        # Delay
        delay_frame = ttk.Frame(config_frame, style="Medium.TFrame")
        delay_frame.pack(fill=tk.X, pady=5)
        
        self.var_delay = tk.BooleanVar(value=self.engine.config["delay_enabled"])
        chk_delay = tk.Checkbutton(delay_frame, text="Delay (ms):", variable=self.var_delay,
                                   bg=self.bg_medium, fg=self.text_color,
                                   selectcolor=self.bg_light, font=('Arial', 10))
        chk_delay.pack(side=tk.LEFT)
        
        self.entry_delay = tk.Entry(delay_frame, bg=self.bg_light, fg=self.text_color,
                                    font=('Arial', 10), width=10, insertbackground='white')
        self.entry_delay.pack(side=tk.LEFT, padx=5)
        self.entry_delay.insert(0, str(self.engine.config["delay_ms"]))
        
        # Botones de acción
        btn_frame = ttk.Frame(config_frame, style="Medium.TFrame")
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_save = tk.Button(btn_frame, text="💾 GUARDAR CONFIGURACIÓN",
                            command=self.save_configuration,
                            bg=self.accent_green, fg="white",
                            font=('Arial', 10, 'bold'), cursor="hand2")
        btn_save.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        btn_clear = tk.Button(btn_frame, text="🗑️ LIMPIAR",
                             command=self.clear_configuration,
                             bg=self.accent, fg="white",
                             font=('Arial', 10, 'bold'), cursor="hand2")
        btn_clear.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def create_log_panel(self, parent):
        """Crea el panel de log de actividad"""
        frame = ttk.LabelFrame(parent, text="Log de Actividad", style="Medium.TFrame")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(frame,
                                                  height=10,
                                                  bg=self.bg_light,
                                                  fg=self.text_color,
                                                  font=('Courier', 9),
                                                  state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configurar tags de colores
        self.log_text.tag_config("Sistema", foreground=self.accent_green)
        self.log_text.tag_config("Error", foreground=self.accent)
        self.log_text.tag_config("Follow", foreground=self.accent_blue)
        self.log_text.tag_config("Assist", foreground="#e74c3c")
        self.log_text.tag_config("Config", foreground="#f39c12")
        self.log_text.tag_config("Warning", foreground="#f39c12")
    
    # === Métodos de actualización ===
    
    def update_status(self):
        """Actualiza los indicadores de estado"""
        status = self.engine.get_status()
        
        # Multiboxing
        if status["active"]:
            self.status_multibox.config(text="ACTIVO", foreground=self.accent_green)
            self.btn_toggle.config(text="⏹ DESACTIVAR (F12)", bg=self.accent)
        else:
            self.status_multibox.config(text="INACTIVO", foreground=self.accent)
            self.btn_toggle.config(text="⏵ ACTIVAR (F12)", bg=self.accent_green)
        
        # Replicación
        if status["paused"]:
            self.status_replication.config(text="PAUSADA", foreground="#f39c12")
            self.btn_pause.config(text="▶ REANUDAR (F10)")
        else:
            self.status_replication.config(text="ACTIVA", foreground=self.accent_green)
            self.btn_pause.config(text="⏸ PAUSAR (F10)")
        
        # Solo Main
        if status["solo_main_mode"]:
            self.status_solo_main.config(text="ON", foreground=self.accent_blue)
            self.btn_solo_main.config(bg=self.accent_blue)
        else:
            self.status_solo_main.config(text="OFF", foreground="#888888")
            self.btn_solo_main.config(bg="#34495e")
        
        # Ventanas
        self.status_windows.config(text=str(status["window_count"]))
    
    def update_windows_list(self, windows):
        """Actualiza la lista de ventanas"""
        self.windows_listbox.delete(0, tk.END)
        
        for w in windows:
            main_tag = " [MAIN]" if w["is_main"] else ""
            window_str = f"PID:{w['pid']:5d} | {w['title']}{main_tag}"
            self.windows_listbox.insert(tk.END, window_str)
            
            if w["is_main"]:
                # Highlight main window
                self.windows_listbox.itemconfig(tk.END, bg="#9b59b6")
    
    def add_log_message(self, source, message, timestamp):
        """Añade un mensaje al log"""
        self.log_text.config(state=tk.NORMAL)
        log_line = f"[{timestamp}] [{source}] {message}\n"
        self.log_text.insert(tk.END, log_line, source)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    # === Métodos de acción ===
    
    def toggle_active(self):
        """Toggle activación del multiboxing"""
        self.engine.toggle_active()
    
    def toggle_pause(self):
        """Toggle pausa de la replicación"""
        self.engine.toggle_pause()
    
    def toggle_solo_main(self):
        """Toggle modo solo main"""
        self.engine.toggle_solo_main()
    
    def refresh_windows(self):
        """Refresca la lista de ventanas"""
        self.engine.find_wow_windows()
    
    def send_follow(self):
        """Envía comando follow"""
        follow_name = self.entry_follow.get().strip()
        if follow_name:
            self.engine.config["follow_target"] = follow_name
            self.engine.send_follow_command()
    
    def send_assist(self):
        """Envía comando assist"""
        assist_name = self.entry_assist.get().strip()
        if assist_name:
            self.engine.config["assist_target"] = assist_name
            self.engine.send_assist_command()
    
    def set_selected_as_main(self):
        """Establece la ventana seleccionada como main"""
        selection = self.windows_listbox.curselection()
        if selection:
            idx = selection[0]
            if idx < len(self.engine.wow_windows):
                hwnd = self.engine.wow_windows[idx]["hwnd"]
                self.engine.set_main_window(hwnd)
    
    def save_configuration(self):
        """Guarda la configuración actual"""
        # Actualizar configuración desde los campos
        self.engine.config["follow_target"] = self.entry_follow.get().strip()
        self.engine.config["assist_target"] = self.entry_assist.get().strip()
        self.engine.config["delay_enabled"] = self.var_delay.get()
        
        try:
            delay_ms = int(self.entry_delay.get())
            self.engine.config["delay_ms"] = delay_ms
        except ValueError:
            pass
        
        blacklist_str = self.entry_blacklist.get().strip()
        if blacklist_str:
            self.engine.config["blacklisted_keys"] = set(blacklist_str.split(','))
        
        # Guardar
        if self.engine.save_config():
            messagebox.showinfo("Éxito", "Configuración guardada exitosamente")
    
    def clear_configuration(self):
        """Limpia la configuración"""
        if messagebox.askyesno("Confirmar", "¿Deseas limpiar toda la configuración?"):
            self.entry_follow.delete(0, tk.END)
            self.entry_assist.delete(0, tk.END)
            self.entry_blacklist.delete(0, tk.END)
            self.entry_blacklist.insert(0, "b,m")
            self.engine.config["follow_target"] = ""
            self.engine.config["assist_target"] = ""
            self.engine.save_config()
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        self.engine.stop_keyboard_listener()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = WoWMultiboxGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()