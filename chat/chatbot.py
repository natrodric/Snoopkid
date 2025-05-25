# Archivo: chat/chatbot.py

import subprocess
from utils.config import OLLAMA_MODEL

def preguntar_ia(pregunta):
    """
    Envía una pregunta al modelo definido en config.py de Ollama y devuelve la respuesta generada.
    """
    try:
        resultado = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=pregunta,
            text=True,
            capture_output=True,
            check=True
        )
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[ERROR] No se pudo obtener respuesta: {e.stderr}"
    except FileNotFoundError:
        return "[ERROR] Ollama no está instalado o no se encuentra en el PATH."
