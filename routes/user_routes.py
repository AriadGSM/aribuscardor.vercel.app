from flask import Blueprint, jsonify, request
from database import get_db_connection
from mysql.connector import Error

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/usuarios', methods=['GET'])
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

@user_bp.route('/api/usuarios', methods=['POST'])
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

@user_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
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