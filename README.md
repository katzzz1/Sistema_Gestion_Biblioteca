<<<<<<< HEAD
# Sistema_Gestion_Biblioteca
=======
# Sistema_Gestion_Biblioteca

Repositorio: https://github.com/katzzz1/Sistema_Gestion_Biblioteca

## Descripción del proyecto

Este proyecto es una aplicación de escritorio desarrollada en Python con Tkinter y SQLite para gestionar una biblioteca. Permite administrar socios, libros y préstamos con operaciones CRUD completas: alta, baja, modificación y listado.

El sistema fue diseñado para cumplir con la consigna de un proyecto universitario de análisis y metodología de sistemas, siguiendo un modelo de negocio orientado a la gestión de préstamos de una biblioteca.

## Contexto del sistema

La biblioteca necesita registrar y controlar:

- socios activos,
- libros disponibles y prestados,
- préstamos realizados y sus fechas de devolución,
- datos básicos para mantener un seguimiento ordenado de la actividad.

La aplicación permite centralizar esta información en una base de datos local SQLite, brindando una interfaz simple y funcional para gestionar la operación diaria.

## Funcionalidades principales

- Registro de socios
- Modificación de datos de socios
- Eliminación de socios
- Listado de socios
- Registro de libros
- Modificación de libros
- Eliminación de libros
- Listado de libros
- Registro de préstamos
- Modificación de préstamos
- Eliminación de préstamos
- Listado de préstamos
- Validación de campos obligatorios
- Persistencia en SQLite
- Interfaz gráfica en Tkinter

## Tecnologías utilizadas

- Python
- Tkinter
- SQLite
- unittest

## Estructura del proyecto

```text
Sistema_Gestion_Biblioteca/
├── database.py
├── main.py
├── test_biblioteca.py
├── vista_socio.py
├── vista_libro.py
├── vista_prestamo.py
├── contexto_proyecto_parcial.md
├── biblioteca.db
├── test_biblioteca.db
├── .venv/
├── README.md
└── ...
```

### Descripción de archivos

- `main.py`: punto de entrada principal de la aplicación.
- `database.py`: conexión a SQLite y funciones CRUD para socios, libros y préstamos.
- `vista_socio.py`: interfaz para gestionar socios.
- `vista_libro.py`: interfaz para gestionar libros.
- `vista_prestamo.py`: interfaz para gestionar préstamos.
- `test_biblioteca.py`: pruebas unitarias de validación del CRUD.
- `biblioteca.db`: base de datos real de la aplicación.
- `test_biblioteca.db`: base de datos separada para pruebas.

## Cómo funciona la aplicación

La app abre una ventana principal con pestañas para:

1. Socios
2. Libros
3. Préstamos

Cada pestaña permite:

- completar un formulario,
- agregar un registro,
- seleccionar una fila de la tabla,
- modificar los datos,
- eliminar el registro,
- limpiar el formulario.

Los datos se guardan en SQLite y se muestran en la tabla correspondiente.

## Requisitos

- Python 3.9 o superior
- Windows 10/11 (la interfaz está pensada para Tkinter en Windows)
- Git para clonar el repositorio

## Ejecución correcta

### 1) Clonar el repositorio

```bash
git clone https://github.com/katzzz1/Sistema_Gestion_Biblioteca.git
cd Sistema_Gestion_Biblioteca
```

### 2) Crear un entorno virtual

En PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución por política, usar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3) Ejecutar la aplicación

```powershell
python main.py
```

### 4) Ejecutar pruebas

```powershell
python test_biblioteca.py
```

## Base de datos

La aplicación usa SQLite con una base de datos local persistente.

- Base de uso real: `biblioteca.db`
- Base de pruebas: `test_biblioteca.db`

Esto permite que la aplicación principal no se borre al ejecutar las pruebas y que el entorno de testing quede aislado.

## Observaciones importantes

- No abrir dos instancias de la aplicación a la vez si se quiere evitar bloqueos de SQLite.
- Si aparece un mensaje de base bloqueada, cerrar la ventana y volver a abrir la app.
- Si querés reiniciar la base de datos del sistema, borrar `biblioteca.db` y volver a ejecutar la app para recrearla automáticamente.

## Estado del proyecto

El proyecto está funcional y cuenta con CRUD completo para socios, libros y préstamos. Además, incluye pruebas unitarias para validar la lógica principal.

## Autor

Pardo Katia
>>>>>>> 7fac998 (Primera versión del sistema de biblioteca)
