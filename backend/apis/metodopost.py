from controller.databasecontroller import databaseController
import json 

class controllerpost():
    global database 
    database = databaseController()

    def __init__(self):
        pass

    def agregar_usuario(self, auth0id, correo, nombre):
        """ Llama al procedimiento almacenado para insertar un usuario """
        conn = database.conectar_base_datos()
        cursor = conn.cursor()
        cursor.execute("SELECT agregar_usuario(%s, %s, %s);", (auth0id, correo, nombre))
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return user_id 
    
    def registrar_restaurante(self, nombre_restaurante):
        """
        Registra un restaurante en la base de datos y devuelve un JSON en formato string con el ID registrado o un error.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('registrar_restaurante', [nombre_restaurante])
                restaurant_id = cursor.fetchone()[0]
                connection.commit()

                return json.dumps({"id_restaurante": restaurant_id})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
                if 'connection' in locals() and connection is not None:
                    connection.close()
        
    def registrar_mesa_restaurante(self, id_restaurante, id_mesa):
        """
        Registra mesa para restaurante
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('agregar_mesa', [id_restaurante, id_mesa])

                connection.commit()

                return json.dumps({"Message": "Mesa agregada"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
                if 'connection' in locals() and connection is not None:
                    connection.close()

    def crear_menu(self, descripcion_menu):
        """
        Crea un nuevo menú en la base de datos con la descripción proporcionada.
        Retorna el ID del menú creado en formato JSON.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('crear_menu', [descripcion_menu])

                # Obtener el ID del nuevo menú creado
                id_menu = cursor.fetchone()[0]

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return json.dumps({"id_menu": id_menu})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()
    
    def vincular_menu_restaurante(self, id_menu, id_restaurante):
        """
        Vincula un menu a un restaurante.
        Retorna mensaje de confirmacion.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('asociar_menu_restaurante', [id_restaurante, id_menu])

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return "Menu vinculado a restaurante"

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def crear_pedido(self, id_usuario, estado, id_restaurante):
        """
        Crea un nuevo pedido
        Retorna numero de pedido.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('insertar_pedido', [id_usuario, estado, id_restaurante])

                # Obtiene id de pedido
                id_pedido = cursor.fetchone()[0]

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return json.dumps({"id_pedido": id_pedido})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def agregar_producto(self, id_menu, nombre, precio):
        """
        Crea un nuevo producto
        Retorna numero de producto.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('crear_producto', [id_menu, nombre, precio])

                # Obtiene id de producto
                id_producto = cursor.fetchone()[0]

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return json.dumps({"id_producto" : id_producto})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def agregar_producto_pedido(self, id_producto, id_pedido, cantidad):
        """
        Crea un nuevo pedido
        Retorna numero de pedido.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('insertar_pedido_producto', [id_pedido, id_producto, cantidad])

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return json.dumps({"Message" : "Producto agregado"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def crear_reserva(self, id_mesa, id_usuario, fechaHora):
        """
        Crea una reserva
        Retorna numero de reserva.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('crear_reserva', [id_mesa, id_usuario, fechaHora])

                # Obtiene id de producto
                id_reserva = cursor.fetchone()[0]

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return json.dumps({"idReserva" : id_reserva})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()



