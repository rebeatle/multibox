"""
WoW Multiboxing Engine
Módulo que contiene toda la lógica para el multiboxing
"""

import win32gui
import win32con
import win32api
import win32process
import time
import json
import os
from pynput import keyboard
from datetime import datetime
from typing import List, Dict, Callable, Optional

class WoWMultiboxEngine:
    """Motor principal del multiboxing"""
    
    def __init__(self):
        self.wow_windows: List[Dict] = []
        self.active: bool = False
        self.paused: bool = False
        self.solo_main_mode: bool = False
        self.main_window: Optional[int] = None
        self.config_file: str = "wow_multibox_config.json"
        
        # Callbacks para eventos (usado por la GUI)
        self.on_status_change: Optional[Callable] = None
        self.on_windows_updated: Optional[Callable] = None
        self.on_log_message: Optional[Callable] = None
        
        # Configuración por defecto
        self.config = {
            "follow_target": "",
            "assist_target": "",
            "delay_enabled": False,
            "delay_ms": 10,
            "keys_to_replicate": set('abcdefghijklmnopqrstuvwxyz1234567890 '),
            "blacklisted_keys": set(['b', 'm']),
        }
        
        # Listener de teclado
        self.keyboard_listener = None
        
        self.load_config()
    
    def log(self, source: str, message: str):
        """Registra un mensaje en el log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{source}] {message}"
        print(log_entry)
        
        if self.on_log_message:
            self.on_log_message(source, message, timestamp)
    
    def load_config(self):
        """Carga la configuración desde archivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved = json.load(f)
                    self.config["follow_target"] = saved.get("follow_target", "")
                    self.config["assist_target"] = saved.get("assist_target", "")
                    self.config["delay_enabled"] = saved.get("delay_enabled", False)
                    self.config["delay_ms"] = saved.get("delay_ms", 10)
                    
                    # Cargar blacklist
                    blacklist = saved.get("blacklisted_keys", "b,m")
                    if blacklist:
                        self.config["blacklisted_keys"] = set(blacklist.split(','))
                
                self.log("Config", "Configuración cargada desde archivo")
            except Exception as e:
                self.log("Error", f"Error cargando configuración: {e}")
    
    def save_config(self):
        """Guarda la configuración en archivo JSON"""
        try:
            save_data = {
                "follow_target": self.config["follow_target"],
                "assist_target": self.config["assist_target"],
                "delay_enabled": self.config["delay_enabled"],
                "delay_ms": self.config["delay_ms"],
                "blacklisted_keys": ','.join(self.config["blacklisted_keys"])
            }
            with open(self.config_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            self.log("Config", "Configuración guardada exitosamente")
            return True
        except Exception as e:
            self.log("Error", f"Error guardando configuración: {e}")
            return False
    
    def get_process_id(self, hwnd: int) -> Optional[int]:
        """Obtiene el PID de una ventana"""
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return pid
        except:
            return None
    
    def find_wow_windows(self) -> int:
        """Encuentra todas las ventanas de WoW con PID y HWND"""
        self.wow_windows = []
        
        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                print(window_text)
                # Buscar ventanas de WoW
                if any(keyword in window_text.lower() for keyword in ["world of warcraft", "wow"]):
                    pid = self.get_process_id(hwnd)
                    if pid:
                        window_info = {
                            "hwnd": hwnd,
                            "pid": pid,
                            "title": window_text,
                            "is_main": hwnd == self.main_window
                        }
                        self.wow_windows.append(window_info)
        
        win32gui.EnumWindows(callback, None)
        
        self.log("Sistema", f"{len(self.wow_windows)} ventanas de WoW encontradas")
        
        if self.on_windows_updated:
            self.on_windows_updated(self.wow_windows)
        
        return len(self.wow_windows)
    
    def set_main_window(self, hwnd: int):
        """Establece una ventana como la principal"""
        self.main_window = hwnd
        for w in self.wow_windows:
            w["is_main"] = (w["hwnd"] == hwnd)
        
        main_title = next((w["title"] for w in self.wow_windows if w["hwnd"] == hwnd), "Unknown")
        self.log("Config", f"Ventana '{main_title}' establecida como MAIN")
        
        if self.on_windows_updated:
            self.on_windows_updated(self.wow_windows)
    
    def get_foreground_window(self) -> int:
        """Obtiene la ventana activa actual"""
        return win32gui.GetForegroundWindow()
    
    def is_wow_window(self, hwnd: int) -> bool:
        """Verifica si una ventana es de WoW"""
        return any(w["hwnd"] == hwnd for w in self.wow_windows)
    
    def send_key_to_window(self, hwnd: int, key, is_special: bool = False):
        """Envía una tecla a una ventana específica sin activarla"""
        try:
            if is_special:
                vk_code = key
            else:
                vk_code = win32api.VkKeyScan(key)
            
            # WM_KEYDOWN
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
            
            if self.config["delay_enabled"]:
                time.sleep(self.config["delay_ms"] / 1000.0)
            else:
                time.sleep(0.01)
            
            # WM_KEYUP
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
            
        except Exception as e:
            self.log("Error", f"Error enviando tecla: {e}")
    
    def send_text_to_window(self, hwnd: int, text: str):
        """Envía texto completo a una ventana"""
        for char in text:
            self.send_key_to_window(hwnd, char)
            time.sleep(0.02)
    
    def send_command_to_slaves(self, command: str) -> int:
        """Envía un comando de chat a todas las ventanas slave"""
        slaves = [w for w in self.wow_windows if not w["is_main"]]
        
        if not slaves:
            self.log("Warning", "No hay ventanas slave detectadas")
            return 0
        
        VK_RETURN = 0x0D
        
        for w in slaves:
            # Presionar ENTER para abrir chat
            self.send_key_to_window(w["hwnd"], VK_RETURN, is_special=True)
            time.sleep(0.05)
            
            # Escribir el comando
            self.send_text_to_window(w["hwnd"], command)
            time.sleep(0.05)
            
            # Presionar ENTER para enviar
            self.send_key_to_window(w["hwnd"], VK_RETURN, is_special=True)
        
        return len(slaves)
    
    def send_follow_command(self) -> bool:
        """Envía comando /follow"""
        if not self.config["follow_target"]:
            self.log("Error", "Nombre para Follow no configurado")
            return False
        
        command = f"/follow {self.config['follow_target']}"
        count = self.send_command_to_slaves(command)
        self.log("Follow", f"Comando enviado a {count} ventana(s)")
        return count > 0
    
    def send_assist_command(self) -> bool:
        """Envía comando /assist"""
        if not self.config["assist_target"]:
            self.log("Error", "Nombre para Assist no configurado")
            return False
        
        command = f"/assist {self.config['assist_target']}"
        count = self.send_command_to_slaves(command)
        self.log("Assist", f"Comando enviado a {count} ventana(s)")
        return count > 0
    
    def replicate_key(self, key_char: str):
        """Replica una tecla a las ventanas correspondientes"""
        if not self.active or self.paused:
            return
        
        # Verificar si la tecla está en la blacklist
        if key_char in self.config["blacklisted_keys"]:
            return
        
        # Verificar si la tecla debe replicarse
        if key_char not in self.config["keys_to_replicate"]:
            return
        
        current_window = self.get_foreground_window()
        
        # Solo replicar si la ventana actual es de WoW
        if not self.is_wow_window(current_window):
            return
        
        # Determinar ventanas objetivo
        if self.solo_main_mode:
            target_windows = [w for w in self.wow_windows if w["is_main"]]
        else:
            target_windows = [w for w in self.wow_windows if w["hwnd"] != current_window]
        
        # Enviar tecla a ventanas objetivo
        for w in target_windows:
            self.send_key_to_window(w["hwnd"], key_char)
    
    def toggle_active(self):
        """Activa/desactiva el multiboxing"""
        self.active = not self.active
        status = "ACTIVADO" if self.active else "DESACTIVADO"
        self.log("Sistema", f"Multiboxing {status}")
        
        if self.on_status_change:
            self.on_status_change()
    
    def toggle_pause(self):
        """Pausa/reanuda la replicación"""
        if self.active:
            self.paused = not self.paused
            status = "PAUSADA" if self.paused else "REANUDADA"
            self.log("Sistema", f"Replicación {status}")
            
            if self.on_status_change:
                self.on_status_change()
    
    def toggle_solo_main(self):
        """Activa/desactiva el modo solo main"""
        self.solo_main_mode = not self.solo_main_mode
        status = "ACTIVADO" if self.solo_main_mode else "DESACTIVADO"
        self.log("Sistema", f"Modo Solo Main {status}")
        
        if self.on_status_change:
            self.on_status_change()
    
    def on_key_press(self, key):
        """Callback cuando se presiona una tecla"""
        try:
            # F12: Toggle activación
            if key == keyboard.Key.f12:
                self.toggle_active()
                return
            
            # F10: Pausar/Reanudar
            if key == keyboard.Key.f10:
                self.toggle_pause()
                return
            
            # F11: Refrescar ventanas
            if key == keyboard.Key.f11:
                self.find_wow_windows()
                return
            
            # F9: Enviar Follow
            if key == keyboard.Key.f9:
                self.send_follow_command()
                return
            
            # F8: Enviar Assist
            if key == keyboard.Key.f8:
                self.send_assist_command()
                return
            
            # F7: Toggle Solo Main Mode
            if key == keyboard.Key.f7:
                self.toggle_solo_main()
                return
            
            # Replicar teclas normales
            if hasattr(key, 'char') and key.char:
                key_char = key.char.lower()
                self.replicate_key(key_char)
            
            # Tecla espacio
            elif key == keyboard.Key.space:
                self.replicate_key(' ')
                
        except AttributeError:
            pass
    
    def start_keyboard_listener(self):
        """Inicia el listener de teclado"""
        if self.keyboard_listener is None or not self.keyboard_listener.running:
            self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
            self.keyboard_listener.start()
            self.log("Sistema", "Listener de teclado iniciado")
    
    def stop_keyboard_listener(self):
        """Detiene el listener de teclado"""
        if self.keyboard_listener and self.keyboard_listener.running:
            self.keyboard_listener.stop()
            self.log("Sistema", "Listener de teclado detenido")
    
    def get_status(self) -> Dict:
        """Obtiene el estado actual del sistema"""
        return {
            "active": self.active,
            "paused": self.paused,
            "solo_main_mode": self.solo_main_mode,
            "window_count": len(self.wow_windows),
            "has_main": self.main_window is not None
        }