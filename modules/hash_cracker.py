import hashlib
import os

def seleccionar_algoritmo():
    while True:
        print("\n=== Selecciona el tipo de hash ===")
        print("[1] MD5")
        print("[2] SHA1")
        print("[3] SHA256")
        print("[0] Salir")
        opcion = input("> ")

        algoritmos = {
            "1": "md5",
            "2": "sha1",
            "3": "sha256"
        }

        if opcion == "0":
            return None

        if opcion in algoritmos:
            return algoritmos[opcion]
        else:
            print("[!] Opción inválida. Intenta de nuevo.")

def seleccionar_diccionario():
    while True:
        print("\n=== Selecciona el diccionario ===")
        print("[1] Usar rockyou (/usr/share/wordlists/rockyou.txt)")
        print("[2] Elegir de /usr/share/wordlists")
        print("[3] Introducir ruta manual")
        print("[0] Volver")
        opcion = input("> ")

        if opcion == "0":
            return None
        elif opcion == "1":
            ruta = "/usr/share/wordlists/rockyou.txt"
            if os.path.isfile(ruta):
                return ruta
            else:
                print("[!] rockyou.txt no se encuentra en la ruta esperada.")
        elif opcion == "2":
            carpeta = "/usr/share/wordlists"
            try:
                archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
                if not archivos:
                    print("[!] No se encontraron diccionarios en esa carpeta.")
                    continue
                print("\n=== Diccionarios disponibles ===")
                for i, nombre in enumerate(archivos, 1):
                    print(f"[{i}] {nombre}")
                print("[0] Volver")

                eleccion = input("> ")
                if eleccion == "0":
                    continue
                if eleccion.isdigit() and 1 <= int(eleccion) <= len(archivos):
                    return os.path.join(carpeta, archivos[int(eleccion) - 1])
                else:
                    print("[!] Opción inválida.")
            except FileNotFoundError:
                print("[!] No se encontró la carpeta /usr/share/wordlists.")
        elif opcion == "3":
            ruta = input("Introduce la ruta absoluta del diccionario: ").strip()
            if os.path.isfile(ruta):
                return ruta
            else:
                print("[!] Archivo no encontrado.")
        else:
            print("[!] Opción inválida.")

def calcular_hash(texto, algoritmo):
    if algoritmo == "md5":
        return hashlib.md5(texto.encode()).hexdigest()
    elif algoritmo == "sha1":
        return hashlib.sha1(texto.encode()).hexdigest()
    elif algoritmo == "sha256":
        return hashlib.sha256(texto.encode()).hexdigest()
    else:
        return None

def crackear_hash(hash_objetivo, ruta_diccionario, algoritmo):
    try:
        with open(ruta_diccionario, "r", encoding="utf-8", errors="ignore") as dicc:
            for linea in dicc:
                palabra = linea.strip()
                hash_generado = calcular_hash(palabra, algoritmo)
                if hash_generado == hash_objetivo.lower():
                    return palabra
        return None
    except FileNotFoundError:
        print(f"\n[!] El archivo '{ruta_diccionario}' no existe.")
        return None

def iniciar_crack():
    while True:
        print("\n=== Hash Cracker ===")

        algoritmo = seleccionar_algoritmo()
        if not algoritmo:
            print("[*] Saliendo del crackeador de hashes.")
            return

        while True:
            hash_objetivo = input("\nIntroduce el hash a romper (o escribe 'volver' para cambiar el tipo de hash, o 'salir'): ").strip().lower()
            if hash_objetivo == "salir":
                print("[*] Saliendo del crackeador de hashes.")
                return
            if hash_objetivo == "volver":
                break

            while True:
                ruta_diccionario = seleccionar_diccionario()
                if ruta_diccionario is None:
                    break

                print("\n[*] Iniciando ataque por diccionario...")
                resultado = crackear_hash(hash_objetivo, ruta_diccionario, algoritmo)

                if resultado:
                    print(f"\n[+] ¡Hash roto! La palabra es: '{resultado}'")
                else:
                    print("\n[-] No se encontró coincidencia en el diccionario.")

                print("\n¿Qué quieres hacer ahora?")
                print("[1] Probar otro diccionario con el mismo hash")
                print("[2] Introducir otro hash")
                print("[0] Salir")
                decision = input("> ").strip()

                if decision == "1":
                    continue  # volver a elegir diccionario
                elif decision == "2":
                    break  # pedir nuevo hash
                elif decision == "0":
                    print("[*] Saliendo del crackeador de hashes.")
                    return
                else:
                    print("[!] Opción inválida. Volviendo al menú de diccionario.")

if __name__ == "__main__":
    iniciar_crack()
