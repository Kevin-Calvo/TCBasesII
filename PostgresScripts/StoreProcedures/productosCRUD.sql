CREATE OR REPLACE FUNCTION crear_producto(
    p_id_menu INT,
    p_nombre VARCHAR(100),
    p_precio DECIMAL(10,2)
) RETURNS INT AS $$
DECLARE 
    v_id_producto INT;
BEGIN
    INSERT INTO Producto (IdMenu, Nombre, Precio)
    VALUES (p_id_menu, p_nombre, p_precio)
    RETURNING IdProducto INTO v_id_producto;

    RETURN v_id_producto;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION modificar_producto(
    p_id_producto INT,
    p_nombre VARCHAR(100),
    p_precio DECIMAL(10,2)
) RETURNS VOID AS $$
BEGIN
    UPDATE Producto
    SET Nombre = COALESCE(p_nombre, Nombre),
        Precio = COALESCE(p_precio, Precio)
    WHERE IdProducto = p_id_producto;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_producto(
    p_id_producto INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Producto WHERE IdProducto = p_id_producto;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION consultar_productos_por_restaurante(
    p_id_restaurante INT
) 
RETURNS TABLE(restaurante VARCHAR(100), id_restaurante INT, menu VARCHAR(100), id_menu INT, id_producto INT, nombre VARCHAR(100), precio DECIMAL(10,2) ) AS $$
BEGIN
    RETURN QUERY
    SELECT 
		r.Nombre::VARCHAR(100) AS Restaurante,  -- Se asegura de que el tipo sea VARCHAR(100)
		r.IdRestaurante,
		m.Descripcion::VARCHAR(100) AS Menu,    -- Se asegura de que el tipo sea VARCHAR(100)
        p.IdMenu,
        p.IdProducto, 
        p.Nombre, 
        p.Precio
        
    FROM 
        Restaurante r
    INNER JOIN 
        RestauranteMenu rm ON rm.IdRestaurante = r.IdRestaurante
    INNER JOIN 
        Menu m ON m.IdMenu = rm.IdMenu
    INNER JOIN 
        Producto p ON p.IdMenu = m.IdMenu
    WHERE 
        r.IdRestaurante = p_id_restaurante;
END;
$$ LANGUAGE plpgsql;












