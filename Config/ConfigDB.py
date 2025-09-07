import os
from dotenv import load_dotenv

class ConfigDB:
    """
    Clase de configuración para rutas y parámetros del ETL.
    """
    # Cargar variables de entorno
    load_dotenv()

    # Rutas de archivos
    INPUT_PATH = 'Pokemon.csv'
    OUTPUT_PATH = 'output/Pokemon_clean.csv'
    
    # Configuración MySQL
    MYSQL_TABLE = 'pokemon'
    MYSQL_CONFIG = {
        'host': os.getenv('DBHOST'),
        'user': os.getenv('DBUSER'),
        'password': os.getenv('DBPASSWORD'),
        'port': os.getenv('DBPORT'),
        'database': os.getenv('DBDATABASE_NAME')
    }
