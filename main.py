from datetime import datetime
import csv
import os
from cliente import Cliente
from turno import Turno

class GestorTurnos:
    def __init__(self, clientes_file='clientes.csv', turnos_file='turnos.csv'):
        self.clientes = {}  
        self.turnos = {}    
        self.clientes_file = clientes_file
        self.turnos_file = turnos_file
        
        self.cargar_al_inicio()

    def cargar_al_inicio(self):
        self.cargar_clientes_csv()
        self.cargar_turnos_csv()
    
    def cargar_clientes_csv(self):
        if not os.path.exists(self.clientes_file):
            print("Archivo de clientes no encontrado. Comenzando con lista vacía.")
            return

        file = open(self.clientes_file, mode='r', encoding='utf-8')
        lineas = file.readlines()
        file.close()

        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea:
                datos = linea.split(',')
                try:
                    id_cliente = int(datos[0])
                    nombre = datos[1]
                    telefono = datos[2]
                    
                    cliente = Cliente(nombre, telefono, id_cliente=id_cliente)
                    self.clientes[id_cliente] = cliente
                except Exception as e:
                    print(f"Error al cargar línea de cliente: {linea}. Error: {e}")

    def cargar_turnos_csv(self):
        if not os.path.exists(self.turnos_file):
            print("Archivo de turnos no encontrado. Comenzando con lista vacía.")
            return

        file = open(self.turnos_file, mode='r', encoding='utf-8')
        lineas = file.readlines()
        file.close()

        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea:
                datos = linea.split(',')
                try:
                    id_turno = int(datos[0])
                    id_cliente = int(datos[1])
                    fecha_hora_str = datos[2]
                    servicio = datos[3]
                    
                    turno = Turno(id_cliente, fecha_hora_str, servicio, id_turno=id_turno)
                    self.turnos[id_turno] = turno
                except Exception as e:
                    print(f"Error al cargar línea de turno: {linea}. Error: {e}")
                    
    def guardar_datos(self):
        print("\nGuardando datos de clientes...")
        
        clientes_data = []
        for cliente in self.clientes.values():
            clientes_data.append(cliente.a_dict())              
        
        if clientes_data:
            columnas = ['id_cliente', 'nombre', 'telefono']

            with open(self.clientes_file, 'w', encoding='utf-8') as file:   
                header_line = ",".join(columnas) + "\n"
                file.write(header_line)

                for data in clientes_data:
                    vector = []     
                    for col in columnas:
                        vector.append(str(data[col]))
                        
                    fila = ",".join(vector) + "\n"
                    file.write(fila) 

        print("Guardando datos de turnos...")
        
        turnos_data = []
        for turno in self.turnos.values():
            turnos_data.append(turno.a_dict())
        
        if turnos_data:
            columnas = ['id_turno', 'id_cliente', 'fecha_hora', 'servicio']

            with open(self.turnos_file, 'w', encoding='utf-8') as file:
                header_line = ",".join(columnas) + "\n"
                file.write(header_line)
                
                
                for data in turnos_data:
                    vector = []
                    for col in columnas:
                        vector.append(str(data[col]))
                        
                    fila = ",".join(vector) + "\n"
                    file.write(fila)
        
        print("Datos guardados exitosamente.")

    def registrar_cliente(self):
        print("\n--- Registrar Nuevo Cliente ---")
        nombre = input("Ingrese nombre del cliente: ").strip()
        telefono = input("Ingrese teléfono de contacto: ").strip()

        for cliente in self.clientes.values():
            if cliente.telefono == telefono:
                print(f"El teléfono {telefono} ya está registrado para {cliente.nombre}.")
                return

        try:
            nuevo_cliente = Cliente(nombre, telefono)
            self.clientes[nuevo_cliente.id_cliente] = nuevo_cliente
            print(f"Cliente registrado: {nuevo_cliente}")
            self.guardar_datos() 
        except Exception as e:
            print(f"Error al registrar cliente: {e}")

    def solicitar_turno(self):
        print("\n--- Solicitar Turno ---")
        if not self.clientes:
            print("No hay clientes registrados. Registre uno primero.")
            return

        self.listar_clientes_simples()
        try:
            id_cliente = int(input("Ingrese el ID del cliente que solicita el turno: "))
        except ValueError:
            print("Entrada inválida. Debe ser un número.")
            return

        if id_cliente not in self.clientes:
            print("ID de cliente no encontrado.")
            return
            
        cliente = self.clientes[id_cliente]
        print(f"Cliente seleccionado: {cliente.nombre}")

        fecha_hora_str = input("Ingrese Fecha y Hora (YYYY-MM-DD HH:MM): ").strip()
        servicio = input("Ingrese Servicio (ej: Corte, Tinte, etc.): ").strip()

        try:
            if self.turno_duplicado(fecha_hora_str): 
                print("Horario no disponible. Ya hay un turno agendado a esa hora.")
                return

            nuevo_turno = Turno(id_cliente, fecha_hora_str, servicio)
            self.turnos[nuevo_turno.id_turno] = nuevo_turno
            print(f"Turno solicitado: {nuevo_turno}")
            self.guardar_datos() 

        except ValueError:
            print("Error en el formato de fecha/hora o datos. Intente de nuevo.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def turno_duplicado(self, fecha_hora_str):
        try:
            nueva_fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return False 

        for turno in self.turnos.values():
            if turno.fecha_hora == nueva_fecha_hora:
                return True
        return False

    def modificar_o_cancelar_turno(self):
        print("\n--- Modificar o Cancelar Turno ---")
        if not self.turnos:
            print("No hay turnos registrados para modificar o cancelar.")
            return

        self.listar_turnos()

        try:
            id_turno = int(input("Ingrese el ID del turno a modificar/cancelar: "))
        except ValueError:
            print("Entrada inválida. Debe ser un número.")
            return

        if id_turno not in self.turnos:
            print(f"No se encontró ningún turno con ID {id_turno}.")
            return

        print(f"\nTurno seleccionado: {self.turnos[id_turno]}")
        
        accion = input("¿Desea (M)odificar o (C)ancelar este turno? ").strip().upper()

        if accion == 'C':
            self.cancelar_turno(id_turno)
        elif accion == 'M':
            self.modificar_turno(id_turno)
        else:
            print("Opción no válida. Cancelando operación.")
            
    def cancelar_turno(self, id_turno):
        confirmacion = input("¿Está seguro que desea CANCELAR este turno? (S/N): ").strip().upper()
        
        if confirmacion == 'S':
            del self.turnos[id_turno]
            print(f"Turno ID {id_turno} ha sido cancelado exitosamente.")
            self.guardar_datos()
        else:
            print("Cancelación anulada.")

    def modificar_turno(self, id_turno):
        turno = self.turnos[id_turno]
        print("\nSeleccione qué desea modificar:")
        print("1. Fecha y Hora")
        print("2. Servicio")
        
        opcion = input("> ").strip()

        if opcion == '1':
            nueva_fecha_hora_str = input("Ingrese NUEVA Fecha y Hora (YYYY-MM-DD HH:MM): ").strip()
            
            try:
                if self.turno_duplicado_excluyendo(nueva_fecha_hora_str, id_turno):
                    print("ERROR: El nuevo horario no está disponible.")
                    return
                    
                turno.fecha_hora = turno.convierte_fecha_hora(nueva_fecha_hora_str)
                print("Fecha y hora modificadas exitosamente.")

            except ValueError:
                print("Error: Formato de fecha y hora incorrecto. Modificación cancelada.")
                return

        elif opcion == '2':
            nuevo_servicio = input(f"Ingrese NUEVO Servicio (actual: {turno.servicio}): ").strip()
            if nuevo_servicio:
                turno.servicio = nuevo_servicio
                print("Servicio modificado exitosamente.")
            else:
                print("Servicio no modificado.")
        else:
            print("Opción de modificación no válida.")
            return

        print(f"Datos del turno actualizados: {turno}")
        self.guardar_datos()

    def turno_duplicado_excluyendo(self, fecha_hora_str, id_turno_excluir):
        try:
            nueva_fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return False 

        for id_t, turno in self.turnos.items():
            if id_t != id_turno_excluir and turno.fecha_hora == nueva_fecha_hora:
                return True
        return False    


    def listar_turnos(self):
        print("\n--- Listado de Turnos ---")
        if not self.turnos:
            print("No hay turnos registrados.")
            return
        
        print("Filtros (opcional): (F)echa, (C)liente, (T)odos. Ingrese la letra:")
        filtro = input("> ").strip().upper()
        
        turnos_filtrados = [] 

        if filtro == 'F':
            fecha_str = input("Ingrese fecha a filtrar (YYYY-MM-DD): ").strip()
            for t in self.turnos.values():
                 if t.fecha_hora.strftime('%Y-%m-%d') == fecha_str:
                    turnos_filtrados.append(t)
        elif filtro == 'C':
            self.listar_clientes_simples()
            try:
                id_cliente = int(input("Ingrese ID del cliente a filtrar: "))
                for t in self.turnos.values():
                    if t.id_cliente == id_cliente:
                        turnos_filtrados.append(t)
            except ValueError:
                print("ID inválido, mostrando todos.")
        else:
            for t in self.turnos.values():
                turnos_filtrados.append(t)

        if not turnos_filtrados:
            print("No se encontraron turnos con ese filtro.")
            return

        for turno in sorted(turnos_filtrados, key=lambda t: t.fecha_hora):
            cliente = self.clientes.get(turno.id_cliente, "Cliente Desconocido")
            nombre_cliente = cliente.nombre if isinstance(cliente, Cliente) else cliente
            print(f"[{turno.id_turno}] {turno.fecha_hora.strftime('%Y-%m-%d %H:%M')} | Cliente: {nombre_cliente} (ID: {turno.id_cliente}) | Servicio: {turno.servicio}")


    def listar_clientes_simples(self):
        print("\n--- Clientes Registrados ---")
        for c in self.clientes.values():
            print(f"ID: {c.id_cliente} - {c.nombre}")
        print("----------------------------")

    def menu_principal(self):
        while True:
            print("\n" + "="*40)
            print("===== Sistema de Turnos de Peluquería =====")
            print("="*40)
            print("1. Registrar nuevo cliente")
            print("2. Solicitar turno")
            print("3. Listar turnos existentes")
            print("4. Modificar o cancelar turno")
            print("5. Guardar datos en CSV / Cargar desde dict")
            print("6. Salir")
            print("="*40)
            
            opcion = input("Ingrese su opción: ").strip()
            
            try:
                if opcion == '1':
                    self.registrar_cliente()
                elif opcion == '2':
                    self.solicitar_turno()
                elif opcion == '3':
                    self.listar_turnos()
                elif opcion == '4':
                    self.modificar_o_cancelar_turno()
                elif opcion == '5':
                    self.guardar_datos()
                elif opcion == '6':
                    self.guardar_datos() 
                    print("Adiós. ¡Gracias por usar el sistema!")
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
            except Exception as e:
                print(f"Ocurrió un error en la operación: {e}")

if __name__ == "__main__":
    gestor = GestorTurnos()
    gestor.menu_principal()


