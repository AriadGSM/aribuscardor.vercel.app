import mysql.connector
from mysql.connector import Error
import json
import os

def load_config():
    try:
        with open('appsettings.json', 'r') as config_file:
            config = json.load(config_file)
            environment = os.getenv('FLASK_ENV', config.get('Environment', 'Development'))
            conn_cfg = config['ConnectionStrings'][environment]
            print(f"✅ Entorno actual: {environment}")
            return {
                'host': conn_cfg['Server'],
                'user': conn_cfg['User'],
                'password': conn_cfg['Password'],
                'database': conn_cfg['Database'],
                'ssl_disabled': not conn_cfg['Encrypt']
            }
    except Exception as e:
        print(f"❌ Error al cargar configuración: {e}")
        return None

def get_db_connection():
    try:
        cfg = load_config()
        if not cfg:
            raise Exception("Configuración inválida o no encontrada")
        connection = mysql.connector.connect(**cfg)
        return connection
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None