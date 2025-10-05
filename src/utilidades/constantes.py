from pathlib import Path

#------------RUTA-DATA-CRUDA-------------------------------------------------
DATA_PATH = Path("../data")  # Carpeta de entrada con archivos Excel
DATA_PROCESADA_PATH = Path("../data_procesada")  # Carpeta de salida para archivos procesados
DATA_UNIFICADA_FINAL_PATH = Path("../data_final")  # Carpeta de salida para archivo final unificado

#-------------RUTA-DATA-CRUDA-UNIFICADA-------------------------------------------------------------------------------------------------
# MOSTRADOR
PATRON_MOSTRADOR_PATH = "MOSTRADOR_*.xlsx"  # Patrón para buscar archivos Excel
MOSTRADOR_SALIDA_PATH = DATA_PROCESADA_PATH / "ventas_mostrador.csv"  # Archivo CSV ajustado por inflación

# FACTURACION
PATRON_FACTURACION_PATH = "FACTURACION_*.txt"  # Archivo txt de facturas procesadas
FACTURACION_SALIDA_PATH = DATA_PROCESADA_PATH / "ventas_facturacion.csv"  # Archivo txt final de facturas procesadas

# TOTAL
TOTAL_PATH = DATA_PATH / "TOTAL_2024.csv"  # Archivo CSV de ventas totales

#--------------RUTA-DATA-FINAL------------------------------------------------------------------------------------------------
# ARCHIVO FINAL UNIFICADO
ARCHIVO_UNIFICADO_PATH = DATA_UNIFICADA_FINAL_PATH / "ventas_unificadas.csv"  # Archivo CSV final unificado

# ARCHIVO FINAL DE MOSTRADOR Y FACTURACION
ARCHIVO_MOSTRADOR_FINAL_PATH = DATA_UNIFICADA_FINAL_PATH / "ventas_mostrador_final.csv"  # Archivo CSV final unificado
ARCHIVO_FACTURACION_FINAL_PATH = DATA_UNIFICADA_FINAL_PATH / "ventas_facturacion_final.csv"  # Archivo CSV final unificado

# ARCHIVO FINAL DE VENTAS TOTALES
TOTAL_FINAL_PATH = DATA_UNIFICADA_FINAL_PATH / "ventas_totales_final.csv"  # Archivo CSV final unificado


