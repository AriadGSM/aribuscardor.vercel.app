from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tools.db'
db = SQLAlchemy(app)

# Modelo para las herramientas
class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    usuario = db.Column(db.String(80), nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)

# Rutas
@app.route('/')
def index():
    tools = Tool.query.all()
    return render_template('index.html', tools=tools)

@app.route('/agregar', methods=['POST'])
def agregar_tool():
    if request.method == 'POST':
        nuevo_tool = Tool(
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            usuario=request.form['usuario'],
            contraseña=request.form['contraseña']
        )
        db.session.add(nuevo_tool)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar_tool(id):
    tool = Tool.query.get_or_404(id)
    db.session.delete(tool)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tool(id):
    tool = Tool.query.get_or_404(id)
    if request.method == 'POST':
        tool.nombre = request.form['nombre']
        tool.correo = request.form['correo']
        tool.usuario = request.form['usuario']
        tool.contraseña = request.form['contraseña']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', tool=tool)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)