CREATE OR REPLACE FUNCTION actualizar_usuario(
    p_id_usuario INT,
    p_correo VARCHAR(100),
    p_nombre VARCHAR(100)
) RETURNS VOID AS $$
BEGIN
    UPDATE Usuario
    SET Correo = COALESCE(p_correo, Correo),
        Nombre = COALESCE(p_nombre, Nombre)
    WHERE IdUsuario = p_id_usuario;
END;
$$ LANGUAGE plpgsql;

