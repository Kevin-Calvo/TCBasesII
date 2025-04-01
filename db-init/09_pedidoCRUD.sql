CREATE OR REPLACE FUNCTION insertar_pedido(
    p_idusuario INT,
    p_estado VARCHAR(50),
    p_idrestaurante INT
) 
RETURNS INT AS $$
DECLARE
    v_idpedido INT;
BEGIN
    -- Insertar un nuevo pedido en la tabla Pedido y capturar el IdPedido generado
    INSERT INTO Pedido (IdUsuario, Estado, IdRestaurante)
    VALUES (p_idusuario, p_estado, p_idrestaurante)
    RETURNING IdPedido INTO v_idpedido;

    -- Retornar el IdPedido generado
    RETURN v_idpedido;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION modificar_estado_pedido(
    p_idpedido INT,
    p_estado VARCHAR(50)
) 
RETURNS VOID AS $$
BEGIN
    -- Modificar el estado del pedido en la tabla Pedido
    UPDATE Pedido
    SET Estado = p_estado
    WHERE IdPedido = p_idpedido;
    
    -- Puedes agregar una validación o manejo de errores si el pedido no existe
    IF NOT FOUND THEN
        RAISE EXCEPTION 'El pedido con ID % no existe', p_idpedido;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insertar_pedido_producto(
    p_idpedido INT,
    p_idproducto INT,
    p_cantidad INT
) 
RETURNS VOID AS $$
BEGIN
    -- Insertar un nuevo registro en la tabla PedidoProducto
    INSERT INTO PedidoProducto (IdPedido, IdProducto, Cantidad)
    VALUES (p_idpedido, p_idproducto, p_cantidad);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION mostrar_detalles_pedido(
    p_idpedido INT
) 
RETURNS TABLE (
    NombreProducto VARCHAR,
    Cantidad INT,
    PrecioProducto DECIMAL,
    TotalPorProducto DECIMAL,
    TotalPedido DECIMAL,
    NombreUsuario VARCHAR,
    EstadoPedido VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        prod.Nombre AS NombreProducto,  -- Aquí se debe usar el alias correcto
        pp.Cantidad,
        prod.Precio,
        pp.Cantidad * prod.Precio AS TotalPorProducto,
        -- Calcular el total del pedido sumando el total de cada producto
        (SELECT SUM(pp2.Cantidad * prod2.Precio) 
         FROM PedidoProducto pp2 
         JOIN Producto prod2 ON pp2.IdProducto = prod2.IdProducto
         WHERE pp2.IdPedido = pp.IdPedido) AS TotalPedido,
        u.Nombre AS NombreUsuario,
        p.Estado AS EstadoPedido
    FROM PedidoProducto pp
    JOIN Producto prod ON pp.IdProducto = prod.IdProducto
    JOIN Pedido p ON pp.IdPedido = p.IdPedido
    JOIN Usuario u ON p.IdUsuario = u.IdUsuario
    WHERE pp.IdPedido = p_idpedido;
END;
$$ LANGUAGE plpgsql;







