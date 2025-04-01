CREATE OR REPLACE FUNCTION crear_menu(
    p_descripcion TEXT
) RETURNS INT AS $$
DECLARE
    v_id_menu INT;
BEGIN
    -- Insertar el nuevo menú y obtener el ID generado
    INSERT INTO Menu (Descripcion)
    VALUES (p_descripcion)
    RETURNING IdMenu INTO v_id_menu;

    -- Retornar el ID del nuevo menú creado
    RETURN v_id_menu;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION modificar_menu(
    p_id_menu INT,
    p_descripcion TEXT
) RETURNS VOID AS $$
BEGIN
    UPDATE Menu
    SET Descripcion = p_descripcion
    WHERE IdMenu = p_id_menu;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION consultar_menus()
RETURNS TABLE(id_menu INT, descripcion TEXT) AS $$
BEGIN
    RETURN QUERY SELECT Menu.IdMenu, Menu.Descripcion FROM Menu;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_menu(
    p_id_menu INT
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Menu WHERE IdMenu = p_id_menu;
END;
$$ LANGUAGE plpgsql;

create or replace function asociar_menu_restaurante(
	p_id_restaurante INT,
	p_id_menu INT
) returns VOID as $$
begin
	insert into RestauranteMenu (IdRestaurante, IdMenu)
	values (p_id_restaurante, p_id_menu);
end;
$$ language plpgsql;

create or replace function eliminar_menu_restaurante(
	p_id_restaurante INT,
	p_id_menu INT
) returns VOID as $$
begin
	DELETE FROM RestauranteMenu 
	WHERE IdRestaurante = p_id_restaurante AND IdMenu = p_id_menu;
end;
$$ language plpgsql;










