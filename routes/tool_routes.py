from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_db_connection
from controllers.controllerUsuario import ControllerUsuario
from models.Usuario.usuario import Usuario_toll
from flask import session  # Agregar esta importación al inicio del archivo
from functools import wraps
from werkzeug.utils import secure_filename
import os

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


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('❌ Acceso denegado. Se requieren privilegios de administrador.', 'danger')
            return redirect(url_for('tool.login'))
        return f(*args, **kwargs)
    return decorated_function

# 👤 Ruta para login de administrador
@tool_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        
        try:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                # Verificar credenciales del administrador
                cursor.execute("SELECT * FROM usuario WHERE usuario = %s AND is_admin = 1", (usuario,))
                admin = cursor.fetchone()
                
                if admin and controller.verificar_password(admin['contrasena'], contrasena):
                    session['usuario_id'] = admin['idUsua']
                    session['is_admin'] = True
                    flash('✅ Inicio de sesión exitoso como administrador', 'success')
                    return redirect(url_for('tool.admin_dashboard'))
                else:
                    flash('❌ Credenciales inválidas o usuario no es administrador', 'danger')
        except Exception as e:
            flash(f'❌ Error en el inicio de sesión: {str(e)}', 'danger')
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                
    return render_template('view/admin_login.html')

# 📊 Panel de administrador
@tool_bp.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('view/admin.html')

# 📦 Agregar producto
@tool_bp.route('/admin/agregar_producto', methods=['POST'])
@admin_required
def agregar_producto():
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        imagen = request.files.get('imagen')
        
        if imagen:
            # Guardar la imagen en la carpeta static/img
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join('static/src/img', filename)
            imagen.save(os.path.join(tool_bp.root_path, '..', imagen_path))
        else:
            imagen_path = None
            
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, descripcion, precio, imagen)
                VALUES (%s, %s, %s, %s)
            """, (nombre, descripcion, precio, imagen_path))
            connection.commit()
            flash('✅ Producto agregado correctamente', 'success')
            
    except Exception as e:
        flash(f'❌ Error al agregar producto: {str(e)}', 'danger')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
    return redirect(url_for('tool.admin_dashboard'))
