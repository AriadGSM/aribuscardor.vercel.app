from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection
from controllers.controllerUsuario import ControllerUsuario
from models.Usuario.usuario import Usuario_toll

tool_bp = Blueprint('tool', __name__)
controller = ControllerUsuario()


# 🧾 LISTAR USUARIOS
@tool_bp.route('/')
def index():
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

    return render_template('view/index.html', tools=tools)


# ➕ AGREGAR USUARIO
@tool_bp.route('/agregar_tool', methods=['POST'])
def agregar_tool():
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
            cursor.callproc('sp_agregar_usuario', (usuario.nombre, usuario.correo, usuario.usuario, contraseña_hash))
            connection.commit()
            flash("✅ Usuario agregado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al agregar usuario: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for('tool.index'))


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

    return redirect(url_for('tool.index'))


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

    return redirect(url_for('tool.index'))
