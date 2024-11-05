-- Active: 1722942989265@@127.0.0.1@3306@AulaVirtual
CREATE DATABASE AulaVirtual;

USE AulaVirtual;


-- Crear tabla USUARIO
CREATE TABLE Usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    dni INT NOT NULL UNIQUE,
    PRIMARY KEY (id_usuario)
);

-- Crear tabla ROLES
CREATE TABLE Roles (
    id_rol INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    rol_usuario VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_rol),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);


-- Tabla de Materias
CREATE TABLE Materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_materia VARCHAR(100),
    nombre_profesor varchar(100) NOT NULL
);

-- Tabla Modulo
CREATE TABLE Modulo (
    id_modulo INT AUTO_INCREMENT PRIMARY KEY,
    id_materia INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia) ON DELETE CASCADE
);

-- Tabla Contenidos
CREATE TABLE Contenido(
    id_contenido INT AUTO_INCREMENT PRIMARY KEY,
    id_modulo INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    archivo_pdf VARCHAR(255),  -- Campo para almacenar el PDF
    FOREIGN KEY (id_modulo) REFERENCES Modulo(id_modulo) ON DELETE CASCADE
)

-- Tabla ContenidoUsuario (relaciona el contenido con el usuario y el estado de completado)
CREATE TABLE ContenidoUsuario (
    id_contUsuario INT AUTO_INCREMENT NOT NULL,
    id_contenido INT NOT NULL,
    id_usuario INT NOT NULL,
    enlace VARCHAR(255),
    completado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id_contUsuario),
    FOREIGN KEY (id_contenido) REFERENCES Contenido(id_contenido) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

-- Modificar tabla de Calendario para relacionarla con Materias
CREATE TABLE Calendario (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_materia INT NOT NULL,
    fecha DATE,
    evento VARCHAR(100),
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
);

-- Insertar ContenidoUsuarios
INSERT INTO ContenidoUsuario (id_contenido, id_usuario, completado) VALUES
(1, 2, TRUE),
(2, 2, FALSE),
(3, 2, FALSE);

INSERT INTO ContenidoUsuario (id_contenido, id_usuario, completado) VALUES
(1, 2),
(2, 2),
(3, 2);

-- Insertar Materias
INSERT INTO Materias (nombre_materia, nombre_profesor) VALUES
('Programación I', "Hector Garcia"),
('Informatica Aplicada I', "Barrios Christian"),
('Redes y Telecomucaciones', "Barrios Christian");

-- Insertar Módulos
INSERT INTO Modulo (id_materia, nombre) VALUES
(1, 'Módulo 1 - Introducción a la Programación'),
(2, 'Módulo 2 - Introducción a la Informática Aplicada'),
(3, 'Módulo 3 - Fundamentos de Redes y Telecomunicaciones');

 
INSERT INTO Contenido (id_modulo, titulo, descripcion, archivo_pdf) VALUES
(1, 'Teórico - Introducción a la Programación con Javascript', 'Hoy veremos una breve introducción a Javascript, sus variables, tipo de datos, entre otros.', 'JavaScript_Guia_ref_rap.pdf'),
(1, 'Teórico - Introducción a React', 'Hoy veremos una breve introducción a React, para que sirve, como usarlo, entre otros', 'Practico1_React.pdf'),
(1, 'Práctico React', 'Hoy haremos nuestro primer práctico con React, les adjunto el archivo.', 'Practico2_React.pdf'),
(1, 'Evaluacion', 'Aquí encontrarás el material para las evaluaciones de los temas vistos.', 'Evaluacion1_React.pdf');


INSERT INTO Usuario(nombre, apellido, email, contraseña, dni) VALUES
('Christian', 'Barrios', 'profe@gmail.com', 'profe12345', '12345678'),
('Matias', 'Guzman', 'programacion@gmail.com', 'alumno12345', '46587536')

-- Insertar Roles
INSERT INTO Roles (id_usuario, rol_usuario) VALUES
(3, 'Profesor'),
(4, 'Estudiante')



SELECT Usuario.nombre, Usuario.apellido, Roles.rol_usuario
FROM Usuario
INNER JOIN Roles ON Usuario.id_usuario = Roles.id_usuario;



CREATE USER '51702027'@'localhost' IDENTIFIED BY 'nicolas07.';
GRANT ALL PRIVILEGES ON AulaVirtual.* TO '51702027'@'localhost';
FLUSH PRIVILEGES; 