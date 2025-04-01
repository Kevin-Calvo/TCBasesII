CREATE OR REPLACE FUNCTION registrar_restaurante(
    p_nombre VARCHAR(100)
) RETURNS INT AS $$
DECLARE
    v_id_restaurante INT;
BEGIN
    -- Insertar el restaurante y obtener el ID generado
    INSERT INTO Restaurante (Nombre)
    VALUES (p_nombre)
    RETURNING IdRestaurante INTO v_id_restaurante;

    -- Retornar el ID del restaurante insertado
    RETURN v_id_restaurante;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION modificar_restaurante(
    p_id INT,
    p_nombre VARCHAR(100)
) RETURNS VOID AS $$
BEGIN
    UPDATE Restaurante
    SET Nombre = p_nombre
    WHERE IdRestaurante = p_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_restaurante(
    p_id INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Restaurante
    WHERE IdRestaurante = p_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION consultar_restaurante()
RETURNS TABLE (ID INT, Nombre VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT R.IdRestaurante, R.Nombre 
    FROM Restaurante R;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION agregar_mesa(
    p_id_restaurante INT,
    p_id_mesa INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Mesa (IdRestaurante, IdMesa) 
    VALUES (p_id_restaurante, p_id_mesa);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_mesa(
    p_id_mesa INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Mesa 
    WHERE IdMesa = p_id_mesa;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION consultar_mesas_por_restaurante(
    p_id_restaurante INT
) 
RETURNS TABLE(Restaurante VARCHAR(100), id_mesa INT) AS $$
BEGIN
    RETURN QUERY
    SELECT R.Nombre, m.IdMesa
    FROM Mesa m
	INNER JOIN
		Restaurante R ON R.IdRestaurante = M.IdRestaurante
    WHERE m.IdRestaurante = p_id_restaurante;
END;
$$ LANGUAGE plpgsql;

select * from usuario


