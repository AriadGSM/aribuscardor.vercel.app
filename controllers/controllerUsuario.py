class controllerUsuario:
    def __init__(self):
        self.usuario = []
    def agregarUsuario(self, usuario):
        self.usuario.append(usuario)
    def eliminarUsuario(self, usuario):
        self.usuario.remove(usuario)
    def editarUsuario(self, usuario):
        self.usuario.remove(usuario)
        self.usuario.append(usuario)
        