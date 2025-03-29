from controller.databasecontroller import databaseController
import json 

class controllerdelete():
    global database 
    database = databaseController()

    def __init__(self):
        pass

    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario.
        Retorna un mensaje de éxito en formato JSON.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para modificar el menú
                cursor.callproc('eliminar_usuario', [id_usuario])

                # Confirmar la transacción
                connection.commit()

                # Retornar el mensaje de éxito
                return json.dumps({"message": "Usuario eliminado con éxito"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def eliminar_menu(self, id_menu):
        """
        Elimina un usuario.
        Retorna un mensaje de éxito en formato JSON.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para modificar el menú
                cursor.callproc('eliminar_menu', [id_menu])

                # Confirmar la transacción
                connection.commit()

                # Retornar el mensaje de éxito
                return json.dumps({"message": "Menu eliminado con éxito"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def eliminar_menu_restaurante(self, id_menu, id_restaurante):
        """
        Elimina vincula de un menu a un restaurante.
        Retorna mensaje de confirmacion.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('eliminar_menu_restaurante', [id_restaurante, id_menu])

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return "Vinculo de menu a restaurante eliminado"

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto
        Retorna mensaje de confirmacion.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('eliminar_producto', [id_producto])

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return "Producto eliminado"

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def eliminar_restaurante(self, id_restaurante):
        """
        Elimina un restaurante
        Retorna mensaje de confirmacion.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('eliminar_restaurante', [id_restaurante])

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return "Restaurante eliminado"

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def eliminar_mesa(self, id_mesa):
        """
        Elimina una mesa
        Retorna mensaje de confirmacion.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('eliminar_mesa', [id_mesa])

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return "Mesa eliminada"

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def eliminar_reserva(self, id_reserva):
        """
        Elimina una reserva
        Retorna mensaje de confirmacion.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Llamar al procedimiento almacenado para crear el menú
                cursor.callproc('eliminar_reserva', [id_reserva])

                # Confirmar la transacción
                connection.commit()

                # Retornar el ID del menú en formato JSON
                return "Reserva eliminada"

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()