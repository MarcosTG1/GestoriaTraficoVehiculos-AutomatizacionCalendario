import pandas as pd
from datetime import timedelta
import sys
import os

# Añadir el directorio raíz al path para poder importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.ManejoGoogleCalendar import get_calendar_service, add_event

def AnadirEventosCalendarioJustificantes():
    from src.config import PATH_JUSTIFICANTES, DIAS_RECURRENCIA_JUSTIFICANTE, VECES_REPETICION_JUSTIFICANTE
    print("--- Iniciando proceso de actualización de calendario (JUSTIFICANTES RECURRENTES) ---")
    
    service = get_calendar_service()
    if not service:
        print("[ERROR] No se pudo conectar con Google Calendar.")
        return

    try:
        df = pd.read_csv(PATH_JUSTIFICANTES, sep=',')
        print(f"Archivo cargado correctamente: {PATH_JUSTIFICANTES}")
        print(f"Registros encontrados: {len(df)}")
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo CSV en: {PATH_JUSTIFICANTES}")
        return
    except Exception as e:
        print(f"[ERROR] Al leer el CSV: {e}")
        return

    count_ok = 0
    count_err = 0

    for index, row in df.iterrows():
        try:
            bastidor = row['BASTIDOR']
            fecha_creacion_str = row['FECHA DE CREACIÓN']
            
            # Convertir string a datetime
            fecha_creacion = pd.to_datetime(fecha_creacion_str)
            
            # El primer evento es en la fecha de creación
            start_time = fecha_creacion.isoformat()
            end_time = (fecha_creacion + timedelta(hours=1)).isoformat()
            
            summary = f"Justificante: {bastidor}"
            description = f"Evento recurrente generado automáticamente.\nBastidor: {bastidor}\nFecha Creación Original: {fecha_creacion_str}"
            
            # Configurar recurrencia: Cada 28 días, 3 veces en total
            recurrence = [f"RRULE:FREQ=DAILY;INTERVAL={DIAS_RECURRENCIA_JUSTIFICANTE};COUNT={VECES_REPETICION_JUSTIFICANTE}"]
            
            print(f"Procesando Justificante: {summary} inicio {start_time} (Recurrencia: {recurrence})")
            
            add_event(service, summary, start_time, end_time, description=description, recurrence=recurrence)
            count_ok += 1
            
        except Exception as e:
            print(f"[ERROR] Fallo en fila {index}: {e}")
            count_err += 1

    print("\n--- Resumen Justificantes ---")
    print(f"Eventos recurrentes creados: {count_ok}")
    print(f"Errores: {count_err}")

def AnadirEventosCalendarioIncidencias():
    from src.config import PATH_INCIDENCIAS, DIAS_RECURRENCIA_INCIDENCIA, VECES_REPETICION_INCIDENCIA
    
    print("--- Iniciando proceso de actualización de calendario (INCIDENCIAS) ---")
    
    service = get_calendar_service()
    if not service:
        print("[ERROR] No se pudo conectar con Google Calendar.")
        return

    try:
        df = pd.read_csv(PATH_INCIDENCIAS, sep=',')
        print(f"Archivo cargado correctamente: {PATH_INCIDENCIAS}")
        print(f"Registros encontrados: {len(df)}")
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo CSV en: {PATH_INCIDENCIAS}")
        return
    except Exception as e:
        print(f"[ERROR] Al leer el CSV: {e}")
        return

    count_ok = 0
    count_err = 0

    for index, row in df.iterrows():
        try:
            bastidor = row['BASTIDOR']
            fecha_creacion_str = row['FECHA DE CREACIÓN']
            
            # Convertir string a datetime
            fecha_creacion = pd.to_datetime(fecha_creacion_str)
            
            # El evento comienza en la fecha de creación
            start_time = fecha_creacion.isoformat()
            end_time = (fecha_creacion + timedelta(hours=1)).isoformat()
            
            summary = f"Estado de incidencia : {bastidor}"
            description = f"Evento recurrente generado automáticamente.\nBastidor: {bastidor}\nFecha Creación Original: {fecha_creacion_str}"
            
            # Configurar recurrencia: Cada 15 días, 6 veces en total
            # RRULE:FREQ=DAILY;INTERVAL=15;COUNT=6
            recurrence = [f"RRULE:FREQ=DAILY;INTERVAL={DIAS_RECURRENCIA_INCIDENCIA};COUNT={VECES_REPETICION_INCIDENCIA}"]
            
            print(f"Procesando Incidencia: {summary} inicio {start_time} (Recurrencia: {recurrence})")
            
            add_event(service, summary, start_time, end_time, description=description, recurrence=recurrence)
        except Exception as e:
            print(f"[ERROR] Fallo en fila {index}: {e}")
            count_err += 1

    print("\n--- Resumen Incidencias ---")
    print(f"Eventos recurrentes creados: {count_ok}")
    print(f"Errores: {count_err}")

def AnadirEventosCalendarioTrafico():
    from src.config import PATH_TRAFICO, DIAS_RECURRENCIA_TRAFICO, VECES_REPETICION_TRAFICO
    
    print("--- Iniciando proceso de actualización de calendario (TRÁFICO) ---")
    
    service = get_calendar_service()
    if not service:
        print("[ERROR] No se pudo conectar con Google Calendar.")
        return

    try:
        df = pd.read_csv(PATH_TRAFICO, sep=',')
        print(f"Archivo cargado correctamente: {PATH_TRAFICO}")
        print(f"Registros encontrados: {len(df)}")
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo CSV en: {PATH_TRAFICO}")
        return
    except Exception as e:
        print(f"[ERROR] Al leer el CSV: {e}")
        return

    count_ok = 0
    count_err = 0

    for index, row in df.iterrows():
        try:
            bastidor = row['BASTIDOR']
            fecha_creacion_str = row['FECHA DE CREACIÓN']
            
            # Convertir string a datetime
            fecha_creacion = pd.to_datetime(fecha_creacion_str)
            
            # El evento comienza en la fecha de creación
            start_time = fecha_creacion.isoformat()
            end_time = (fecha_creacion + timedelta(hours=1)).isoformat()
            
            summary = f"Rechazado por Tráfico : {bastidor}"
            description = f"Evento recurrente generado automáticamente.\nBastidor: {bastidor}\nFecha Creación Original: {fecha_creacion_str}"
            
            # Configurar recurrencia
            recurrence = [f"RRULE:FREQ=DAILY;INTERVAL={DIAS_RECURRENCIA_TRAFICO};COUNT={VECES_REPETICION_TRAFICO}"]
            
            print(f"Procesando Tráfico: {summary} inicio {start_time} (Recurrencia: {recurrence})")
            
            add_event(service, summary, start_time, end_time, description=description, recurrence=recurrence)
            count_ok += 1
            
        except Exception as e:
            print(f"[ERROR] Fallo en fila {index}: {e}")
            count_err += 1

    print("\n--- Resumen Tráfico ---")
    print(f"Eventos recurrentes creados: {count_ok}")
    print(f"Errores: {count_err}")