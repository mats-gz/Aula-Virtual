-- Active: 1722942989265@@127.0.0.1@3306@AulaVirtual
CREATE DATABASE AulaVirtual

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
