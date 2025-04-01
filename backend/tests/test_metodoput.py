import pytest
import json
from unittest.mock import MagicMock, patch
from apis.metodoput import controllerput

@pytest.fixture
def mock_db():
    with patch('controller.databasecontroller.databaseController') as mock_db_class:
        mock_db_instance = mock_db_class.return_value
        mock_db_instance.conectar_base_datos.return_value = MagicMock()
        yield mock_db_instance

@pytest.fixture
def controller(mock_db):
    return controllerput()

def test_usuario_update_success(controller, mock_db):
    mock_conn = mock_db.conectar_base_datos.return_value
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    
    result = controller.usuario_update(1, 'correo@example.com', 'Nuevo Nombre')
    
    mock_cursor.callproc.assert_called_once_with('actualizar_usuario', [1, 'correo@example.com', 'Nuevo Nombre'])
    assert json.loads(result) == {"message": "Usuario actualizado con éxito"}

def test_restaurante_update_success(controller, mock_db):
    mock_conn = mock_db.conectar_base_datos.return_value
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    
    result = controller.restaurante_update(1, 'Nuevo Restaurante')
    
    mock_cursor.callproc.assert_called_once_with('modificar_restaurante', [1, 'Nuevo Restaurante'])
    assert json.loads(result) == {"message": "Restaurante actualizado con éxito"}

def test_modificar_menu_success(controller, mock_db):
    mock_conn = mock_db.conectar_base_datos.return_value
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    
    result = controller.modificar_menu(1, 'Nueva Descripción')
    
    mock_cursor.callproc.assert_called_once_with('modificar_menu', [1, 'Nueva Descripción'])
    assert json.loads(result) == {"message": "Modificación con éxito"}

def test_modificar_pedido_success(controller, mock_db):
    mock_conn = mock_db.conectar_base_datos.return_value
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    
    result = controller.modificar_pedido(1, 'Enviado')
    
    mock_cursor.callproc.assert_called_once_with('modificar_estado_pedido', [1, 'Enviado'])
    assert json.loads(result) == {"message": "Modificación con éxito"}

def test_modificar_producto_success(controller, mock_db):
    mock_conn = mock_db.conectar_base_datos.return_value
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    
    result = controller.modificar_producto(1, 'Nuevo Producto', 10.99)
    
    mock_cursor.callproc.assert_called_once_with('modificar_producto', [1, 'Nuevo Producto', 10.99])
    assert json.loads(result) == {"message": "Modificación con éxito"}

def test_usuario_update_db_connection_error(controller, mock_db):
    mock_db.conectar_base_datos.return_value = None
    
    result = controller.usuario_update(1, 'correo@example.com', 'Nuevo Nombre')
    assert json.loads(result) == {"error": "Error de conexión a la base de datos"}

def test_usuario_update_exception(controller, mock_db):
    mock_conn = mock_db.conectar_base_datos.return_value
    mock_conn.cursor.side_effect = Exception("Database error")
    
    result = controller.usuario_update(1, 'correo@example.com', 'Nuevo Nombre')
    assert json.loads(result) == {"error": "Database error"}