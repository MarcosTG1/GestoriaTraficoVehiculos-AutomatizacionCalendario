import sys
import os
import datetime

# Añadir el directorio raíz al path para poder importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.ManejoGoogleCalendar import get_calendar_service, delete_event

def BorrarEventos():
    print("--- Iniciando proceso de ELIMINACIÓN de eventos (Año Actual y Anterior) ---")
    
    service = get_calendar_service()
    if not service:
        print("[ERROR] No se pudo conectar con Google Calendar.")
        return

    # Obtener fecha actual
    now = datetime.datetime.utcnow()
    current_year = now.year
    previous_year = current_year - 1
    
    # Calcular rango: Desde 1 Enero del año anterior hasta 31 Diciembre del año siguiente 
    start_date = datetime.datetime(previous_year, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(current_year + 1, 12, 31, 0, 0, 0)
    
    time_min = start_date.isoformat() + "Z"
    time_max = end_date.isoformat() + "Z"
    
    print(f"Buscando eventos desde {previous_year} hasta {end_date}...")
    print(f"Rango: {start_date.date()} -> {end_date.date()}")
    
    # Listar eventos 
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            maxResults=5000, 
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No se encontraron eventos para eliminar en este rango.")
        return

    print(f"Se han encontrado {len(events)} eventos.")
    confirm = input("¿Estás SEGURO de que quieres eliminarlos TODOS? (escribe 'si' para confirmar): ")
    
    if confirm.lower() != 'si':
        print("Operación cancelada.")
        return

    count_deleted = 0
    count_err = 0

    for event in events:
        try:
            event_id = event['id']
            summary = event.get('summary', 'Sin título')
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            print(f"Eliminando: {summary} ({start})")
            delete_event(service, event_id)
            count_deleted += 1
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el evento {event_id}: {e}")
            count_err += 1

    print("\n--- Resumen de Eliminación ---")
    print(f"Eventos eliminados: {count_deleted}")
    print(f"Errores: {count_err}")

if __name__ == "__main__":
    BorrarEventos()
