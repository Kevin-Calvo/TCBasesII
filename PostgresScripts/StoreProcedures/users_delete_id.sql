CREATE OR REPLACE FUNCTION eliminar_usuario(
    p_id_usuario INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Usuario  -- Faltaba "FROM"
    WHERE IdUsuario = p_id_usuario;
END;
$$ LANGUAGE plpgsql;




