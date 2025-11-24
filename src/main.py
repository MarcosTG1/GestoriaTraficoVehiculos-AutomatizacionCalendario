import sys
import os

# Añadir el directorio raíz al path para poder importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.ManejoDeEventos import AnadirEventosCalendarioJustificantes, AnadirEventosCalendarioIncidencias, AnadirEventosCalendarioTrafico
from scripts.ProcesoAutenticación import ProcesoAutenticacion
from scripts.BorrarEventos import BorrarEventos

def main():
    print("=== INICIANDO SISTEMA DE ACTUALIZACIÓN DE CALENDARIO ===")

    ProcesoAutenticacion()

    print("\n[0/3] Borrando eventos...")
    BorrarEventos()
    
    print("\n[1/3] Procesando Justificantes...")
    AnadirEventosCalendarioJustificantes()
    
    print("\n[2/3] Procesando Incidencias...")
    AnadirEventosCalendarioIncidencias()

    print("\n[3/3] Procesando Tráfico...")
    AnadirEventosCalendarioTrafico()
    
    print("\n=== PROCESO COMPLETADO ===")

if __name__ == "__main__":
    main()
