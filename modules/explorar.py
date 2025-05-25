# Archivo: modules/explorar.py

import os
from utils.config import CAPTURAS_DIR  # Importación añadida

if not os.path.isdir(CAPTURAS_DIR):
    print("❗ El directorio de capturas no existe.")

def listar_capturas():
    """
    Lista las carpetas dentro del directorio de capturas.
    """
    if not os.path.isdir(CAPTURAS_DIR):
        return []
    carpetas = [carpeta for carpeta in os.listdir(CAPTURAS_DIR) if os.path.isdir(os.path.join(CAPTURAS_DIR, carpeta))]
    return carpetas

def listar_archivos(carpeta):
    """
    Lista los archivos dentro de una carpeta dada, sin imprimir.
    """
    ruta_carpeta = os.path.join(CAPTURAS_DIR, carpeta)
    if not os.path.isdir(ruta_carpeta):
        return []
    archivos = [archivo for archivo in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, archivo))]
    return archivos

def mostrar_contenido_archivo(carpeta, archivo):
    """
    Muestra el contenido de un archivo seleccionado.
    """
    ruta_archivo = os.path.join(CAPTURAS_DIR, carpeta, archivo)
    if not os.path.isfile(ruta_archivo):
        print("❗ El archivo no existe.")
        return

    print(f"\n📄 Contenido de '{archivo}':\n")
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
        print(contenido)
