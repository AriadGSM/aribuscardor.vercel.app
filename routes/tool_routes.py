from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_db_connection
from controllers.controllerUsuario import ControllerUsuario
from models.Usuario.usuario import Usuario_toll

tool_bp = Blueprint(
    'tool',
    __name__,
    static_folder='../static',  
    static_url_path='/static'   
)


controller = ControllerUsuario()

# 📱 PÁGINA DE INICIO
@tool_bp.route('/')
def index():
    return render_template('view/index.html')

# 🧾 LISTAR USUARIOS
@tool_bp.route('/login')
def login():
    connection = None
    cursor = None
    tools = []

    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc('sp_listar_usuario')
            for result in cursor.stored_results():
                tools = result.fetchall()
    except Exception as e:
        flash(f"❌ Error al listar usuarios: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return render_template('view/login.html', tools=tools)


# ➕ AGREGAR USUARIO
@tool_bp.route('/agregar_tool', methods=['POST'])
def agregar_tool():
    try:
        print("Datos recibidos:", request.form)
        usuario = Usuario_toll(
            request.form.get('nombre', ''),
            request.form.get('correo', ''),
            request.form.get('usuario', ''),
            request.form.get('contrasena', '')
        )
        print("Usuario creado:", usuario)
        connection = None
        cursor = None

        try:
            controller.validar_datos(usuario.nombre, usuario.correo, usuario.usuario, usuario.contrasena)
            contraseña_hash = controller.hash_password(usuario.contrasena)

            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                cursor.callproc('sp_agregar_usuario', (usuario.nombre, usuario.correo, usuario.usuario, contraseña_hash))
                connection.commit()
                flash("✅ Usuario agregado correctamente", "success")
        except Exception as e:
            print(f"Error detallado: {str(e)}")
            flash(f"❌ Error al agregar usuario: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for('tool.login'))


# ✏️ EDITAR USUARIO
@tool_bp.route('/editar_tool/<int:id>', methods=['POST'])
def editar_tool(id):
    connection = None
    cursor = None

    usuario = Usuario_toll(
        request.form.get('nombre', ''),
        request.form.get('correo', ''),
        request.form.get('usuario', ''),
        request.form.get('contraseña', '')
    )

    try:
        controller.validar_datos(usuario.nombre, usuario.correo, usuario.usuario, usuario.contrasena)
        contraseña_hash = controller.hash_password(usuario.contrasena)

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.callproc('sp_editar_usuario', (id, usuario.nombre, usuario.correo, usuario.usuario, contraseña_hash))
            connection.commit()
            flash("✅ Usuario editado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al editar usuario: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for('tool.login'))


# 🗑️ ELIMINAR USUARIO
@tool_bp.route('/eliminar_tool/<int:id>', methods=['GET'])
def eliminar_tool(id):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.callproc('sp_eliminar_usuario', (id,))
            connection.commit()
            flash("🗑️ Usuario eliminado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al eliminar usuario: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for('tool.login'))


# 🛒 Agregar al carrito
@tool_bp.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    try:
        data = request.get_json()
        usuario_id = session.get('usuario_id')  # Asumiendo que tienes el ID del usuario en la sesión
        if not usuario_id:
            return jsonify({'error': 'Usuario no autenticado'}), 401

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.callproc('sp_agregar_al_carrito', (
                usuario_id,
                data['producto_id'],
                data['cantidad'],
                data['precio_unitario']
            ))
            connection.commit()
            return jsonify({'mensaje': 'Producto agregado al carrito'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# 🛍️ Ver carrito
@tool_bp.route('/ver_carrito')
def ver_carrito():
    try:
        usuario_id = session.get('usuario_id')
        if not usuario_id:
            return jsonify({'error': 'Usuario no autenticado'}), 401

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc('sp_obtener_carrito', (usuario_id,))
            for result in cursor.stored_results():
                items = result.fetchall()
            return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
