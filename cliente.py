class Cliente:

    next_id = 1 

    def __init__(self, nombre, telefono, id_cliente=None):
        self.id_cliente = id_cliente if id_cliente is not None else Cliente.next_id
        self.nombre = nombre
        self.telefono = telefono

        if id_cliente is None:
            Cliente.next_id += 1
        elif id_cliente >= Cliente.next_id:
            Cliente.next_id = id_cliente + 1

    def __str__(self):
        return f"ID: {self.id_cliente}, Nombre: {self.nombre}, Teléfono: {self.telefono}"
    
    def a_dict(self):
        return {
            'id_cliente': self.id_cliente,
            'nombre': self.nombre,
            'telefono': self.telefono
        }
    



    
