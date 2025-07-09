from pathlib import Path

# Definición de rutas y patrones para unificar archivos Excel

DATA_PATH = Path("../data")  # Carpeta de entrada con archivos Excel
DATA_PROCESADA_PATH = Path("../data_procesada")  # Carpeta de salida para archivos procesados
PATRON_ARCHIVOS_PATH = "ventas_detalle_*.xlsx"  # Patrón para buscar archivos Excel
ARCHIVO_SALIDA_PATH = DATA_PROCESADA_PATH / "ventas_historico.csv"  # Archivo CSV de salida unificado
DATA_LIMPIA_PATH = DATA_PROCESADA_PATH / "ventas_limpio.csv"  # Archivo CSV limpio de salida
DATA_SIN_INFLACION = DATA_PROCESADA_PATH / "ventas_ajustado_a_jun25.csv"  # Archivo CSV ajustado por inflación
DATA_FACTURAS_PATH = DATA_PATH / "VENTAS_JUNIO_2025.txt"  # Archivo txt de facturas procesadas
DATA_FINAL_FACTURAS_PATH = DATA_PROCESADA_PATH / "ventas_final.csv"  # Archivo txt final de facturas procesadas