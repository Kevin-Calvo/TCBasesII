from http.server import BaseHTTPRequestHandler
from model.persona import Persona
from  apis.metodoget import controllerget
from  apis.metodopost import controllerpost
from  apis.metodoput import controllerput
from  apis.metododelete import controllerdelete
from controller.databasecontroller import databaseController
import psycopg2
import os
import json 
from dotenv import load_dotenv



class ControllerAPI(BaseHTTPRequestHandler):
    global database 
    database = databaseController()

    global getController 
    getController = controllerget()

    global postController
    postController = controllerpost()

    global putController
    putController = controllerput()

    global deleteController
    deleteController = controllerdelete()

    #APIS GET 

    def do_GET(self):
        persona = Persona('Kevin', 'Calvo', 'kevin@hotmail.com', '2')
        #Prueba conexion a base de datos
        if self.path == "/prueba/database":
            connection = database.conectar_base_datos()
            if not connection :
                self.enviar_mensaje("Conexion Fallida")
            else :
                self.enviar_mensaje("Conexion Exitosa")
            connection.close()

        #Obtener datos del usuario autenticado
        elif self.path == "/users/me":
            if persona.getId() != None :
                self.enviar_mensaje(getController.obtener_usuario_por_id(persona.getId()))
            else :
                self.enviar_mensaje("Sesion no iniciada")
                
        # Listar restaurantes
        elif self.path == "/restaurante/consultar":
            mensaje = getController.consultar_restaurantes()
            self.enviar_mensaje(mensaje)

        # Consultar mesas por restaurante
        elif self.path == "/restaurante/mesas/consultar":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            mensaje = getController.consultar_mesas_por_restaurante(post_data)
            self.enviar_mensaje(mensaje)

        #Obtener productos de un restaurante
        elif self.path == "/menu/restaurante/info":
        # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_restaurante = data.get("id_restaurante")
                
                # Verificar que el restauranteid está presente
                if not id_restaurante:
                    self.enviar_mensaje("Error: Falta el campo 'id_restaurante'")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = getController.consultar_productos_por_restaurante(id_restaurante)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
                
        #Obtener menus
        elif self.path == "/menu/info":
            mensaje = getController.consultar_menus()
            self.enviar_mensaje(mensaje)
            return
        
        #Consultar pedido
        elif self.path == "/pedido/info":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_pedido = data.get("id_pedido")
                
                # Verificar que el restauranteid está presente
                if not id_pedido:
                    self.enviar_mensaje("Error: Falta el campo 'id_pedido'")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = getController.obtener_pedido(id_pedido)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return
        
        #Consultar resrvas de un usaurio
        elif self.path == "/reserva/usuario/info":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_usuario = data.get("id_usuario")
                
                # Verificar que el restauranteid está presente
                if not id_usuario:
                    self.enviar_mensaje("Error: Falta el campo 'id_usuario'")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = getController.consultar_reservas_por_usuario(id_usuario)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return
        #Ruta no encontrada
        else:
            self.send_response(404)
            self.end_headers()


    #APIS POST 

    def do_POST(self):
         #Registrar usuario
        if self.path == "/register":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario

            auth0id = data.get("auth0id")
            correo = data.get("correo")
            nombre = data.get("nombre")

            if not auth0id or not correo or not nombre:
                mensaje = "Erros: Todos los campos son requeridos"
                self.enviar_mensaje(mensaje)
                return

            try:
                user_id = postController.agregar_usuario(auth0id, correo, nombre)
                self.enviar_mensaje(json.dumps({"id_usuario": user_id}))
            except Exception as e:
                self.enviar_mensaje("error" + str(e))

        #Registrar restaurante
        elif self.path == "/restaurante/new":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario

            # Obtener el nombre del restaurante del JSON
            nombre_restaurante = data.get("nombre")

            if not nombre_restaurante:
                self.enviar_mensaje("Error: Falta el campo 'nombre'")
                return

            # Llamar a la función para registrar el restaurante
            mensaje = postController.registrar_restaurante(nombre_restaurante)
            self.enviar_mensaje(mensaje)

        elif self.path == "/restaurante/mesas/new":
             # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario

            # Obtener el nombre del restaurante del JSON
            id_restaurante = data.get("id_restaurante")
            id_mesa = data.get("id_mesa")

            if not id_restaurante or not id_mesa:
                self.enviar_mensaje("Error: Faltan campos de informacion")
                return

            # Llamar a la función para registrar el restaurante
            mensaje = postController.registrar_mesa_restaurante(id_restaurante, id_mesa)
            self.enviar_mensaje(mensaje)
            return
        
        #Crear menu
        elif self.path == "/menu/new":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                descripcion = data.get("descripcion")
                
                # Verificar que el restauranteid está presente
                if not descripcion:
                    self.enviar_mensaje("Error: Falta el campo 'descripcion'")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = postController.crear_menu(descripcion)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return
        
        #Vincular menu con restaurante
        elif self.path == "/menu/restaurante":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_menu = data.get("id_menu")
                id_restaurante = data.get("id_restaurante")
                
                # Verificar que el restauranteid está presente
                if not id_menu or not id_restaurante:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = postController.vincular_menu_restaurante(id_menu, id_restaurante)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return

        #Agregar producto
        elif self.path == "/producto/new":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_menu = data.get("id_menu")
                nombre = data.get("nombre")
                precio = data.get("precio")
                
                # Verificar que el restauranteid está presente
                if not id_menu or not nombre or not precio:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = postController.agregar_producto(id_menu, nombre, precio)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return

        #Crear reserva
        elif self.path == "/reserva/new":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_mesa = data.get("id_mesa")
                id_usuario = data.get("id_usuario")
                fechaHora = data.get("fechaHora")
                
                # Verificar que los datos estan presentes
                if not id_usuario or not id_mesa or not fechaHora:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = postController.crear_reserva(id_mesa, id_usuario, fechaHora)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return
        
        #Crear pedido
        elif self.path == "/pedido/new":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_usuario = data.get("id_usuario")
                estado = data.get("estado")
                id_restaurante = data.get("id_restaurante")
                
                # Verificar que los datos estan presentes
                if not id_usuario or not id_restaurante or not estado:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = postController.crear_pedido(id_usuario, estado, id_restaurante)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return
        
        #Agregar producto a pedido
        elif self.path == "/pedido/producto/new":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_pedido = data.get("id_pedido")
                id_producto = data.get("id_producto")
                cantidad = data.get("cantidad")
                
                # Verificar que los datos estan presentes
                if not id_pedido or not id_producto or not cantidad:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = postController.agregar_producto_pedido(id_pedido, id_producto, cantidad)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return

        #Ruta no encontrada
        else:
            self.send_response(404)
            self.end_headers()


    #APIS PUT 
    def do_PUT(self):
        #Actualizar usuario
        if self.path == "/users/update":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            user_id = data.get("id_usuario")
            correo = data.get("correo")
            nombre = data.get("nombre")

            if not user_id or not correo or not nombre:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = putController.usuario_update(user_id,correo,nombre)
            self.enviar_mensaje(mensaje)

        #Actualizar restaurante
        if self.path == "/restaurante/update":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            restaurante_id = data.get("id_restaurante")
            nombre = data.get("nombre")

            if not restaurante_id or not nombre:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = putController.restaurante_update(restaurante_id, nombre)
            self.enviar_mensaje(mensaje)

        #Actualizar menu
        elif self.path == "/menu/update":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            menu_id = data.get("id_menu")
            descripcion = data.get("descripcion")

            if not menu_id or not descripcion:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = putController.modificar_menu(menu_id, descripcion)
            self.enviar_mensaje(mensaje)
            return 
        
        #Actualizar producto
        elif self.path == "/producto/update":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            producto_id = data.get("id_producto")
            nombre = data.get("nombre")
            precio = data.get("precio")

            if not producto_id or not nombre or not precio:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = putController.modificar_producto(producto_id, nombre, precio)
            self.enviar_mensaje(mensaje)
            return 
        
        #Actualizar pedido
        elif self.path == "/pedido/update":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_pedido = data.get("id_pedido")
                estado = data.get("estado")
                
                # Verificar que los datos estan presentes
                if not id_pedido or not estado:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = putController.modificar_pedido(id_pedido, estado)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return

        #Ruta no encontrada
        else:
            self.send_response(404)
            self.end_headers()
           
    

    #APIS DELETE Y SUS METODOS 
    def do_DELETE(self):
        #Eliminar Usuario
        if self.path == "/users/delete":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            usuario_id = data.get("id_usuario")

            if not usuario_id:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = deleteController.eliminar_usuario(usuario_id)
            self.enviar_mensaje(mensaje)
            return
            return
        #Eliminar Restaurante
        if self.path == "/restaurante/delete":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            restaurante_id = data.get("id_restaurante")

            if not restaurante_id:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = deleteController.eliminar_restaurante(restaurante_id)
            self.enviar_mensaje(mensaje)
            return
        
        #Eliminar mesas
        elif self.path == "/restaurante/mesas/delete":
            # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            mesa_id = data.get("id_mesa")

            if not mesa_id:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = deleteController.eliminar_mesa(mesa_id)
            self.enviar_mensaje(mensaje)
            return  

        #Eliminar menu
        elif self.path == "/menu/delete":
             # Leer los datos JSON de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Leer el JSON recibido
            data = json.loads(post_data)  # Convertir JSON a diccionario
            
            # Obtener los datos necesarios
            menu_id = data.get("id_menu")

            if not menu_id:
                self.enviar_mensaje("Error: Faltan campos requeridos")
                return
        
            mensaje = deleteController.eliminar_menu(menu_id)
            self.enviar_mensaje(mensaje)
            return  
        
        #Eliminar vinculo Restaurante Menu
        elif self.path == "/menu/restaurante/delete":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_menu = data.get("id_menu")
                id_restaurante = data.get("id_restaurante")
                
                # Verificar que el restauranteid está presente
                if not id_menu or not id_restaurante:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = deleteController.eliminar_menu_restaurante(id_menu, id_restaurante)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return

        #Eliminar producto
        elif self.path == "/producto/delete":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_producto = data.get("id_producto")
                
                # Verificar que el restauranteid está presente
                if not id_producto:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = deleteController.eliminar_producto(id_producto)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return 

        #Cancelar reserva
        elif self.path == "/reserva/delete":
            content_length = int(self.headers['Content-Length'])  # Obtener el tamaño del contenido
            post_data = self.rfile.read(content_length)  # Leer los datos del cuerpo de la solicitud
            
            try:
                # Convertir el JSON recibido a un diccionario
                data = json.loads(post_data)
                
                # Extraer el restauranteid del JSON
                id_reserva = data.get("id_reserva")
                
                # Verificar que el restauranteid está presente
                if not id_reserva:
                    self.enviar_mensaje("Error: Falta alguno de los datos")
                    return
                
                # Llamar a la función consultar_productos con el restauranteid
                mensaje = deleteController.eliminar_reserva(id_reserva)
                self.enviar_mensaje(mensaje)
            except json.JSONDecodeError:
                # Manejar el caso en que el JSON no es válido
                self.enviar_mensaje("Error: el cuerpo de la solicitud no es un JSON valido")
            return 
        
        #Ruta no encontrada
        else:
            self.send_response(404)
            self.end_headers()


    #Metodos generales
    def enviar_mensaje(self, mensaje):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(mensaje.encode("utf-8"))
        
    