#!/usr/bin/env python3
import os

# Ruta por defecto para las capturas
DEFAULT_CAPTURE_DIR = '/etc/snoopkid/capturas'

# Esta variable se actualizará si el usuario define una ruta distinta
CAPTURAS_DIR = DEFAULT_CAPTURE_DIR

# Carpetas obligatorias que deben existir
SUBDIRECTORIOS = ['sniffer', 'chat', 'explorar']  # Puedes agregar más si creas otros módulos

# Definición del modelo Ollama
OLLAMA_MODEL = "mistral"  # Cambia esto por el nombre real del modelo que estés usando

def set_directorio_capturas(nueva_ruta):
    """Actualiza la ruta de capturas y crea subdirectorios si no existen."""
    global CAPTURAS_DIR
    CAPTURAS_DIR = nueva_ruta
    crear_directorios()

def crear_directorios():
    """Crea el directorio principal y los subdirectorios de capturas si no existen."""
    if not os.path.exists(CAPTURAS_DIR):
        os.makedirs(CAPTURAS_DIR)

    for sub in SUBDIRECTORIOS:
        sub_path = os.path.join(CAPTURAS_DIR, sub)
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)

# Variables específicas para módulos (esto ya las puedes usar importándolas)
CAPTURES_DIR_SNIFFER = os.path.join(CAPTURAS_DIR, 'sniffer')
CAPTURES_DIR_CHAT = os.path.join(CAPTURAS_DIR, 'chat')
CAPTURES_DIR_EXPLORAR = os.path.join(CAPTURAS_DIR, 'explorar')
