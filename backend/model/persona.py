class Persona:
    def __init__(self, nombre, apellido, correo, id):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.id = id

    def __str__(self):
        return f"Nombre: {self.nombre}\\nApellido: {self.apellido}\\nCorreo: {self.correo}"
    
    def getId(self):
        return self.id 