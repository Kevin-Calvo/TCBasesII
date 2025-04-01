	CREATE OR REPLACE FUNCTION crear_reserva(
	    p_idmesa INT,
	    p_idusuario INT,
	    p_fechareserva TIMESTAMP
	) RETURNS INT AS $$
	DECLARE
	    v_id_reserva INT;
	BEGIN
	    -- Insertar la nueva reserva y obtener el ID generado
	    INSERT INTO Reserva (IdMesa, IdUsuario, FechaReserva)
	    VALUES (p_idmesa, p_idusuario, p_fechareserva)
	    RETURNING IdReserva INTO v_id_reserva;
	
	    -- Retornar el ID de la nueva reserva creada
	    RETURN v_id_reserva;
	END;
	$$ LANGUAGE plpgsql;


	CREATE OR REPLACE FUNCTION eliminar_reserva(
    p_idreserva INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Reserva WHERE IdReserva = p_idreserva;
END;
$$ LANGUAGE plpgsql;

	
CREATE OR REPLACE FUNCTION consultar_reserva(
    p_idusuario INT
) RETURNS TABLE(Nombre VARCHAR, IdMesa INT, FechaReserva TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT R.Nombre, M.IdMesa, E.FechaReserva
    FROM MESA M
    INNER JOIN RESTAURANTE R ON R.IDRESTAURANTE = M.IDRESTAURANTE
    INNER JOIN RESERVA E ON E.IDMESA = M.IDMESA
    WHERE E.IdUsuario = p_idusuario
    ORDER BY E.FechaReserva DESC;
END;
$$ LANGUAGE plpgsql;



















