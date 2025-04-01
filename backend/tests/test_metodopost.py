import pytest
import json
from unittest.mock import MagicMock, patch
from apis.metodopost import controllerpost

@pytest.fixture
def mock_database():
    with patch("controller.databasecontroller.databaseController") as mock_db:
        mock_instance = mock_db.return_value
        mock_instance.conectar_base_datos.return_value.cursor.return_value = MagicMock()
        yield mock_instance

@pytest.fixture
def controller(mock_database):
    return controllerpost()

def test_agregar_usuario(controller, mock_database):
    mock_cursor = mock_database.conectar_base_datos.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [1]
    
    result = controller.agregar_usuario("auth0_123", "correo@test.com", "Test User")
    assert result == 1

def test_registrar_restaurante(controller, mock_database):
    mock_cursor = mock_database.conectar_base_datos.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [10]
    
    result = controller.registrar_restaurante("Restaurante Prueba")
    assert json.loads(result) == {"id_restaurante": 10}

def test_registrar_mesa_restaurante(controller, mock_database):
    result = controller.registrar_mesa_restaurante(1, 5)
    assert json.loads(result) == {"Message": "Mesa agregada"}

def test_crear_menu(controller, mock_database):
    mock_cursor = mock_database.conectar_base_datos.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [20]
    
    result = controller.crear_menu("Menu de Prueba")
    assert json.loads(result) == {"id_menu": 20}

def test_vincular_menu_restaurante(controller, mock_database):
    result = controller.vincular_menu_restaurante(20, 1)
    assert result == "Menu vinculado a restaurante"

def test_crear_pedido(controller, mock_database):
    mock_cursor = mock_database.conectar_base_datos.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [30]
    
    result = controller.crear_pedido(1, "pendiente", 2)
    assert json.loads(result) == {"id_pedido": 30}

def test_agregar_producto(controller, mock_database):
    mock_cursor = mock_database.conectar_base_datos.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [40]
    
    result = controller.agregar_producto(20, "Producto de Prueba", 99.99)
    assert json.loads(result) == {"id_producto": 40}

def test_agregar_producto_pedido(controller, mock_database):
    result = controller.agregar_producto_pedido(40, 30, 2)
    assert json.loads(result) == {"Message": "Producto agregado"}

def test_crear_reserva(controller, mock_database):
    mock_cursor = mock_database.conectar_base_datos.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [50]
    
    result = controller.crear_reserva(5, 1, "2025-01-01 12:00:00")
    assert json.loads(result) == {"idReserva": 50}