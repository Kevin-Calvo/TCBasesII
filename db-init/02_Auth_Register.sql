CREATE OR REPLACE FUNCTION agregar_usuario(
    p_auth0id VARCHAR(50),
    p_correo VARCHAR(100),
    p_nombre VARCHAR(100)
) RETURNS INT AS $$
DECLARE
    v_id_usuario INT;
BEGIN
    -- Insertar el usuario y obtener el ID generado
    INSERT INTO Usuario (Auth0Id, Correo, Nombre)
    VALUES (p_auth0id, p_correo, p_nombre)
    RETURNING IdUsuario INTO v_id_usuario;

    -- Retornar el ID del usuario insertado
    RETURN v_id_usuario;
END;
$$ LANGUAGE plpgsql;




