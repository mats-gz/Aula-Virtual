-- Active: 1728344941580@@127.0.0.1@3306
CREATE DATABASE AulaVirtual

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


-- Tabla de Cursos
CREATE TABLE Cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso ENUM('Programación', 'Mecánica')
);

-- Tabla de Materias
CREATE TABLE Materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT,
    nombre_materia VARCHAR(100),
    FOREIGN KEY (id_curso) REFERENCES Cursos(id_curso)
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

-- Tabla de Calendario
CREATE TABLE Calendario (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_materia INT,
    fecha DATE,
    evento VARCHAR(100),
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
);


-- Insertar Cursos
INSERT INTO Cursos (nombre_curso) VALUES
('Programación'),
('Mecánica');

-- Insertar Materias
INSERT INTO Materias (id_curso, nombre_materia) VALUES
(1, 'Programación I'),
(2, 'Informatica Aplicada I'),
(3, 'Redes y Telecomucaciones'),
(4, 'Mecánica I'),
(5, 'Elementos de Maquina I'),
(6, 'Diseño Mecanico I');

INSERT INTO Contenidos (id_materia, tipo_contenido, descripcion) VALUES
(1, 'teórico', 'Introducción a la Programación.'),       
(2, 'teórico', 'Introducción a la Informática Aplicada.'), 
(3, 'teórico', 'Fundamentos de Redes y Telecomunicaciones.'), 
(4, 'teórico', 'Introducción a la Mecánica.'),          
(5, 'teórico', 'Conceptos básicos de Elementos de Máquina.'),  
(6, 'teórico', 'Diseño de Componentes Mecánicos.');     

-- Insertar Evaluaciones
INSERT INTO Evaluaciones (id_materia, fecha, tipo_evaluacion, descripcion) VALUES
(1, '2024-11-15', 'examen', 'Examen final de Programación I.'),
(2, '2024-12-20', 'proyecto', 'Proyecto final de Programación I.')


-- Insertar Eventos en el Calendario
INSERT INTO Calendario (id_materia, fecha, evento) VALUES
(1, '2024-11-15', 'Examen de Programación I'),
(2, '2024-12-20', 'Entrega de Mecanica I')


CREATE USER '51702027'@'localhost' IDENTIFIED BY 'nicolas07.';
GRANT ALL PRIVILEGES ON AulaVirtual.* TO '51702027'@'localhost';
FLUSH PRIVILEGES;
