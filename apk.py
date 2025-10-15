from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir CORS para Angular u otro frontend

# === Cargar configuración desde appsettings.json ===
def load_config():
    try:
        with open('appsettings.json', 'r') as config_file:
            config = json.load(config_file)

            # Detectar entorno actual (variable FLASK_ENV o valor por defecto)
            environment = os.getenv('Flask', config.get('Environment', 'Development'))
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


# === Conexión a MySQL ===
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


# === ENDPOINT: Listar usuarios ===
@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc('listar_usuario')
            usuarios = []
            for result in cursor.stored_results():
                usuarios = result.fetchall()
            cursor.close()
            connection.close()
            return jsonify(usuarios)
        except Error as e:
            print(f"❌ Error: {e}")
            return jsonify({'error': 'Error al obtener usuarios'}), 500
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500


# === ENDPOINT: Agregar usuario ===
@app.route('/api/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            args = (data['nombre'], data['correo'], data['usuario'], data['contraseña'])
            cursor.callproc('agregar_usuario', args)
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'mensaje': 'Usuario agregado correctamente'})
        except Error as e:
            print(f"❌ Error: {e}")
            return jsonify({'error': 'Error al agregar usuario'}), 500
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500


# === ENDPOINT: Eliminar usuario ===
@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('eliminar_usuario', [id])
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'mensaje': f'Usuario con ID {id} eliminado correctamente'})
        except Error as e:
            print(f"❌ Error: {e}")
            return jsonify({'error': 'Error al eliminar usuario'}), 500
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500


# === Punto de inicio ===
if __name__ == '__main__':
    app.run(debug=True)
