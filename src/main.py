from pathlib import Path
import pandas as pd
import re
import numpy as np




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


def unir_ventas(ARCHIVO_MOSTRADOR_FINAL_PATH,ARCHIVO_SERVICIOS_FINAL_PATH,ARCHIVO_UNIFICADO_PATH):
    """
    Une las ventas de facturación (servicio) y mostrador en un solo dataset.
    Exporta el resultado a CSV en ARCHIVO_UNIFICADO_PATH.
    """

    # Dataset de resto de las ventas
    df_servicios = pd.read_csv(ARCHIVO_SERVICIOS_FINAL_PATH)

    # Dataset del mostrador
    df_mostrador = pd.read_csv(ARCHIVO_MOSTRADOR_FINAL_PATH)

    # Seleccionamos columnas y renombramos
    df_servicios_simple = df_servicios[['fecha_emision', 'denominacion', 'TotalVenta_Ajustado',
                                'cuit_receptor', 'Anio', 'Mes', 'importe_total']].rename(columns={
        'fecha_emision': 'fecha',
        'denominacion': 'cliente',
        'TotalVenta_Ajustado': 'monto ajustado',
        'cuit_receptor': 'cuit',
        'Anio': 'anio',
        'Mes': 'mes',
        'importe_total': 'monto'
    })

    df_mostrador_simple = df_mostrador[['Fecha', 'Cliente', 'TotalVenta_Ajustado',
                                        'Producto', 'CUIT', 'Anio', 'Mes', 'TotalVenta']].rename(columns={
        'Fecha': 'fecha',
        'Cliente': 'cliente',
        'TotalVenta_Ajustado': 'monto ajustado',
        'Producto': 'producto',
        'CUIT': 'cuit',
        'Anio': 'anio',
        'Mes': 'mes',
        'TotalVenta': 'monto'
    })

    # Asignamos origen 'servicio' a facturación
    df_servicios_simple['origen'] = 'servicio'

    # Listas de productos
    decoracion_items = [
        'ALMOHADON', 'APOYA CUCHARA', 'AZUCARERA', 'BANCO TRES PATAS', 'BANCO RECTANGULAR',
        'COLGANTES DE CERAMICA', 'COLGANTES VARIOS', 'CORAZON CHICO', 'CORAZON GRANDE', 'CORAZON MEDIANO',
        'CUENCO CHICO', 'CUENCO MEDIANO', 'CUENCO MINI', 'CUENCO GRANDE', 'JARRA', 'JARRITO/ MATE/ VASITO',
        'JARRO', 'LECHERITA', 'MACETA CHICA', 'MACETA MEDIANA', 'PINGUINO LITRO', 'PINGUINO MEDIO LITRO',
        'PLATO 24CM', 'PLATO 30CM', 'PLATO POSTRE', 'PORTA CUCHARA GRANDE', 'PORTA VELA', 'POSE TORTA',
        'REGALERÍA', 'REGALERIA VARIOS', 'TAZA SOLA', 'TAZA SOLA ARTESANAL', 'TAZON ARTESANAL',
        'TAZON PARA LANA', 'TELAS', 'TETERA', 'VELA', 'velas', 'TASA CON PLATO MOLDE', 'TAZA CON PLATO ARTESANAL'
    ]
    decoracion_items = [item.lower() for item in decoracion_items]
    restobar_items = ['RESTOBAR', 'restovar','CONFITERIA']
    restobar_items = [item.lower() for item in restobar_items]

    # Función auxiliar
    def clasificar_origen(producto):
        producto_lower = str(producto).lower()
        if any(item in producto_lower for item in decoracion_items):
            return 'decoracion'
        elif any(item in producto_lower for item in restobar_items):
            return 'restobar'
        else:
            return 'mostrador'

    # Clasificar origen en mostrador
    df_mostrador_simple['origen'] = df_mostrador_simple['producto'].apply(clasificar_origen)

    # Concatenar
    df_unido = pd.concat([df_servicios_simple, df_mostrador_simple], ignore_index=True)

    # Ajustar fecha
    df_unido['fecha'] = df_unido['fecha'].astype(str).str.split().str[0]
    
    df_unido['producto'] = df_unido['producto'].fillna('No aplica')

    # Exportar CSV
    df_unido.to_csv(ARCHIVO_UNIFICADO_PATH, index=False)

    print(f"✅ Archivo unificado exportado en: {ARCHIVO_UNIFICADO_PATH}")
    return df_unido


# === FUNCIÓN PRINCIPAL ===
def unificar_ingresos_csv(DATA_PATH, PATRON_INGRESOS_PATH, INGRESOS_SALIDA_PATH):
    """
    Une todos los archivos CSV dentro de 'directorio_entrada' que cumplan con 'patron_archivos'
    en un único archivo CSV final 'archivo_salida'.

    - Busca archivos usando .glob()
    - Lee y concatena todos los CSV
    - Limpia encabezados
    - Elimina duplicados si existe una columna identificadora
    - Ordena por fecha si existe 'Fecha de Emisión'
    """

    print("🚀 Iniciando proceso de unificación de ingresos ARCA...\n")

    archivos = sorted(DATA_PATH.glob(PATRON_INGRESOS_PATH))

    if not archivos:
        print(f"❌ No se encontraron archivos que coincidan con el patrón: {PATRON_INGRESOS_PATH}")
        return None

    lista_df = []

    for archivo in archivos:
        print(f"📄 Leyendo: {archivo.name}")
        df = pd.read_csv(archivo, sep=";", quotechar='"', encoding="latin1", low_memory=False)
        df["Origen"] = archivo.stem
        lista_df.append(df)

    # Unificar todo
    df_unificado = pd.concat(lista_df, ignore_index=True)

    # Limpieza de nombres de columnas
    df_unificado.columns = (
        df_unificado.columns
        .astype(str)
        .str.strip()
        .str.replace('"', '', regex=False)
    )

    # Ordenar por fecha si existe
    if "Fecha de Emisión" in df_unificado.columns:
        df_unificado["Fecha de Emisión"] = pd.to_datetime(df_unificado["Fecha de Emisión"], errors="coerce")
        df_unificado = df_unificado.sort_values("Fecha de Emisión")

    # Eliminar duplicados si hay identificadores posibles
    posibles_ids = ["Número Desde", "Número Hasta", "Cód. Autorización"]
    for col in posibles_ids:
        if col in df_unificado.columns:
            df_unificado = df_unificado.drop_duplicates(subset=[col])
            break

    # Crear carpeta de salida si no existe
    INGRESOS_SALIDA_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Guardar CSV final
    df_unificado.to_csv(INGRESOS_SALIDA_PATH, index=False, sep=";", encoding="utf-8-sig")

    print("\n✅ Unificación completada correctamente.")
    print(f"   ➜ Archivo exportado: {INGRESOS_SALIDA_PATH}")
    print(f"   ➜ Total de filas: {len(df_unificado):,}")
    print(f"   ➜ Total de columnas: {len(df_unificado.columns)}")

    return df_unificado

