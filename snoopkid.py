#!/usr/bin/env python3
import sys
import os
import time
from datetime import datetime
from prompt_toolkit import prompt
from utils.config import CAPTURAS_DIR, set_directorio_capturas, crear_directorios

sys.path.append('/etc/snoopkid')

from modules import sniffer
from modules import explorar
from chat.chatbot import preguntar_ia
from modules import hash_cracker as crack
from modules import virustotal


def obtener_snoopkid_art(anchura):
    arte = r"""
 _____                                                                  _____ 
( ___ )----------------------------------------------------------------( ___ )
 |   |                                                                  |   | 
 |   |                                                                  |   | 
 |   |                                                                  |   | 
 |   |        ____   _   _   ___    ___   ____   _  __ ___  ____        |   | 
 |   |       / ___| | \ | | / _ \  / _ \ |  _ \ | |/ /|_ _||  _ \       |   | 
 |   |       \___ \ |  \| || | | || | | || |_) || ' /  | | | | | |      |   | 
 |   |        ___) || |\  || |_| || |_| ||  __/ | . \  | | | |_| |      |   | 
 |   |       |____/ |_| \_| \___/  \___/ |_|    |_|\_\|___||____/       |   | 
 |   |                                                                  |   | 
 |   |                                                                  |   | 
 |   |                                                                  |   | 
 |___|                                                                  |___| 
(_____)----------------------------------------------------------------(_____)
"""
    return '\n'.join([line.center(anchura) for line in arte.split('\n')])


def mostrar_menu():
    os.system('clear')
    terminal_width = os.get_terminal_size().columns
    art_width = int(terminal_width * 0.7)

    print(f"\033[1;32m{obtener_snoopkid_art(art_width)}\033[0m")

    top_border = "╔" + "═" * (art_width + 1) + "╗"
    middle_border = "╠" + "═" * (art_width + 1) + "╣"
    bottom_border = "╚" + "═" * (art_width + 1) + "╝"

    texto_1 = "🐉 Snoopkid"
    texto_2 = "🔥 Tu toolkit de confianza"

    pad_1 = (art_width - len(texto_1)) // 2
    pad_2 = (art_width - len(texto_2)) // 2

    print(f"\033[1;36m{top_border}")
    print(f"║{' ' * pad_1}{texto_1}{' ' * (art_width - len(texto_1) - pad_1)}║")
    print(f"{middle_border}")
    print(f"║{' ' * pad_2}{texto_2}{' ' * (art_width - len(texto_2) - pad_2)}║")
    print(f"{bottom_border}\033[0m")

    print("\nSelecciona una opción:")
    print("1. Iniciar Sniffer")
    print("2. Asistente IA")
    print("3. Explorar Capturas")
    print("4. Cracker de hashes")
    print("5. Analizar archivo con VirusTotal 	⏳⏳⏳ ESTE MODULO ESTA EN FASE DE PRUEBA, TODAVIA FALTA ALGUNAS CORRECIONES PARA QUE FUNCIONE CORRECTAMENTE ⏳⏳⏳")
    print("6. Salir")


def preguntar_ruta_capturas():
    if not os.path.exists(CAPTURAS_DIR):
        print(f"\nLa ruta por defecto para las capturas es: {CAPTURAS_DIR}")
        nueva_ruta = input("¿Deseas cambiarla? (Presiona Enter para usar la ruta por defecto): ").strip()
        if nueva_ruta:
            if not os.path.exists(nueva_ruta):
                os.makedirs(nueva_ruta)
            set_directorio_capturas(nueva_ruta)
            print(f"\nRuta de capturas cambiada a: {CAPTURAS_DIR}")
        else:
            crear_directorios()
            print(f"\nUsando la ruta por defecto: {CAPTURAS_DIR}")


def imprimir_progresivo(texto, delay=0.025):
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def guardar_conversacion(conversacion):
    from utils.config import CAPTURES_DIR_CHAT
    carpeta = CAPTURES_DIR_CHAT
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    fecha_hora = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archivo = os.path.join(carpeta, f'chat_{fecha_hora}.txt')
    with open(archivo, 'w') as f:
        f.write(conversacion)
    print(f"\n✅ Conversación guardada como {archivo}")


def lanzar_chat():
    os.system('clear')
    terminal_width = os.get_terminal_size().columns
    print(f"\033[1;32m{obtener_snoopkid_art(int(terminal_width * 0.7))}\033[0m")
    print("\033[1;35m💬 Asistente IA de Ciberseguridad Snoopkid\033[0m")
    print("Escribe una pregunta o duda relacionada con ciberseguridad.")
    print("Escribe \033[1;31m/bye\033[0m para salir del asistente.\n")

    conversacion = ""

    while True:
        try:
            pregunta = prompt("👤 Tú:\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Cerrando asistente IA...\n")
            break

        if pregunta.lower() in ["/bye", "salir", "exit", "quit"]:
            print("\n👋 Cerrando asistente IA...\n")
            guardar = input("¿Quieres guardar la conversación? (s/n): ").strip().lower()
            if guardar == "s":
                guardar_conversacion(conversacion)
            break

        if not pregunta:
            print("❗ No has escrito nada. Intenta de nuevo.")
            continue

        print("\n🤖 Snoopbot está pensando...\n")
        time.sleep(0.7)

        hora_respuesta = datetime.now().strftime('%H:%M:%S')
        respuesta = preguntar_ia(pregunta)
        conversacion += f"Tú: {pregunta}\nSnoopbot [{hora_respuesta}]: {respuesta}\n"
        print(f"\033[1;34m🧠 Snoopbot [{hora_respuesta}]:\033[0m")
        imprimir_progresivo(respuesta)
        print()


def explorar_capturas():
    while True:
        carpetas = explorar.listar_capturas()
        if not carpetas:
            print("❗ No se encontraron carpetas.")
            break

        print("\n📁 Carpetas encontradas:")
        for idx, carpeta in enumerate(carpetas, 1):
            print(f"{idx}. {carpeta}")

        carpeta_seleccionada = input("\nSelecciona el número de la carpeta que deseas explorar: ")

        try:
            carpeta_idx = int(carpeta_seleccionada) - 1
            if carpeta_idx < 0 or carpeta_idx >= len(carpetas):
                print("❗ Opción inválida.")
                continue
            carpeta = carpetas[carpeta_idx]
        except ValueError:
            print("❗ Opción inválida.")
            continue

        while True:
            archivos_originales = explorar.listar_archivos(carpeta)
            if not archivos_originales:
                print("❗ No se encontraron archivos.")
                break

            archivos = archivos_originales.copy()
            archivos.append("Salir al menú principal")

            print(f"\n📄 Archivos encontrados en la carpeta '{carpeta}':")
            for idx, archivo in enumerate(archivos, 1):
                print(f"{idx}. {archivo}")

            archivo_seleccionado = input("\nSelecciona el número del archivo que deseas ver: ")

            try:
                archivo_idx = int(archivo_seleccionado) - 1
                if archivo_idx < 0 or archivo_idx >= len(archivos):
                    print("❗ Opción inválida.")
                    continue
                if archivo_idx == len(archivos) - 1:
                    return
                archivo = archivos[archivo_idx]
            except ValueError:
                print("❗ Opción inválida.")
                continue

            explorar.mostrar_contenido_archivo(carpeta, archivo)


def main():
    preguntar_ruta_capturas()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            sniffer.ejecutar_sniffer()
        elif opcion == "2":
            lanzar_chat()
        elif opcion == "3":
            explorar_capturas()
        elif opcion == "4":
            crack.iniciar_crack()
        elif opcion == "5":
            virustotal.iniciar_analisis()
        elif opcion == "6":
            print("👋 Saliendo de Snoopkid...\n")
            break
        else:
            print("❗ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Saliendo de Snoopkid...\n")
