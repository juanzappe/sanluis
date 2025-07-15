from pathlib import Path

# Definición de rutas y patrones para unificar archivos Excel

DATA_PATH = Path("../data")  # Carpeta de entrada con archivos Excel
DATA_PROCESADA_PATH = Path("../data_procesada")  # Carpeta de salida para archivos procesados

# MOSTRADOR
PATRON_MOSTRADOR_PATH = "MOSTRADOR_*.xlsx"  # Patrón para buscar archivos Excel
MOSTRADOR_SALIDA_PATH = DATA_PROCESADA_PATH / "ventas_mostrador.csv"  # Archivo CSV ajustado por inflación

# FACTURACION
PATRON_FACTURACION_PATH = "FACTURACION_*.txt"  # Archivo txt de facturas procesadas
FACTURACION_SALIDA_PATH = DATA_PROCESADA_PATH / "ventas_facturacion.csv"  # Archivo txt final de facturas procesadas

ARCHIVO_UNIFICADO_PATH = DATA_PROCESADA_PATH / "ventas_unificadas.csv"  # Archivo CSV final unificado
