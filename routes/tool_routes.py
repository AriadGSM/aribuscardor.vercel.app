from flask import Blueprint, jsonify, render_template, request

tool_bp = Blueprint('tool', __name__)

@tool_bp.route('/')
def index():
    return render_template('view/index.html', tools=[])

@tool_bp.route('/agregar_tool', methods=['POST'])
def agregar_tool():
    # Implementar la lógica para agregar una tool
    return jsonify({'mensaje': 'Tool agregada correctamente'})

@tool_bp.route('/editar_tool/<int:id>', methods=['POST'])
def editar_tool(id):
    # Implementar la lógica para editar una tool
    return jsonify({'mensaje': f'Tool {id} editada correctamente'})

@tool_bp.route('/eliminar_tool/<int:id>')
def eliminar_tool(id):
    # Implementar la lógica para eliminar una tool
    return jsonify({'mensaje': f'Tool {id} eliminada correctamente'})