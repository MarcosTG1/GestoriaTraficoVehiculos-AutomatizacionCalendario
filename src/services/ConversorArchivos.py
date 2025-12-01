import pandas as pd
import os
import sys
from pathlib import Path

def convertir_xls_a_csv(ruta_entrada: str, ruta_salida: str = None) -> str:
    """
    Convierte un archivo .xls a .csv.
    
    Args:
        ruta_entrada (str): Ruta al archivo .xls
        ruta_salida (str, optional): Ruta donde guardar el .csv. 
                                     Si no se especifica, usa el mismo nombre que el archivo de entrada.
    
    Returns:
        str: Ruta del archivo .csv generado.
    """
    try:
        # Verificar que el archivo de entrada existe
        if not os.path.exists(ruta_entrada):
            raise FileNotFoundError(f"El archivo no existe: {ruta_entrada}")
            
        # Verificar extensión
        if not ruta_entrada.lower().endswith('.xls'):
            print(f"Advertencia: El archivo {ruta_entrada} no tiene extensión .xls, intentando convertir de todas formas...")

        # Definir ruta de salida si no se proporciona
        if ruta_salida is None:
            path_entrada = Path(ruta_entrada)
            ruta_salida = str(path_entrada.with_suffix('.csv'))

        print(f"Convirtiendo '{ruta_entrada}' a CSV...")
        
        # Leer el archivo Excel buscando la cabecera correcta
        # Primero leemos unas pocas filas para encontrar dónde empiezan los datos
        df_temp = pd.read_excel(ruta_entrada, engine='xlrd', header=None, nrows=20)
        
        fila_header = 0
        encontrado = False
        for i, row in df_temp.iterrows():
            # Buscamos una fila que contenga "Identificador" o "Fecha factura"
            # Convertimos a string por si acaso hay datos numéricos
            fila_str = row.astype(str).str.cat(sep=' ')
            if "Identificador" in fila_str and "Fecha factura" in fila_str:
                fila_header = i
                encontrado = True
                break
        
        if encontrado:
            print(f"Cabecera detectada en la fila {fila_header + 1}")
        else:
            print("No se detectó cabecera conocida, usando la primera fila.")

        # Leer el archivo completo saltando las filas innecesarias
        df = pd.read_excel(ruta_entrada, engine='xlrd', header=fila_header)
        
        # Guardar como CSV
        df.to_csv(ruta_salida, index=False, encoding='utf-8-sig', sep=',')
        
        print(f"Conversión exitosa. Archivo guardado en: {ruta_salida}")
        return ruta_salida

    except Exception as e:
        print(f"Error durante la conversión: {e}")
        return None

if __name__ == "__main__":
    # Uso desde línea de comandos: python src/services/ConversorArchivos.py archivo.xls [salida.csv]
    if len(sys.argv) < 2:
        # Para pruebas rápidas si no se pasan argumentos, se puede descomentar la línea de abajo o usar argumentos
        # convertir_xls_a_csv("ruta/a/tu/archivo.xls")
        print("Uso: python src/services/ConversorArchivos.py <archivo_entrada.xls> [archivo_salida.csv]")
    else:
        entrada = sys.argv[1]
        salida = sys.argv[2] if len(sys.argv) > 2 else None
        convertir_xls_a_csv(entrada, salida)