import os

def BorrarDatosEjecucion(ruta_archivo: str):
    try:
        os.remove(ruta_archivo)
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no existe.")
    except Exception as e:
        print(f"Error al borrar el archivo {ruta_archivo}: {e}")
    except PermissionError:
        print(f"No se puede borrar el archivo {ruta_archivo} porque está en uso.")
