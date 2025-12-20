import pandas as pd
from datetime import timedelta, datetime
import sys
import os
import time
from typing import Callable, Optional

# Añadir el directorio raíz al path para poder importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.ManejoGoogleCalendar import get_calendar_service, add_event

def RevisarAntiguedadFechaCreacion(fecha_creacion: datetime, dias_ajuste: int) -> tuple[datetime, int]:
    """
    Verifica si la fecha de creación es antigua (más de 50 días) y la ajusta si es necesario.
    """
    fecha_hoy = datetime.now()
    fecha_limite = fecha_hoy - timedelta(days=50)  
    
    if fecha_creacion < fecha_limite:
        # Ajustar la fecha: hoy - dias_ajuste
        fecha_ajustada = fecha_hoy - timedelta(days=dias_ajuste)
        print(f"[AJUSTE] Fecha antigua detectada ({fecha_creacion.strftime('%Y-%m-%d')}). Nueva fecha: {fecha_ajustada.strftime('%Y-%m-%d')}")
        return fecha_ajustada, dias_ajuste + 1
    
    return fecha_creacion, dias_ajuste

def ProcesarEventosGenerico(
    nombre_proceso: str,
    ruta_archivo: str,
    procesar_fila: Callable[[pd.Series, int], Optional[dict]],
    es_csv: bool = True,
    validar_nombre_archivo: Optional[str] = None
):
    """
    Función genérica para procesar archivos y crear eventos en el calendario.
    
    Args:
        nombre_proceso: Nombre para logs (ej: "JUSTIFICANTES").
        ruta_archivo: Ruta al archivo de datos.
        procesar_fila: Función que recibe (row, dias_ajuste) y devuelve un dict con datos del evento o None.
                       El dict debe tener: 'summary', 'start_time', 'end_time', 'description', 'recurrence', 'nuevo_dias_ajuste'.
        es_csv: Si es True lee CSV directamente, si es False asume XLS y convierte.
        validar_nombre_archivo: Si no es None, valida que el archivo tenga este nombre exacto.
    """
    print(f"--- Iniciando proceso de actualización de calendario ({nombre_proceso}) ---")
    
    service = get_calendar_service()
    if not service:
        print("[ERROR] No se pudo conectar con Google Calendar.")
        return

    # Validación de nombre (específico para Facturas)
    if validar_nombre_archivo:
        nombre_real = os.path.basename(ruta_archivo)
        if nombre_real != validar_nombre_archivo:
            print(f"[ERROR CRÍTICO] El archivo no tiene el nombre correcto.")
            print(f"Esperado: {validar_nombre_archivo}")
            print(f"Encontrado: {nombre_real}")
            print("Deteniendo ejecución.")
            sys.exit(1)

    try:
        df = None
        if es_csv:
            df = pd.read_csv(ruta_archivo, sep=',')
            print(f"Archivo cargado correctamente: {ruta_archivo}")
        else:
            # Caso Facturas (XLS -> CSV)
            from services.ConversorArchivos import convertir_xls_a_csv
            ruta_csv = convertir_xls_a_csv(ruta_archivo)
            if not ruta_csv:
                print("[ERROR] Falló la conversión de XLS a CSV.")
                return
            # Facturas usa dayfirst=True
            df = pd.read_csv(ruta_csv, sep=',')
            print(f"Archivo CSV cargado correctamente: {ruta_csv}")
            
        print(f"Registros encontrados: {len(df)}")
        
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo en: {ruta_archivo}")
        return
    except Exception as e:
        print(f"[ERROR] Al procesar el archivo: {e}")
        return

    count_ok = 0
    count_err = 0
    dias_ajuste = 0
    
    for index, row in df.iterrows():
        try:
            datos_evento = procesar_fila(row, dias_ajuste)
            
            if datos_evento:
                dias_ajuste = datos_evento['nuevo_dias_ajuste']
                
                print(f"Procesando {nombre_proceso}: {datos_evento['summary']} inicio {datos_evento['start_time']}")
                if 'recurrence' in datos_evento:
                     print(f"(Recurrencia: {datos_evento['recurrence']})")

                add_event(
                    service, 
                    datos_evento['summary'], 
                    datos_evento['start_time'], 
                    datos_evento['end_time'], 
                    description=datos_evento['description'], 
                    recurrence=datos_evento.get('recurrence')
                )
                count_ok += 1
                
                # Pausa para evitar Rate Limit Exceeded
                time.sleep(0.5)
            
        except Exception as e:
            print(f"[ERROR] Fallo en fila {index}: {e}")
            count_err += 1

    print(f"\n--- Resumen {nombre_proceso} ---")
    print(f"Eventos creados: {count_ok}")
    print(f"Errores: {count_err}")


def AnadirEventosCalendarioJustificantes():
    from src.config import PATH_JUSTIFICANTES, DIAS_RECURRENCIA_JUSTIFICANTE, VECES_REPETICION_JUSTIFICANTE
    
    def procesar(row, dias_ajuste):
        bastidor = row['BASTIDOR']
        fecha_creacion_str = row['FECHA DE CREACIÓN']
        fecha_creacion = pd.to_datetime(fecha_creacion_str)
        
        fecha_creacion, nuevo_dias_ajuste = RevisarAntiguedadFechaCreacion(fecha_creacion, dias_ajuste)
        
        return {
            'summary': f"Justificante: {bastidor}",
            'start_time': fecha_creacion.isoformat(),
            'end_time': (fecha_creacion + timedelta(hours=1)).isoformat(),
            'description': f"Evento recurrente generado automáticamente.\nBastidor: {bastidor}\nFecha Creación Original: {fecha_creacion_str}",
            'recurrence': [f"RRULE:FREQ=DAILY;INTERVAL={DIAS_RECURRENCIA_JUSTIFICANTE};COUNT={VECES_REPETICION_JUSTIFICANTE}"],
            'nuevo_dias_ajuste': nuevo_dias_ajuste
        }

    ProcesarEventosGenerico("JUSTIFICANTES", PATH_JUSTIFICANTES, procesar)

def AnadirEventosCalendarioIncidencias():
    from src.config import PATH_INCIDENCIAS, DIAS_RECURRENCIA_INCIDENCIA, VECES_REPETICION_INCIDENCIA
    
    def procesar(row, dias_ajuste):
        bastidor = row['BASTIDOR']
        fecha_creacion_str = row['FECHA DE CREACIÓN']
        fecha_creacion = pd.to_datetime(fecha_creacion_str)
        
        fecha_creacion, nuevo_dias_ajuste = RevisarAntiguedadFechaCreacion(fecha_creacion, dias_ajuste)
        
        return {
            'summary': f"Estado de incidencia : {bastidor}",
            'start_time': fecha_creacion.isoformat(),
            'end_time': (fecha_creacion + timedelta(hours=1)).isoformat(),
            'description': f"Evento recurrente generado automáticamente.\nBastidor: {bastidor}\nFecha Creación Original: {fecha_creacion_str}",
            'recurrence': [f"RRULE:FREQ=DAILY;INTERVAL={DIAS_RECURRENCIA_INCIDENCIA};COUNT={VECES_REPETICION_INCIDENCIA}"],
            'nuevo_dias_ajuste': nuevo_dias_ajuste
        }

    ProcesarEventosGenerico("INCIDENCIAS", PATH_INCIDENCIAS, procesar)

def AnadirEventosCalendarioTrafico():
    from src.config import PATH_TRAFICO, DIAS_RECURRENCIA_TRAFICO, VECES_REPETICION_TRAFICO
    
    def procesar(row, dias_ajuste):
        bastidor = row['BASTIDOR']
        fecha_creacion_str = row['FECHA DE CREACIÓN']
        fecha_creacion = pd.to_datetime(fecha_creacion_str)
        
        fecha_creacion, nuevo_dias_ajuste = RevisarAntiguedadFechaCreacion(fecha_creacion, dias_ajuste)
        
        return {
            'summary': f"Rechazado por Tráfico : {bastidor}",
            'start_time': fecha_creacion.isoformat(),
            'end_time': (fecha_creacion + timedelta(hours=1)).isoformat(),
            'description': f"Evento recurrente generado automáticamente.\nBastidor: {bastidor}\nFecha Creación Original: {fecha_creacion_str}",
            'recurrence': [f"RRULE:FREQ=DAILY;INTERVAL={DIAS_RECURRENCIA_TRAFICO};COUNT={VECES_REPETICION_TRAFICO}"],
            'nuevo_dias_ajuste': nuevo_dias_ajuste
        }

    ProcesarEventosGenerico("TRÁFICO", PATH_TRAFICO, procesar)

def AnadirEventosCalendarioFacturas():
    from src.config import PATH_FACTURAS, DIAS_RECURRENCIA_FACTURAS, VECES_REPETICION_FACTURAS
    
    def procesar(row, dias_ajuste):
        identificador = row['Identificador']
        fecha_factura_str = row['Fecha factura']
        razon_social = row['Primer apellido/Razón social']
        expediente = row['Expediente']
        descrip_expediente = row['Descrip. Expediente']
        
        # dayfirst=True es manejado implícitamente por pandas si el formato es ambiguo, pero aquí lo forzamos en la conversión previa o asumimos formato correcto
        # En la versión anterior se usaba dayfirst=True en read_csv, pero read_csv no tiene ese parametro, es to_datetime.
        # Corrección: read_csv lee strings. to_datetime es quien necesita dayfirst.
        fecha_factura = pd.to_datetime(fecha_factura_str, dayfirst=True)
        
        fecha_evento, nuevo_dias_ajuste = RevisarAntiguedadFechaCreacion(fecha_factura, dias_ajuste)
        
        return {
            'summary': f"Factura pendiente: {identificador} - {razon_social}",
            'start_time': fecha_evento.isoformat(),
            'end_time': (fecha_evento + timedelta(hours=1)).isoformat(),
            'description': f"Evento generado automáticamente.\nExpediente: {expediente}\nDescripción: {descrip_expediente}\nFecha Factura Original: {fecha_factura_str}",
            'recurrence': [f"RRULE:FREQ=DAILY;INTERVAL={DIAS_RECURRENCIA_FACTURAS};COUNT={VECES_REPETICION_FACTURAS}"],
            'nuevo_dias_ajuste': nuevo_dias_ajuste
        }

    ProcesarEventosGenerico(
        "FACTURAS PENDIENTES", 
        PATH_FACTURAS, 
        procesar, 
        es_csv=False, 
        validar_nombre_archivo="LISTADO_FACTURAS.xls"
    )