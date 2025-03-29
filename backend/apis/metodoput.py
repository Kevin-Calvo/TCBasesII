from controller.databasecontroller import databaseController
import json 

class controllerput():
    global database 
    database = databaseController()

    def __init__(self):
        pass

    def usuario_update(self, user_id, correo, nombre):
        """
        Actualiza la información de un usuario en la base de datos y devuelve un JSON en formato string con el resultado.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('actualizar_usuario', [user_id, correo, nombre])
                connection.commit()

                return json.dumps({"message": "Usuario actualizado con éxito"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def restaurante_update(self, restaurante_id, nombre):
        """
        Actualiza la información de un restaurante en la base de datos y devuelve un JSON en formato string con el resultado.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('modificar_restaurante', [restaurante_id, nombre])
                connection.commit()

                return json.dumps({"message": "Restaurante actualizado con éxito"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def modificar_menu(self, id_menu, descripcion_menu):
        """
        Modifica la descripción de un menú en la base de datos.
        Retorna un mensaje de éxito en formato JSON.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para modificar el menú
                cursor.callproc('modificar_menu', [id_menu, descripcion_menu])

                # Confirmar la transacción
                connection.commit()

                # Retornar el mensaje de éxito
                return json.dumps({"message": "Modificación con éxito"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()
    
    def modificar_pedido(self, id_pedido, estado):
        """
        Modifica el estado de un pedido.
        Retorna un mensaje de éxito en formato JSON.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para modificar el menú
                cursor.callproc('modificar_estado_pedido', [id_pedido, estado])

                # Confirmar la transacción
                connection.commit()

                # Retornar el mensaje de éxito
                return json.dumps({"message": "Modificación con éxito"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def modificar_producto(self, id_producto, nombre, precio):
        """
        Modifica datos de un producto
        Retorna un mensaje de éxito en formato JSON.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para modificar el menú
                cursor.callproc('modificar_producto', [id_producto, nombre, precio])

                # Confirmar la transacción
                connection.commit()

                # Retornar el mensaje de éxito
                return json.dumps({"message": "Modificación con éxito"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()
