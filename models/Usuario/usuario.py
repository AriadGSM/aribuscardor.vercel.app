class Usuario_toll:
    def __init__(self, nombre, correo, usuario, contrasena):
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.usuario = usuario.strip()
        self.contrasena = contrasena.strip()

    def __str__(self):
        return f"Usuario({self.nombre}, {self.correo}, {self.usuario})"
