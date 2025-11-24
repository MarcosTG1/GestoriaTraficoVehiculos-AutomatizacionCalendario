import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- Rutas Base ---
# Detectamos la raíz del proyecto (asumiendo que este archivo está en src/config.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Helper para obtener variables obligatorias
def get_required_env(key):
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"ERROR CRÍTICO: La variable '{key}' NO está definida en el archivo .env. Es obligatoria.")
    return value

# --- Configuración de Google Calendar ---
# Usamos los nombres definidos en .env.example para consistencia
GOOGLE_CREDENTIALS_PATH = get_required_env("GOOGLE_CREDENTIALS_PATH")
GOOGLE_TOKEN_PATH = get_required_env("GOOGLE_TOKEN_PATH")
CALENDAR_ID = get_required_env("CALENDAR_ID")

# --- Rutas de Datos ---
PATH_INCIDENCIAS = get_required_env("PATH_INCIDENCIAS")
PATH_JUSTIFICANTES = get_required_env("PATH_JUSTIFICANTES")
PATH_TRAFICO = get_required_env("PATH_TRAFICO")


# --- Lógica de Negocio ---
# Convertimos a int para que sean utilizables numéricamente

def get_int_required_env(key):
    value = get_required_env(key)
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"ERROR CRÍTICO: La variable '{key}' debe ser un número entero. Valor actual: '{value}'")

DIAS_RECURRENCIA_INCIDENCIA = get_int_required_env("DIAS_RECURRENCIA_INCIDENCIA")
VECES_REPETICION_INCIDENCIA = get_int_required_env("VECES_REPETICION_INCIDENCIA")

DIAS_RECURRENCIA_TRAFICO = get_int_required_env("DIAS_RECURRENCIA_TRAFICO")
VECES_REPETICION_TRAFICO = get_int_required_env("VECES_REPETICION_TRAFICO")

DIAS_RECURRENCIA_JUSTIFICANTE = get_int_required_env("DIAS_RECURRENCIA_JUSTIFICANTE")
VECES_REPETICION_JUSTIFICANTE = get_int_required_env("VECES_REPETICION_JUSTIFICANTE")