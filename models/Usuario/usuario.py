class usuario :
    def __init__(self, nombre, correo, usuario, contrasena):
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.contrasena = contrasena

    def __str__(self):
        return f"Nombre: {self.nombre}, Correo: {self.correo}, Usuario: {self.usuario}, Contraseña: {self.contrasena}"
        