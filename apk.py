from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# ✅ Cargar variables de entorno antes de crear la app
load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir CORS para Angular u otro frontend

# ✅ Configurar clave secreta
app.secret_key = os.getenv("SECRET_KEY") or "clave_por_defecto_segura"

# 🧩 Registrar blueprints
from routes.tool_routes import tool_bp
from routes.user_routes import user_bp

app.register_blueprint(tool_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
