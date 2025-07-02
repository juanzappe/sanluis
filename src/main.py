from pathlib import Path
import pandas as pd

def unificar_ventas_excel_a_csv(directorio_entrada, patron_archivos, archivo_salida):
    """
    Une todos los archivos Excel en 'directorio_entrada' que cumplen el patrón 'patron_archivos'
    en un único archivo CSV llamado 'archivo_salida', unificando columnas y eliminando duplicados.
    """
    directorio_entrada = Path(directorio_entrada)
    archivos = sorted(directorio_entrada.glob(patron_archivos))
    es_primer_archivo = True
    columnas_base = None
    lista_df = []

    for archivo in archivos:
        print(f"Leyendo: {archivo.name}")
        df = pd.read_excel(archivo)
        if es_primer_archivo:
            columnas_base = df.columns
            es_primer_archivo = False
        else:
            # Forzar el mismo orden de columnas
            df = df[columnas_base]
        lista_df.append(df)
    
    # Concatenar todos los DataFrames
    df_unificado = pd.concat(lista_df, ignore_index=True)
    
    # Eliminar duplicados (ajustá la clave según tu archivo, acá usamos 'idVenta')
    df_unificado = df_unificado.drop_duplicates(subset=['idVenta'])

    # Guardar el CSV final
    Path(archivo_salida).parent.mkdir(exist_ok=True)
    df_unificado.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    print(f"Archivo CSV final guardado en: {archivo_salida}")
