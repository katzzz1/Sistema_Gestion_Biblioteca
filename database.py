import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "biblioteca.db")


def crear_conexion():
    """Devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME, timeout=30)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def crear_tablas():
    """Crea las tablas Socio, Libro y Prestamo si no existen, según el DER."""
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS socio (
            dni TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            email TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS libro (
            codigo_libro TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editorial TEXT,
            anio_publicacion INTEGER,
            estado TEXT NOT NULL DEFAULT 'disponible'
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prestamo (
            nro_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
            dni_socio TEXT NOT NULL,
            codigo_libro TEXT NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion_estimada TEXT NOT NULL,
            fecha_devolucion_real TEXT,
            FOREIGN KEY (dni_socio) REFERENCES socio (dni),
            FOREIGN KEY (codigo_libro) REFERENCES libro (codigo_libro)
        )
        """
    )

    conn.commit()
    conn.close()


#  socio CRUD 
def insertar_socio(dni, nombre, apellido, telefono=None, email=""):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO socio (dni, nombre, apellido, telefono, email) VALUES (?, ?, ?, ?, ?)",
        (dni, nombre, apellido, telefono, email),
    )
    conn.commit()
    conn.close()


def listar_socios():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT dni, nombre, apellido, telefono, email FROM socio ORDER BY apellido, nombre")
    datos = cursor.fetchall()
    conn.close()
    return datos


def actualizar_socio(dni, nombre, apellido, telefono=None, email=""):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE socio SET nombre=?, apellido=?, telefono=?, email=? WHERE dni=?",
        (nombre, apellido, telefono, email, dni),
    )
    conn.commit()
    conn.close()


def eliminar_socio(dni):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM socio WHERE dni=?", (dni,))
    conn.commit()
    conn.close()


# libro CRUD 
def insertar_libro(codigo_libro, titulo, autor, editorial=None, anio_publicacion=None, estado="disponible"):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO libro (codigo_libro, titulo, autor, editorial, anio_publicacion, estado) VALUES (?, ?, ?, ?, ?, ?)",
        (codigo_libro, titulo, autor, editorial, anio_publicacion, estado),
    )
    conn.commit()
    conn.close()


def listar_libros():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codigo_libro, titulo, autor, editorial, anio_publicacion, estado FROM libro ORDER BY titulo"
    )
    datos = cursor.fetchall()
    conn.close()
    return datos


def actualizar_libro(codigo_libro, titulo, autor, editorial=None, anio_publicacion=None, estado="disponible"):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE libro SET titulo=?, autor=?, editorial=?, anio_publicacion=?, estado=? WHERE codigo_libro=?",
        (titulo, autor, editorial, anio_publicacion, estado, codigo_libro),
    )
    conn.commit()
    conn.close()


def eliminar_libro(codigo_libro):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libro WHERE codigo_libro=?", (codigo_libro,))
    conn.commit()
    conn.close()


# prestamo CRUD 
def insertar_prestamo(dni_socio, codigo_libro, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real=None):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prestamo (dni_socio, codigo_libro, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real) VALUES (?, ?, ?, ?, ?)",
        (dni_socio, codigo_libro, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real),
    )
    conn.commit()
    conn.close()


def listar_prestamos():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nro_prestamo, dni_socio, codigo_libro, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real FROM prestamo ORDER BY fecha_prestamo DESC, nro_prestamo DESC"
    )
    datos = cursor.fetchall()
    conn.close()
    return datos


def actualizar_prestamo(nro_prestamo, dni_socio, codigo_libro, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real=None):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE prestamo SET dni_socio=?, codigo_libro=?, fecha_prestamo=?, fecha_devolucion_estimada=?, fecha_devolucion_real=? WHERE nro_prestamo=?",
        (dni_socio, codigo_libro, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real, nro_prestamo),
    )
    conn.commit()
    conn.close()


def eliminar_prestamo(nro_prestamo):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prestamo WHERE nro_prestamo=?", (nro_prestamo,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos creada correctamente.")