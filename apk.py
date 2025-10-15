from flask import Flask
from flask_cors import CORS
from routes.tool_routes import tool_bp
from routes.user_routes import user_bp

app = Flask(__name__)
CORS(app)  # Permitir CORS para Angular u otro frontend

# Registrar los blueprints
app.register_blueprint(tool_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
