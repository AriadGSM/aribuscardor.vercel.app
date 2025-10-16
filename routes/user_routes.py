from flask import Blueprint, jsonify, request, render_template
from database import get_db_connection
from mysql.connector import Error

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    print("⌛ Intentando conectar a la base de datos...")
    connection = get_db_connection()
    if connection:
        try:
            print("✅ Conexión exitosa a la base de datos")
            cursor = connection.cursor(dictionary=True)
            print("⌛ Ejecutando procedimiento listar_usuario...")
            cursor.callproc('listar_usuario')
            usuarios = []
            for result in cursor.stored_results():
                usuarios = result.fetchall()
            print(f"📋 Usuarios encontrados: {usuarios}")
            cursor.close()
            connection.close()
            return render_template('view/index.html', tools=usuarios)
        except Error as e:
            print(f"❌ Error al ejecutar procedimiento: {e}")
            return render_template('view/index.html', tools=[])
    print("❌ No se pudo conectar a la base de datos")
    return render_template('view/index.html', tools=[])

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

