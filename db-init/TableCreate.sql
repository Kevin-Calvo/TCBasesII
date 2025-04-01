-- Crear la base de datos
CREATE DATABASE RESTAURANTE;


-- Crear la tabla Restaurante
CREATE TABLE Restaurante (
    IdRestaurante SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL
);

-- Crear la tabla Menu
CREATE TABLE Menu (
    IdMenu SERIAL PRIMARY KEY,
    Descripcion TEXT NOT NULL
);

-- Crear la tabla Producto
CREATE TABLE Producto (
    IdProducto SERIAL PRIMARY KEY,
    IdMenu INT NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    Precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (IdMenu) REFERENCES Menu(IdMenu) ON DELETE CASCADE
);

-- Crear la tabla Mesa
CREATE TABLE Mesa (
    IdMesa PRIMARY KEY,
    IdRestaurante INT NOT NULL,
    FOREIGN KEY (IdRestaurante) REFERENCES Restaurante(IdRestaurante) ON DELETE CASCADE
);


-- Crear la tabla Usuario (Con información mínima para Auth0)
CREATE TABLE Usuario (
    IdUsuario SERIAL PRIMARY KEY,
    Auth0Id VARCHAR(50) UNIQUE NOT NULL, -- ID del usuario en Auth0
    Correo VARCHAR(100) UNIQUE NOT NULL, -- Email único del usuario
    Nombre VARCHAR(100) -- Nombre opcional
);


-- Crear la tabla Reserva
CREATE TABLE Reserva (
    IdReserva SERIAL PRIMARY KEY,
    IdMesa INT NOT NULL,
    IdUsuario INT NOT NULL,
    FechaReserva TIMESTAMP NOT NULL,
    FOREIGN KEY (IdMesa) REFERENCES Mesa(IdMesa) ON DELETE CASCADE,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario) ON DELETE CASCADE,
    CONSTRAINT unique_reservation UNIQUE (FechaReserva, IdMesa)
);

-- Crear la tabla Pedido
CREATE TABLE Pedido (
    IdPedido SERIAL PRIMARY KEY,
    IdUsuario INT NOT NULL,
    Estado VARCHAR(50) CHECK (Estado IN ('Pendiente', 'Preparando', 'Entregado', 'Cancelado', 'Recoge')) NOT NULL,
    IdRestaurante INT NOT NULL,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario) ON DELETE CASCADE,
    FOREIGN KEY (IdRestaurante) REFERENCES Restaurante(IdRestaurante) ON DELETE CASCADE
);


-- Crear la tabla PedidoProducto (Relación entre Pedido y Producto)
CREATE TABLE PedidoProducto (
    IdPedido INT NOT NULL,
    IdProducto INT NOT NULL,
    Cantidad INT not null,
    PRIMARY KEY (IdPedido, IdProducto),
    FOREIGN KEY (IdPedido) REFERENCES Pedido(IdPedido) ON DELETE CASCADE,
    FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto) ON DELETE CASCADE
);

-- Crear la tabla RestauranteMenu (Relación entre Restaurante y Menu)
CREATE TABLE RestauranteMenu (
    IdRestauranteMenu SERIAL PRIMARY KEY,
    IdRestaurante INT NOT NULL,
    IdMenu INT NOT NULL,
    FOREIGN KEY (IdRestaurante) REFERENCES Restaurante(IdRestaurante) ON DELETE CASCADE,
    FOREIGN KEY (IdMenu) REFERENCES Menu(IdMenu) ON DELETE CASCADE
);









