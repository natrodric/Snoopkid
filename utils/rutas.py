import os

def preguntar_ruta_capturas():
    """
    Pregunta al usuario una ruta para guardar las capturas.
    Si la ruta no existe, la crea.
    Devuelve la ruta asegurándose de que es válida.
    """
    ruta = input("Introduce la ruta donde quieres guardar las capturas (o pulsa Enter para usar /etc/snoopkid/capturas/): ").strip()
    
    if not ruta:
        ruta = "/etc/snoopkid/capturas"

    # Normalizamos la ruta por seguridad
    ruta = os.path.abspath(ruta)

    # Comprobamos si existe, si no, la creamos
    if not os.path.exists(ruta):
        try:
            os.makedirs(ruta)
            print(f"Se ha creado la ruta: {ruta}")
        except Exception as e:
            print(f"Error al crear la ruta: {e}")
            print("Se usará la ruta por defecto /etc/snoopkid/capturas/")
            ruta = "/etc/snoopkid/capturas"
            os.makedirs(ruta, exist_ok=True)

    return ruta
