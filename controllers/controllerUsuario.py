from werkzeug.security import generate_password_hash, check_password_hash

class ControllerUsuario:
    def __init__(self):
        self.usuarios = []

    def validar_datos(self, nombre, correo, usuario, contraseña):
        if not all([nombre, correo, usuario, contraseña]):
            raise ValueError("Todos los campos son obligatorios")

        if "@" not in correo:
            raise ValueError("Correo inválido")

        if len(contraseña) < 2:
            raise ValueError("La contraseña debe tener al menos 2 caracteres")

    def hash_password(self, contraseña):
        """Genera un hash seguro de la contraseña"""
        return generate_password_hash(contraseña)

    def verificar_password(self, hash_guardado, contraseña_introducida):
        """Verifica una contraseña contra su hash"""
        return check_password_hash(hash_guardado, contraseña_introducida)
