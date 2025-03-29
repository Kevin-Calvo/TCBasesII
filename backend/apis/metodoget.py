from controller.databasecontroller import databaseController
import json 


class controllerget():
    global database 
    database = databaseController()

    def __init__(self):
        pass

    def obtener_usuario_por_id(self, user_id):
        connection = database.conectar_base_datos()
        if not connection:
            return "Error de conexión a la base de datos"

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM obtener_usuario_por_id(%s);", (user_id,))
                resultado = cursor.fetchall()

                if not resultado:
                    return "Usuario no encontrado"
                
                # Convertir los resultados en una cadena legible
                usuario_info = "\n".join([f"Nombre: {nombre}, Correo: {correo}" for nombre, correo in resultado])
                return usuario_info
        except Exception as ex:
            return f"Error al ejecutar la consulta: {str(ex)}"
        finally:
            connection.close()

    def consultar_restaurantes(self):
        """
        Consulta la lista de restaurantes y devuelve un JSON en formato string.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('consultar_restaurante')
                resultados = cursor.fetchall()
                connection.commit()

                restaurantes = [{"id_restaurante": row[0], "nombre": row[1]} for row in resultados]
                return json.dumps(restaurantes)

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def consultar_mesas_por_restaurante(self, post_data):
        """
        Recibe post_data (cuerpo de la solicitud HTTP) como un JSON string.
        Devuelve un mensaje en formato str con las mesas del restaurante.
        """
        try:
            data = json.loads(post_data)  # Convertir JSON a diccionario
            id_restaurante = data.get("id_restaurante")

            if not id_restaurante:
                return json.dumps({"error": "Falta el campo 'id_restaurante'"})

            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('consultar_mesas_por_restaurante', [id_restaurante])
                resultados = cursor.fetchall()
                connection.commit()

                mesas = [{"restaurante": row[0], "id_mesa": row[1]} for row in resultados]
                return json.dumps(mesas)

        except json.JSONDecodeError:
            return json.dumps({"error": "Formato JSON inválido"})

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def consultar_productos_por_restaurante(self, id_restaurante):
        """
        Consulta los productos de un restaurante en la base de datos y devuelve un JSON en formato string.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('consultar_productos_por_restaurante', [id_restaurante])
                resultados = cursor.fetchall()
                connection.commit()

                if not resultados:
                    return json.dumps({"error": "No se encontraron productos para el restaurante especificado"})

                # Extraer el ID del restaurante desde los resultados
                id_restaurante = resultados[0][1]

                productos = []
                for row in resultados:
                    productos.append({
                        "menu": row[2],
                        "id_menu": row[3],
                        "id_producto": row[4],
                        "nombre": row[5],
                        "precio": float(row[6])
                    })

                respuesta = {
                    "id_restaurante": id_restaurante,
                    "productos": productos
                }

                return json.dumps(respuesta)

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()


    def consultar_menus(self):
        """
        Consulta los menús en la base de datos y devuelve un JSON en formato string.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                cursor.callproc('consultar_menus')
                resultados = cursor.fetchall()
                connection.commit()

                menus = [{"id_menu": row[0], "descripcion": row[1]} for row in resultados]
                return json.dumps(menus)

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def obtener_pedido(self, id_producto):
        """
        Ejecuta la consulta para obtener los detalles del pedido de un producto dado su ID.
        Retorna un JSON con los detalles del pedido.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Ejecutar la consulta usando el id_producto
                cursor.callproc('mostrar_detalles_pedido', [id_producto])

                # Obtener los resultados de la consulta
                rows = cursor.fetchall()
                detalles = []

                for row in rows:
                    # Convertir cada fila de la consulta a un diccionario para un mejor formato JSON
                    detalles.append({
                        "NombreProducto": row[0],
                        "Cantidad": row[1],
                        "PrecioProducto": float(row[2]),
                        "TotalPorProducto": float(row[3]),
                        "TotalPedido": float(row[4]),
                        "NombreUsuario": row[5],
                        "EstadoPedido": row[6]
                    })

                # Retornar los detalles como un JSON
                return json.dumps(detalles)

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()

    def consultar_reservas_por_usuario(self, id_usuario):
        """
        Ejecuta la consulta para obtener las reservas de un usuario dado su ID.
        Retorna un JSON con las reservas.
        """
        try:
            connection = database.conectar_base_datos()
            if not connection:
                return json.dumps({"error": "Error de conexión a la base de datos"})

            with connection.cursor() as cursor:
                # Ejecutar la consulta para consultar reservas por usuario
                cursor.callproc('consultar_reserva', [id_usuario])

                # Obtener los resultados de la consulta
                rows = cursor.fetchall()
                reservas = []

                for row in rows:
                    # Convertir cada fila de la consulta a un diccionario
                    reservas.append({
                        "NombreRestaurante": row[0],
                        "IdMesa": row[1],
                        "FechaReserva": row[2].strftime('%Y-%m-%d %H:%M:%S')  # Convertir timestamp a string
                    })

                # Retornar las reservas en formato JSON
                return json.dumps(reservas)

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()





        