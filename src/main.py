from pathlib import Path
import pandas as pd
import re

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

def parse_line(line, file_name=None, line_num=None):
    try:
        if len(line) < 120:
            print(f"[{file_name} | línea {line_num}] Línea muy corta ({len(line)}): {line.strip()}")
            return None

        match = re.search(r"\d{15}", line[74:])
        if match:
            pos_importe = 74 + match.start()
        else:
            print(f"[{file_name} | línea {line_num}] No se encontró importe: {line.strip()}")
            return None

        nombre = line[74:pos_importe].strip()
        nombre = re.sub(r'^\d+', '', nombre)

        d = {
            "fecha_emision": line[0:8],
            "tipo_comprobante": line[8:11],
            "pto_venta": line[11:16],
            "nro_comprobante": line[16:36].lstrip("0"),
            "cuit_receptor": line[62:74].lstrip("0"),
            "denominacion": nombre,
            # Ahora el importe queda entero, sin decimales
            "importe_total": int(float(line[pos_importe:pos_importe+15]) / 100),
            "archivo_origen": file_name
        }
        return d
    except Exception as e:
        print(f"[{file_name} | línea {line_num}] ERROR: {e} - {line.strip()}")
        return None
