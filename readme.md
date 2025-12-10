# 🎮 WoW Multiboxing Control Panel - Vanilla Edition

Herramienta de multiboxing para World of Warcraft (Vanilla/Servidores Privados) que permite controlar múltiples ventanas simultáneamente desde una interfaz gráfica intuitiva.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso Básico](#-uso-básico)
- [Funcionalidades](#-funcionalidades)
- [Atajos de Teclado](#%EF%B8%8F-atajos-de-teclado)
- [Configuración](#%EF%B8%8F-configuración)
- [Solución de Problemas](#-solución-de-problemas)
- [Aviso Legal](#%EF%B8%8F-aviso-legal)

---

## ✨ Características

- **Replicación de Teclas**: Replica automáticamente las teclas presionadas a todas las ventanas de WoW
- **Interfaz Gráfica**: Panel de control completo con visualización en tiempo real
- **Comandos Rápidos**: Envío automatizado de comandos `/follow` y `/assist`
- **Modo Solo Main**: Envía comandos solo a tu personaje principal
- **Sistema de Pausa**: Pausa temporal la replicación sin desactivar el programa
- **Blacklist de Teclas**: Previene la replicación de teclas específicas (ej: 'B' para bolsas, 'M' para mapa)
- **Detección Automática**: Encuentra automáticamente todas las ventanas de WoW abiertas
- **Log de Actividad**: Registro completo de todas las acciones realizadas
- **Configuración Persistente**: Guarda tu configuración entre sesiones

---

## 📦 Requisitos

### Software
- **Sistema Operativo**: Windows 7/8/10/11
- **Python**: 3.7 o superior
- **World of Warcraft**: Cliente Vanilla o servidor privado compatible

### Dependencias Python
```
pywin32>=305
pynput>=1.7.6
tkinter (incluido con Python)
```

---

## 🚀 Instalación

### 1. Clonar o descargar el repositorio
```bash
git clone <tu-repositorio>
cd wow-multibox
```

### 2. Instalar dependencias
```bash
pip install pywin32 pynput
```

### 3. Verificar instalación
```bash
python multibox_gui.py
```

---

## 🎯 Uso Básico

### Inicio Rápido

1. **Abre todas tus ventanas de WoW** que desees controlar
2. **Ejecuta el programa**: `python multibox_gui.py`
3. **Establece la ventana MAIN**: 
   - Selecciona una ventana de la lista
   - Click en "⭐ Establecer como MAIN"
4. **Configura nombres para Follow/Assist** (opcional)
5. **Presiona F12** o click en "▶ ACTIVAR" para iniciar

### Flujo de Trabajo Típico

```
1. Abrir ventanas WoW → 2. Iniciar programa → 3. Establecer MAIN → 
4. Activar (F12) → 5. Jugar normalmente → 6. F9 para Follow cuando sea necesario
```

---

## 🔧 Funcionalidades

### 1. **Sistema de Replicación**

Cuando está **ACTIVO**, todas las teclas presionadas se replican automáticamente:

- **Modo Normal**: Replica teclas desde la ventana activa a TODAS las demás ventanas
- **Modo Solo Main**: Replica teclas desde CUALQUIER ventana SOLO a la ventana MAIN

**Ejemplo Modo Normal:**
```
Ventana Activa: Personaje 2
Presionas: "1" (habilidad)
Resultado: Los personajes 1, 3, 4, 5 ejecutan la habilidad 1
```

**Ejemplo Solo Main:**
```
Ventana Activa: Personaje 3
Presionas: "2" (habilidad)
Resultado: SOLO el personaje MAIN ejecuta la habilidad 2
```

### 2. **Control de Ventanas**

#### Establecer Ventana MAIN
La ventana MAIN es tu personaje líder:
- Los slaves harán `/follow` a este personaje
- En modo Solo Main, solo esta ventana recibe comandos
- Se marca con color morado en la lista

#### Detección Automática
El programa busca ventanas con:
- "World of Warcraft" en el título
- "WoW" en el título
- Muestra PID y título completo de cada ventana

### 3. **Comandos Rápidos**

#### Follow (F9)
```
Configuración: "MainChar"
Resultado: Todas las ventanas slave ejecutan "/follow MainChar"
Uso: Hacer que todos los personajes sigan al líder
```

#### Assist (F8)
```
Configuración: "MainChar"
Resultado: Todas las ventanas slave ejecutan "/assist MainChar"
Uso: Hacer que todos los personajes ataquen el target del líder
```

**💡 Tip**: Configura estos nombres una vez y guarda la configuración

### 4. **Sistema de Pausa**

| Estado | Comportamiento |
|--------|----------------|
| **Activo + Sin Pausa** | ✅ Replica todas las teclas |
| **Activo + Pausado** | ⏸️ NO replica teclas (temporal) |
| **Inactivo** | ❌ No hace nada |

**Caso de Uso**: Pausar cuando necesitas escribir en chat privado sin que se replique

### 5. **Blacklist de Teclas**

Previene la replicación de teclas específicas:

```
Blacklist por defecto: b, m
b = Bolsas (Bags) - no quieres abrir bolsas en todas las ventanas
m = Mapa (Map) - no quieres abrir el mapa en todas las ventanas
```

**Personalizar:**
```
Entrada: b,m,i,c,p
Resultado: Bloquea B, M, I (Inventario), C (Personaje), P (Hechizos)
```

### 6. **Sistema de Delay**

Añade un pequeño retraso entre el envío de teclas:

- **Desactivado**: 10ms de delay fijo
- **Activado**: Delay personalizable (útil para conexiones lentas)
- **Recomendado**: 10-50ms para servidores privados

---

## ⌨️ Atajos de Teclado

| Tecla | Función | Descripción |
|-------|---------|-------------|
| **F12** | Activar/Desactivar | Toggle ON/OFF del multiboxing |
| **F11** | Refrescar Ventanas | Busca nuevas ventanas de WoW |
| **F10** | Pausar/Reanudar | Pausa temporal la replicación |
| **F9** | Follow | Envía comando `/follow` a slaves |
| **F8** | Assist | Envía comando `/assist` a slaves |
| **F7** | Solo Main Mode | Toggle modo solo main |

**⚠️ Importante**: Los atajos funcionan GLOBALMENTE (incluso cuando WoW está en primer plano)

---

## ⚙️ Configuración

### Archivo de Configuración
El programa guarda la configuración en: `wow_multibox_config.json`

```json
{
  "follow_target": "MainChar",
  "assist_target": "MainChar",
  "delay_enabled": false,
  "delay_ms": 10,
  "blacklisted_keys": "b,m"
}
```

### Panel de Configuración

1. **Follow Target**: Nombre del personaje para comando `/follow`
2. **Assist Target**: Nombre del personaje para comando `/assist`
3. **Delay**: Activar/desactivar y configurar milisegundos de retraso
4. **Blacklist**: Lista de teclas separadas por coma que NO se replican

**Guardar**: Click en "💾 GUARDAR CONFIGURACIÓN"  
**Limpiar**: Click en "🗑️ LIMPIAR" (resetea a valores por defecto)

---

## 🔍 Solución de Problemas

### Problema: Letras repetidas en comandos Follow/Assist

**Síntoma**: Al enviar `/follow`, aparece como `//ffoollllooww`

**Causa**: Algunos clientes de WoW procesan los mensajes de teclado demasiado rápido

**Solución Temporal**: Aumenta el delay a 20-50ms en la configuración

**Solución Permanente**: Modificar `send_key_to_window` en `multibox_engine.py`:
```python
# Cambiar el delay entre KEYDOWN y KEYUP
time.sleep(0.02)  # Aumentar de 0.01 a 0.02
```

### Problema: No detecta ventanas de WoW

**Soluciones**:
1. Asegúrate de que las ventanas de WoW están abiertas
2. Presiona F11 para refrescar la búsqueda
3. Verifica que el título de la ventana contenga "World of Warcraft" o "WoW"
4. Ejecuta el programa como Administrador

### Problema: Las teclas no se replican

**Verificar**:
1. ¿Está ACTIVO? (Estado debe ser "ACTIVO" en verde)
2. ¿Está PAUSADO? (Si dice "PAUSADA", presiona F10)
3. ¿La tecla está en la blacklist? (Revisa configuración)
4. ¿La ventana activa es de WoW? (Solo replica en ventanas de WoW)

### Problema: Comandos no llegan a todas las ventanas

**Causa**: Las ventanas slave no están correctamente identificadas

**Solución**:
1. Establece una ventana como MAIN
2. Presiona F11 para refrescar
3. Verifica que aparece "[MAIN]" en la lista

---

## 📊 Interpretación del Log

```
[14:30:45] [Sistema] Multiboxing ACTIVADO
[14:30:50] [Follow] Comando enviado a 4 ventana(s)
[14:31:20] [Config] Ventana 'WoW - Personaje1' establecida como MAIN
[14:31:25] [Error] Nombre para Follow no configurado
[14:32:10] [Sistema] Replicación PAUSADA
```

**Códigos de Color**:
- 🟢 **Verde** (Sistema): Acciones del sistema
- 🔵 **Azul** (Follow): Comandos de seguimiento
- 🔴 **Rojo** (Error/Assist): Errores y comandos de asistencia
- 🟡 **Amarillo** (Config/Warning): Configuración y advertencias

---

## 📁 Estructura del Proyecto

```
wow-multibox/
│
├── multibox_engine.py          # Motor principal (lógica de multiboxing)
├── multibox_gui.py             # Interfaz gráfica (Tkinter)
├── wow_multibox_config.json    # Configuración guardada (generado automáticamente)
└── README.md                   # Este archivo
```

---

## 🎮 Casos de Uso

### 1. Farming con 5 personajes
```
1. Abrir 5 ventanas de WoW
2. Establecer personaje principal como MAIN
3. Activar (F12)
4. F9 para que todos sigan al MAIN
5. Jugar normalmente - todos atacan lo mismo
```

### 2. Dungeons con grupo completo
```
1. Todos los personajes entran al dungeon
2. F9 para Follow
3. F8 para Assist (todos atacan el target del MAIN)
4. Usar habilidades normalmente - se replican a todos
5. F10 para pausar si necesitas escribir en chat
```

### 3. Control selectivo del MAIN
```
1. Activar modo Solo Main (F7)
2. Ahora SOLO el MAIN responde a tus teclas
3. Útil para posicionar al líder sin mover a los demás
4. F7 nuevamente para volver a modo normal
```

---

## 🛡️ Aviso Legal

**IMPORTANTE**: Esta herramienta está diseñada EXCLUSIVAMENTE para servidores privados que permiten explícitamente el multiboxing.

⚠️ **Advertencias**:
- NO usar en servidores oficiales de Blizzard (está prohibido)
- Verificar las reglas del servidor privado antes de usar
- El uso indebido puede resultar en suspensión de cuenta
- Los desarrolladores NO se hacen responsables del mal uso

✅ **Uso Legítimo**:
- Servidores privados con multiboxing permitido
- Testing y desarrollo personal
- Uso educativo

---

## 💡 Tips y Mejores Prácticas

1. **Siempre establece una ventana MAIN** antes de usar comandos Follow/Assist
2. **Guarda tu configuración** después de establecer nombres de personajes
3. **Usa la blacklist** para prevenir abrir UI innecesarias (bolsas, mapas, etc.)
4. **Pausa cuando escribas en chat** para evitar replicación no deseada
5. **Modo Solo Main** es útil para posicionar solo el líder
6. **Aumenta el delay** si experimentas lag o comandos duplicados

---

## 🔮 Características Futuras (Posibles)

- [ ] Perfiles de configuración múltiples
- [ ] Macros personalizados
- [ ] Modo "round-robin" (rotar ventanas automáticamente)
- [ ] Soporte para comandos de addon
- [ ] Hotkeys personalizables
- [ ] Exportar/Importar configuración

---

## 🤝 Contribuciones

Si deseas mejorar este proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Verifica el log de actividad en el programa
3. Asegúrate de tener las dependencias correctas instaladas

---

## 📝 Changelog

### v1.0 (Versión Actual)
- ✅ Sistema de replicación de teclas
- ✅ Comandos Follow/Assist
- ✅ Modo Solo Main
- ✅ Sistema de pausa
- ✅ Blacklist de teclas
- ✅ Configuración persistente
- ✅ Interfaz gráfica completa
- ✅ Log de actividad en tiempo real

---

## 🙏 Agradecimientos

Herramienta desarrollada para la comunidad de servidores privados de WoW Vanilla.

---

**Happy Multiboxing! 🎮⚔️**

---

*Última actualización: Noviembre 2025*