from pathlib import Path

#------------RUTA-DATA-CRUDA-------------------------------------------------
DATA_PATH = Path("../../1_data")  # Carpeta de entrada con archivos Excel
DATA_PROCESADA_PATH = Path("../../2_data_procesada")  # Carpeta de salida para archivos procesados
DATA_UNIFICADA_FINAL_PATH = Path("../../3_data_final")  # Carpeta de salida para archivo final unificado

#-------------RUTA-DATA-CRUDA-UNIFICADA-------------------------------------------------------------------------------------------------
# MOSTRADOR
PATRON_MOSTRADOR_PATH = "MOSTRADOR_*.xlsx"  # Patrón para buscar archivos Excel
MOSTRADOR_SALIDA_PATH = DATA_PROCESADA_PATH / "ventas_mostrador.csv"  # Archivo CSV ajustado por inflación

# FACTURACION
PATRON_SERVICIOS_PATH = "FACTURACION_*.txt"  # Archivo txt de facturas de servicios procesadas
SERVICIOS_SALIDA_PATH = DATA_PROCESADA_PATH / "ventas_servicios.csv"  # Archivo txt final de facturas de servicios procesadas

# TOTAL
PATRON_INGRESOS_PATH = "TOTAL_*.csv"  # Archivo CSV de ventas totales
INGRESOS_SALIDA_PATH = DATA_PROCESADA_PATH / "ingresos_totales.csv"  # Archivo CSV de ventas totales ajustado por inflación

#--------------RUTA-DATA-FINAL------------------------------------------------------------------------------------------------
# ARCHIVO FINAL UNIFICADO
ARCHIVO_UNIFICADO_PATH = DATA_UNIFICADA_FINAL_PATH / "ventas_unificadas.csv"  # Archivo CSV final unificado

# ARCHIVO FINAL DE MOSTRADOR Y FACTURACION
ARCHIVO_MOSTRADOR_FINAL_PATH = DATA_UNIFICADA_FINAL_PATH / "ventas_mostrador_final.csv"  # Archivo CSV final unificado
ARCHIVO_SERVICIOS_FINAL_PATH = DATA_UNIFICADA_FINAL_PATH / "ventas_servicios_final.csv"  # Archivo CSV final unificado

# ARCHIVO FINAL DE VENTAS TOTALES
ARCHIVO_INGRESOS_FINAL_PATH = DATA_UNIFICADA_FINAL_PATH / "ingresos_totales_final.csv"  # Archivo CSV final unificado


