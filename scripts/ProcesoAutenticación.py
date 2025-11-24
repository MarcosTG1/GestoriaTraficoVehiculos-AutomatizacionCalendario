import os
import sys

# Añadimos el directorio 'src' al path para poder importar los módulos correctamente
# si ejecutamos el script desde la raíz del proyecto.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.ManejoGoogleCalendar import get_calendar_service, list_upcoming_events

def ProcesoAutenticacion():
    """
    Función principal que ejecuta el flujo de autenticación.
    """
    print("--- Iniciando proceso de autenticación con Google Calendar ---")
    print("Este script intentará conectar con la API de Google Calendar.")
    print("Si es la primera vez, se abrirá una ventana en tu navegador para que autorices la aplicación.")
    
    try:
        # Intentamos obtener el servicio de calendario.
        # Esta función (get_calendar_service) maneja toda la lógica de OAuth2:
        # 1. Busca el archivo 'secrets/token.json'. Si existe y es válido, lo usa.
        # 2. Si no existe o expiró, busca 'secrets/credentials.json' e inicia el flujo de login en el navegador.
        # 3. Guarda el nuevo token en 'secrets/token.json' para futuras ejecuciones.
        service = get_calendar_service()
        
        if service:
            print("\n¡Autenticación exitosa!")
            print("El archivo 'secrets/token.json' ha sido generado/verificado correctamente.")
            print("Ahora puedes usar este token para ejecutar scripts sin necesidad de loguearte manualmente de nuevo.")
            
            print("\n--- Verificación de funcionamiento ---")
            print("Listando los próximos 5 eventos de tu calendario principal para confirmar acceso:")
            # Llamamos a una función de prueba para ver si realmente tenemos acceso a los datos.
            list_upcoming_events(service, max_results=5)
        else:
            print("\n[ERROR] No se pudo obtener el servicio de Google Calendar.")
            print("Verifique que 'secrets/credentials.json' existe y es correcto.")
            
    except FileNotFoundError as fnf_error:
        print(f"\n[ERROR CRÍTICO] Archivo no encontrado: {fnf_error}")
        print("Asegúrate de haber descargado el archivo 'credentials.json' desde Google Cloud Console")
        print("y haberlo guardado en la carpeta 'secrets/' de este proyecto.")
    except Exception as e:
        print(f"\n[ERROR INESPERADO] Ocurrió un error durante la autenticación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ProcesoAutenticacion()
