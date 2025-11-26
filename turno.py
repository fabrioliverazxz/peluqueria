from datetime import datetime

class Turno:
    Tur_id = 1

    def __init__(self, id_cliente, fecha_hora_str, servicio, id_turno=None):
        self.id_turno = id_turno if id_turno is not None else Turno.Tur_id
        self.id_cliente = id_cliente
        self.servicio = servicio
        
        self.fecha_hora = self.convierte_fecha_hora(fecha_hora_str)

        if id_turno is None:
            Turno.Tur_id += 1
        elif id_turno >= Turno.Tur_id:
            Turno.Tur_id = id_turno + 1

    def convierte_fecha_hora(self, fecha_hora_str):
        try:
            return datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
        except ValueError:
            print("Error: Formato de fecha y hora incorrecto. Use YYYY-MM-DD HH:MM.")
            raise 
    
    def __str__(self):
        return (f"ID Turno: {self.id_turno} | Cliente ID: {self.id_cliente} | "
                f"Fecha/Hora: {self.fecha_hora.strftime('%Y-%m-%d %H:%M')} | Servicio: {self.servicio}")

    def a_dict(self):
        return {
            'id_turno': self.id_turno,
            'id_cliente': self.id_cliente,
            'fecha_hora': self.fecha_hora.strftime('%Y-%m-%d %H:%M'), 
            'servicio': self.servicio
        }