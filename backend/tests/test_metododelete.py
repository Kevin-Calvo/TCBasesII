import pytest
from unittest.mock import MagicMock
import json
from controller.databasecontroller import databaseController
from apis.metododelete import controllerdelete

# Crear una instancia de controllerdelete
deleteController = controllerdelete()

# Fixture para simular la conexión a la base de datos
@pytest.fixture
def mock_connection():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_conn

def test_eliminar_usuario(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.return_value = None
    resultado = deleteController.eliminar_usuario(2)
    assert json.loads(resultado)["message"] == "Usuario eliminado con éxito"

def test_eliminar_menu(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.return_value = None
    resultado = deleteController.eliminar_menu(1)
    assert json.loads(resultado)["message"] == "Menu eliminado con éxito"

def test_eliminar_menu_restaurante(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.return_value = None
    resultado = deleteController.eliminar_menu_restaurante(1, 101)
    assert resultado == "Vinculo de menu a restaurante eliminado"

def test_eliminar_producto(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.return_value = None
    resultado = deleteController.eliminar_producto(10)
    assert resultado == "Producto eliminado"

def test_eliminar_restaurante(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.return_value = None
    resultado = deleteController.eliminar_restaurante(5)
    assert resultado == "Restaurante eliminado"

def test_eliminar_mesa(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.return_value = None
    resultado = deleteController.eliminar_mesa(3)
    assert resultado == "Mesa eliminada"

def test_eliminar_reserva(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.return_value = None
    resultado = deleteController.eliminar_reserva(7)
    assert resultado == "Reserva eliminada"

# Tests para simular fallos en la conexión a la base de datos
def test_error_conexion(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=None)
    resultado = deleteController.eliminar_usuario(2)
    assert json.loads(resultado)["error"] == "Error de conexión a la base de datos"

# Tests para simular errores generados por excepciones inesperadas
def test_error_generico(mock_connection):
    deleteController.database.conectar_base_datos = MagicMock(return_value=mock_connection)
    mock_connection.cursor.return_value.__enter__.return_value.callproc.side_effect = Exception("Error inesperado")
    resultado = deleteController.eliminar_producto(10)
    assert json.loads(resultado)["error"] == "Error inesperado"
