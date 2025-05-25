# Archivo: modules/sniffer.py

import os
import sys
import select
from datetime import datetime
import scapy.all as scapy

# Importamos la ruta desde la configuración
from utils.config import CAPTURES_DIR_SNIFFER


TIPOS_PAQUETES = {
    1: ('ARP', lambda pkt: pkt.haslayer(scapy.ARP)),
    2: ('ICMP', lambda pkt: pkt.haslayer(scapy.ICMP)),
    3: ('DNS', lambda pkt: pkt.haslayer(scapy.DNS)),
    4: ('TCP', lambda pkt: pkt.haslayer(scapy.TCP)),
    5: ('UDP', lambda pkt: pkt.haslayer(scapy.UDP)),
    6: ('HTTP', lambda pkt: pkt.haslayer(scapy.TCP) and (b"HTTP" in bytes(pkt))),
    7: ('HTTPS', lambda pkt: pkt.haslayer(scapy.TCP) and (pkt.dport == 443 or pkt.sport == 443)),
    8: ('ICMPv6', lambda pkt: pkt.haslayer(scapy.ICMPv6ND_RS)),
    9: ('mDNS', lambda pkt: pkt.haslayer(scapy.DNS) and pkt[scapy.DNS].qd and b".local" in pkt[scapy.DNS].qd.qname)
}

def seleccionar_clasificaciones():
    print("\nSelecciona los tipos de paquetes a capturar:")
    for num, (nombre, _) in TIPOS_PAQUETES.items():
        print(f" {num}. {nombre}")
    print(" 0. Todos los tipos")
    print(" q. Cancelar / Volver al menú principal")

    seleccion = input("Introduce los números separados por espacios (ENTER = importantes): ").strip().lower()

    if seleccion == "":
        return [1, 2, 3, 4, 5]  # Por defecto los importantes
    elif seleccion == "0":
        return list(TIPOS_PAQUETES.keys())
    elif seleccion == "q":
        print("\n\033[1;33m[↩] Selección cancelada. Regresando al menú principal...\033[0m\n")
        return None

    try:
        seleccion_numeros = list(map(int, seleccion.split()))
        if all(num in TIPOS_PAQUETES for num in seleccion_numeros):
            return seleccion_numeros
        else:
            print("[ERROR] Selección inválida. Intenta de nuevo.")
            return seleccionar_clasificaciones()
    except ValueError:
        print("[ERROR] Entrada inválida. Intenta de nuevo.")
        return seleccionar_clasificaciones()

def start_sniffer(interface, filtros):
    packets = []

    def packet_callback(packet):
        for tipo in filtros:
            tipo_info = TIPOS_PAQUETES.get(tipo)
            if tipo_info and tipo_info[1](packet):
                packets.append(packet)
                print(packet.summary())
                break

    print(f"\n[INFO] Inicializando el sniffer en {interface}, puede tardar unos segundos...")
    print("[INFO] Pulsa ENTER para detener la captura... o 'q' para salir.\n")

    try:
        while True:
            scapy.sniff(iface=interface, prn=packet_callback, store=False, timeout=1)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                user_input = input()
                if user_input.strip().lower() == 'q':
                    print("\n[INFO] Salida solicitada por el usuario.")
                    break
    except KeyboardInterrupt:
        print("\n[!] Sniffer interrumpido por teclado.")

    print("\n[INFO] Sniffer detenido.")
    return packets

def save_packets(packets):
    opcion = input("¿Deseas guardar el tráfico capturado? (s/n): ").strip().lower()
    if opcion == "s":
        os.makedirs(CAPTURES_DIR_SNIFFER, exist_ok=True)
        nombre = f"snoopkid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        ruta_completa = os.path.join(CAPTURES_DIR_SNIFFER, nombre)
        scapy.wrpcap(ruta_completa, packets)
        print(f"[INFO] Captura guardada en {ruta_completa}")
    else:
        print("[INFO] Captura descartada.")

def ejecutar_sniffer():
    interface = input("Introduce la interfaz de red (ej: eth0, wlan0): ").strip()
    filtros = seleccionar_clasificaciones()

    if filtros is None:
        return  # Cancelado por el usuario

    packets = start_sniffer(interface, filtros)
    save_packets(packets)

if __name__ == "__main__":
    ejecutar_sniffer()

