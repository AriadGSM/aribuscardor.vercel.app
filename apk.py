from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import json
import os

app = Flask(__name__)

def load_config():
    try:
        with open('appsettings.json', 'r') as config_file:
            config = json.load(config_file)
            environment = config.get('Environment', 'Development')
            connection_config = config['ConnectionStrings'][environment]
            
            return {
                'host': connection_config['Server'],
                'user': connection_config['User'],
                'password': connection_config['Password'],
                'database': connection_config['Database'],
                'ssl_disabled': not connection_config['Encrypt']
            }
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return None

def get_db_connection():
    try:
        config = load_config()
        if not config:
            raise Exception("No se pudo cargar la configuración")
            
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

@app.route('/')
def index():
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
            return render_template('index.html', tools=usuarios)
        except Error as e:
            print(f"Error: {e}")
            return "Error al obtener usuarios"
    return "Error de conexión a la base de datos"

@app.route('/agregar', methods=['POST'])
def agregar_tool():
    if request.method == 'POST':
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                args = (request.form['nombre'],
                       request.form['correo'],
                       request.form['usuario'],
                       request.form['contraseña'])
                cursor.callproc('agregar_usuario', args)
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('index'))
            except Error as e:
                print(f"Error: {e}")
                return "Error al agregar usuario"
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar_tool(id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('eliminar_usuario', [id])
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error: {e}")
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tool(id):
    if request.method == 'POST':
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                args = (id,
                       request.form['nombre'],
                       request.form['correo'],
                       request.form['usuario'],
                       request.form['contraseña'])
                cursor.callproc('editar_usuario', args)
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('index'))
            except Error as e:
                print(f"Error: {e}")
                return "Error al editar usuario"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)