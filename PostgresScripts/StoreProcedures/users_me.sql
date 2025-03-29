CREATE OR REPLACE FUNCTION obtener_usuario_por_id(
    p_id_usuario INT
) RETURNS TABLE (Nombre VARCHAR(100), Correo VARCHAR(100)) AS $$
BEGIN
    RETURN QUERY 
    SELECT u.Nombre, u.Correo
    FROM Usuario u
    WHERE u.IdUsuario = p_id_usuario;
END;
$$ LANGUAGE plpgsql;


