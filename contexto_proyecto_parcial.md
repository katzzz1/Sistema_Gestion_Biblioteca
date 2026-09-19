# Contexto del proyecto — Primer parcial Análisis y Metodología de Sistemas

## Consigna general
Elegir un proyecto y desarrollar dos partes:
- **Parte 1 (análisis):** Diagrama de Contexto, DFD Nivel 1 (mínimo 3 procesos), Diccionario de Datos, DER (mínimo 3 entidades).
- **Parte 2 (implementación):** sistema en Python con CRUD completo (alta, baja, modificación, listado) para al menos 2 entidades. La base de datos debe corresponderse con el DER de la Parte 1.

## Proyecto elegido
Sistema de gestión de préstamos de una biblioteca.

## Stack elegido para la Parte 2
**Tkinter + SQLite** (interfaz de escritorio).

## Diagrama de Contexto
Sistema: "Sistema de gestión de préstamos de biblioteca", representado como una única unidad.

Entidades externas:
- **Socio**: envía solicitud de préstamo/devolución, recibe confirmación.
- **Bibliotecario**: registra préstamos y devoluciones.
- **Administrador**: da de alta socios y pide reportes.

## DFD Nivel 1
Tres procesos:
- **1.0 Alta de socio**: Administrador → proceso → almacena en D1 Socios.
- **2.0 Alta de libro**: Bibliotecario → proceso → almacena en D2 Libros.
- **3.0 Gestionar préstamo**: Socio solicita préstamo/devolución → el proceso consulta D1 y D2 (valida socio y libro) → registra en D3 Préstamos → confirma al Socio.

Almacenes de datos: D1 Socios, D2 Libros, D3 Préstamos (coinciden con las tres entidades del DER).

## Diccionario de Datos
```
Socio = @dni + nombre + apellido + (telefono) + email
    ** dni: identificador único del socio (clave primaria)

Libro = @codigo_libro + titulo + autor + (editorial) + anio_publicacion + estado
    ** codigo_libro: identificador único del libro (clave primaria)
    ** estado: [disponible | prestado]

Prestamo = @nro_prestamo + dni_socio + codigo_libro + fecha_prestamo +
           fecha_devolucion_estimada + (fecha_devolucion_real)
    ** nro_prestamo: identificador único del préstamo (clave primaria)
    ** dni_socio: referencia al Socio (clave foránea)
    ** codigo_libro: referencia al Libro (clave foránea)
    ** fecha_devolucion_real: vacío hasta que el libro se devuelve
```

## DER (entidades, atributos y relaciones)

**Socio** (dni PK, nombre, apellido, telefono, email)
**Libro** (codigo_libro PK, titulo, autor, editorial, anio_publicacion, estado)
**Prestamo** (nro_prestamo PK, dni_socio FK, codigo_libro FK, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real)

Relaciones:
- Socio (1) — Realiza — Préstamo (N)
- Préstamo (N) — Incluye — Libro (1)

## Próximo paso (donde quedamos)
Empezar la Parte 2: diseñar la base SQLite según este DER y armar la interfaz Tkinter con CRUD completo, como mínimo, para Socio y Libro (Préstamo puede sumarse como tercera pantalla si da el tiempo).
