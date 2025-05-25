# 🕵️‍♂️ Snoopkid

**Snoopkid** es un toolkit de ciberseguridad en desarrollo, diseñado para ofrecer una colección de herramientas útiles para análisis, pruebas y automatización en terminal. Es un proyecto modular, con una arquitectura que facilita la ampliación progresiva mediante nuevos módulos.

> 🚧 Este proyecto está en construcción. Aún faltan funcionalidades por pulir y herramientas por completar. La idea es seguir desarrollándolo poco a poco e ir incorporando nuevas utilidades.

---

## 🔧 Funcionalidades actuales

### 🔹 Sniffer de red
Captura tráfico en vivo y guarda los datos en formato `.pcap` para su posterior análisis.

### 🔹 Análisis de capturas
Permite explorar capturas almacenadas previamente. Próximamente se integrará con herramientas como `Wireshark` o `TShark` para un análisis más detallado (actualmente solo muestra contenido con `cat`).

### 🔹 Chatbot IA local
Asistente basado en IA que se ejecuta directamente en la máquina utilizando el modelo [Mistral](https://mistral.ai/). Permite interacción desde la terminal de forma privada y sin depender de servidores externos.

### 🔹 Cracker de hashes
Permite romper hashes `MD5`, `SHA1` y `SHA256` mediante ataque de diccionario. El usuario puede elegir el diccionario a usar y añadir los suyos propios.

### 🔹 Análisis de archivos con VirusTotal *(en pruebas)*
Consulta archivos mediante la API pública de VirusTotal. Esta funcionalidad todavía no está finalizada y puede no funcionar correctamente en su estado actual.

---

## 📁 Estructura del proyecto

```bash
snoopkid/
├── snoopkid.py               # Menú principal
├── requirements.txt          # Dependencias del proyecto
├── utils/                    # Configuración y rutas comunes
├── modules/                  # Módulos individuales del toolkit
├── chat/                     # Módulo de chatbot IA
├── capturas/                 # Directorio donde se guardan archivos generados
│   ├── sniffer/              # Capturas de red (.pcap)
│   ├── chat/                 # Conversaciones con el chatbot
│   └── virustotal/           # Resultados de análisis (texto)
└── ...
```

---

## 💻 Ejecución

Para iniciar Snoopkid, navega a la carpeta raíz del proyecto y ejecuta:

```bash
python3 snoopkid.py
```

Desde ahí accederás a un menú donde podrás seleccionar los módulos disponibles.

> ☑️ Es posible que necesites permisos de superusuario (`sudo`) para ejecutar algunas funciones como el sniffer.

---

## 🧠 Requisitos

### 🔧 Generales

- Python 3.10 o superior
- Sistema basado en Unix (desarrollado en Kali Linux)
- Acceso root para funciones específicas

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

### 🤖 Requisitos del módulo IA

- Tener descargado localmente un modelo como **Mistral** compatible con `llama-cpp-python` o similar
- Configurar la ruta al modelo en `utils/config.py`
- Requiere entorno capaz de ejecutar modelos de lenguaje en local

---

## 📈 Estado del desarrollo

Actualmente se están desarrollando y corrigiendo los siguientes puntos:

- Integración del visor de capturas con `tshark`
- Estabilización del módulo de análisis con VirusTotal
- Instalador automático para facilitar el uso a usuarios sin formación técnica, permitiendo una instalación sencilla y guiada.
- Mejora progresiva de la interacción del chatbot
- Implementación de nuevos módulos futuros

---

## 🔮 Próximas funcionalidades previstas

- Generador de payloads personalizados
- Plugin system para añadir módulos externos
- Refuerzo del control de errores
- Interfaz más intuitiva para terminal
- Consolidación de logs y registros por módulo

---

## 📧 Autor

Desarrollado por **Natxo** como parte de un proyecto formativo.
