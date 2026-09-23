import os
import unittest

import database
from database import (
    BASE_DIR,
    actualizar_libro,
    actualizar_prestamo,
    actualizar_socio,
    crear_tablas,
    eliminar_libro,
    eliminar_prestamo,
    eliminar_socio,
    insertar_libro,
    insertar_prestamo,
    insertar_socio,
    listar_libros,
    listar_prestamos,
    listar_socios,
)

DB_NAME = os.path.join(BASE_DIR, "test_biblioteca.db")


class BibliotecaCrudTests(unittest.TestCase):
    def setUp(self):
        database.DB_NAME = DB_NAME
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        crear_tablas()

    def tearDown(self):
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        database.DB_NAME = os.path.join(BASE_DIR, "biblioteca.db")

    def test_socio_crud(self):
        insertar_socio("12345678", "Ana", "García", "11223344", "ana@mail.com")
        socios = listar_socios()
        self.assertEqual(len(socios), 1)
        self.assertEqual(socios[0][1], "Ana")

        actualizar_socio("12345678", "Ana", "García Díaz", "11223344", "ana.nueva@mail.com")
        socios = listar_socios()
        self.assertEqual(socios[0][2], "García Díaz")
        self.assertEqual(socios[0][4], "ana.nueva@mail.com")

        eliminar_socio("12345678")
        self.assertEqual(listar_socios(), [])

    def test_libro_crud(self):
        insertar_libro("L-001", "Clean Code", "Robert C. Martin", "Pearson", 2008, "disponible")
        libros = listar_libros()
        self.assertEqual(len(libros), 1)
        self.assertEqual(libros[0][1], "Clean Code")

        actualizar_libro("L-001", "Clean Code", "Robert C. Martin", "Prentice Hall", 2011, "prestado")
        libros = listar_libros()
        self.assertEqual(libros[0][3], "Prentice Hall")
        self.assertEqual(libros[0][5], "prestado")

        eliminar_libro("L-001")
        self.assertEqual(listar_libros(), [])

    def test_prestamo_crud(self):
        insertar_socio("12345678", "Ana", "García", "11223344", "ana@mail.com")
        insertar_libro("L-001", "Clean Code", "Robert C. Martin", "Pearson", 2008, "disponible")

        insertar_prestamo("12345678", "L-001", "2026-09-18", "2026-09-25")
        prestamos = listar_prestamos()
        self.assertEqual(len(prestamos), 1)
        self.assertEqual(prestamos[0][1], "12345678")
        self.assertEqual(prestamos[0][2], "L-001")

        actualizar_prestamo(1, "12345678", "L-001", "2026-09-18", "2026-09-26", "2026-09-20")
        prestamos = listar_prestamos()
        self.assertEqual(prestamos[0][4], "2026-09-26")
        self.assertEqual(prestamos[0][5], "2026-09-20")

        eliminar_prestamo(1)
        self.assertEqual(listar_prestamos(), [])


if __name__ == "__main__":
    unittest.main()
