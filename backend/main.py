from http.server import HTTPServer
from apis.api_controller import ControllerAPI

def run(server_class=HTTPServer, handler_class=ControllerAPI, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor corriendo en http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
