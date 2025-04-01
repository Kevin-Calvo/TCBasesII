import pytest
import json
from unittest.mock import patch, MagicMock
from apis.metodoget import controllerget

@pytest.fixture
def mock_db_connection():
    with patch("controller.databasecontroller.databaseController.conectar_base_datos") as mock_connect:
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        yield mock_connection

@pytest.fixture
def controller():
    return controllerget()

def test_obtener_usuario_por_id_usuario_existente(controller, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [("Juan Perez", "juan@example.com")]

    resultado = controller.obtener_usuario_por_id(1)
    assert resultado == "Nombre: Juan Perez, Correo: juan@example.com"

def test_obtener_usuario_por_id_no_encontrado(controller, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = []

    resultado = controller.obtener_usuario_por_id(2)
    assert resultado == "Usuario no encontrado"

def test_consultar_restaurantes(controller, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [(1, "Restaurante A"), (2, "Restaurante B")]

    resultado = json.loads(controller.consultar_restaurantes())
    assert resultado == [
        {"id_restaurante": 1, "nombre": "Restaurante A"},
        {"id_restaurante": 2, "nombre": "Restaurante B"}
    ]

def test_consultar_mesas_por_restaurante(controller, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [("Restaurante A", 101), ("Restaurante A", 102)]

    post_data = json.dumps({"id_restaurante": 1})
    resultado = json.loads(controller.consultar_mesas_por_restaurante(post_data))
    assert resultado == [
        {"restaurante": "Restaurante A", "id_mesa": 101},
        {"restaurante": "Restaurante A", "id_mesa": 102}
    ]

def test_consultar_productos_por_restaurante(controller, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [
        ("Producto A", 1, "Menu 1", 10, 1001, "Producto A", 15.50),
        ("Producto B", 1, "Menu 1", 10, 1002, "Producto B", 20.00)
    ]

    resultado = json.loads(controller.consultar_productos_por_restaurante(1))
    assert resultado == {
        "id_restaurante": 1,
        "productos": [
            {"menu": "Menu 1", "id_menu": 10, "id_producto": 1001, "nombre": "Producto A", "precio": 15.50},
            {"menu": "Menu 1", "id_menu": 10, "id_producto": 1002, "nombre": "Producto B", "precio": 20.00}
        ]
    }

def test_obtener_pedido(controller, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [
        ("Producto A", 2, 15.00, 30.00, 50.00, "Usuario X", "Enviado")
    ]

    resultado = json.loads(controller.obtener_pedido(1001))
    assert resultado == [
        {
            "NombreProducto": "Producto A",
            "Cantidad": 2,
            "PrecioProducto": 15.00,
            "TotalPorProducto": 30.00,
            "TotalPedido": 50.00,
            "NombreUsuario": "Usuario X",
            "EstadoPedido": "Enviado"
        }
    ]

def test_consultar_reservas_por_usuario(controller, mock_db_connection):
    mock_cursor = mock_db_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [
        ("Restaurante A", 5, "2024-03-31 19:00:00")
    ]

    resultado = json.loads(controller.consultar_reservas_por_usuario(1))
    assert resultado == [
        {
            "NombreRestaurante": "Restaurante A",
            "IdMesa": 5,
            "FechaReserva": "2024-03-31 19:00:00"
        }
    ]