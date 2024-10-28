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

-- Tabla de Contenidos
CREATE TABLE Contenidos (
    id_contenido INT AUTO_INCREMENT PRIMARY KEY,
    id_materia INT,
    tipo_contenido ENUM('teórico', 'práctico'),
    descripcion TEXT,
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
);

-- Tabla de Evaluaciones
CREATE TABLE Evaluaciones (
    id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    id_materia INT,
    fecha DATE,
    tipo_evaluacion ENUM('examen', 'tarea', 'proyecto'),
    descripcion TEXT,
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
);

-- Modificar tabla de Calendario para relacionarla con Materias
CREATE TABLE Calendario (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_materia INT NOT NULL,
    fecha DATE,
    evento VARCHAR(100),
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
);

-- Insertar Materias
INSERT INTO Materias (nombre_materia, nombre_profesor) VALUES
('Programación I', "Hector Garcia"),
('Informatica Aplicada I', "Barrios Christian"),
('Redes y Telecomucaciones', "Barrios Christian");

INSERT INTO Contenidos (id_materia, tipo_contenido, descripcion) VALUES
(1, 'teórico', 'Introducción a la Programación.'),       
(2, 'teórico', 'Introducción a la Informática Aplicada.'), 
(3, 'teórico', 'Fundamentos de Redes y Telecomunicaciones.');

-- Insertar Evaluaciones
INSERT INTO Evaluaciones (id_materia, fecha, tipo_evaluacion, descripcion) VALUES
(1, '2024-11-15', 'examen', 'Examen final de Programación I.'),
(2, '2024-12-20', 'proyecto', 'Proyecto final de Programación I.')



INSERT INTO Usuario(nombre, apellido, email, contraseña, dni) VALUES
('Christian', 'Barrios', 'profe@gmail.com', 'profe12345', '12345678'),
('Matias', 'Guzman', 'programacion@gmail.com', 'alumno12345', '46587536')

-- Insertar Roles
INSERT INTO Roles (id_usuario, rol_usuario) VALUES
(1, 'Profesor'),
(2, 'Estudiante')



SELECT Usuario.nombre, Usuario.apellido, Roles.rol_usuario
FROM Usuario
INNER JOIN Roles ON Usuario.id_usuario = Roles.id_usuario;



CREATE USER '51702027'@'localhost' IDENTIFIED BY 'nicolas07.';
GRANT ALL PRIVILEGES ON AulaVirtual.* TO '51702027'@'localhost';
FLUSH PRIVILEGES; esta