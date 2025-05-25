import requests
import time
import os

API_KEY = "INTRODUCE TU API KEY"

HEADERS = {
    "x-apikey": API_KEY
}

def obtener_hash_archivo(ruta):
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(ruta,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def consultar_analisis_por_hash(sha256):
    url = f"https://www.virustotal.com/api/v3/files/{sha256}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print(f"⚠ Error consultando VirusTotal: código {response.status_code}")
        return None

def subir_archivo(ruta):
    url = "https://www.virustotal.com/api/v3/files"
    with open(ruta, "rb") as f:
        files = {"file": (os.path.basename(ruta), f)}
        response = requests.post(url, headers=HEADERS, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠ Error subiendo archivo: código {response.status_code}")
        return None

def obtener_id_analisis(subida_response):
    # Según API VT, el id está en data.id
    try:
        return subida_response["data"]["id"]
    except KeyError:
        return None

def consultar_resultado_analisis(id_analisis):
    url = f"https://www.virustotal.com/api/v3/analyses/{id_analisis}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def iniciar_analisis():
    ruta = input("📂 Ruta del archivo a analizar con VirusTotal: ").strip()
    if not os.path.exists(ruta):
        print("❌ Archivo no encontrado.")
        return

    sha256 = obtener_hash_archivo(ruta)
    print("🔍 Consultando análisis previo por hash...")
    resultado = consultar_analisis_por_hash(sha256)

    if resultado:
        print("✅ Análisis previo encontrado en VirusTotal.")
        # Aquí puedes mostrar resumen básico del análisis si quieres
        print("Mostrando datos de análisis previo...")
        # TODO: Mostrar resultados más detallados según estructura JSON
        return

    print("⚠ No se encontró análisis previo. Subiendo archivo para análisis...")

    subida = subir_archivo(ruta)
    if not subida:
        print("❌ Error al subir archivo para análisis.")
        return

    id_analisis = obtener_id_analisis(subida)
    if not id_analisis:
        print("❌ No se pudo obtener ID del análisis.")
        return

    print("🔍 Esperando análisis de VirusTotal... (esto puede tardar unos segundos)")

    for intento in range(15):  # Espera hasta 15 veces (e.g. 30 segundos)
        time.sleep(2)
        analisis = consultar_resultado_analisis(id_analisis)
        if analisis and analisis.get("data", {}).get("attributes", {}).get("status") == "completed":
            print("✅ Análisis completado.")
            # Aquí mostrar detalles del análisis
            # TODO: Procesar y mostrar datos de detección
            return
        print(f"⏳ Esperando resultado... intento {intento + 1}/15")

    print("⚠ Tiempo de espera agotado para recibir el análisis.")
