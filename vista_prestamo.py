import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    actualizar_prestamo,
    eliminar_prestamo,
    insertar_prestamo,
    listar_prestamos,
)


class PrestamoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.nro_seleccionado = None

        self.configure(style="App.TFrame")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_formulario()
        self._crear_tabla()
        self._crear_botones()
        self.listar_prestamos()

    def _crear_formulario(self):
        frame = ttk.LabelFrame(self, text="Datos del préstamo")
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        ttk.Label(frame, text="DNI socio:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.entry_dni = ttk.Entry(frame, width=22)
        self.entry_dni.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(frame, text="Código libro:", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=6)
        self.entry_codigo = ttk.Entry(frame, width=22)
        self.entry_codigo.grid(row=0, column=3, padx=5, pady=6)

        ttk.Label(frame, text="Fecha préstamo:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=6)
        self.entry_fecha_prestamo = ttk.Entry(frame, width=22)
        self.entry_fecha_prestamo.grid(row=1, column=1, padx=5, pady=6)

        ttk.Label(frame, text="Fecha devolución estimada:", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky="w", padx=5, pady=6)
        self.entry_fecha_devolucion = ttk.Entry(frame, width=22)
        self.entry_fecha_devolucion.grid(row=1, column=3, padx=5, pady=6)

        ttk.Label(frame, text="Fecha devolución real:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=6)
        self.entry_fecha_real = ttk.Entry(frame, width=22)
        self.entry_fecha_real.grid(row=2, column=1, padx=5, pady=6)

    def _crear_tabla(self):
        columnas = ("nro_prestamo", "dni_socio", "codigo_libro", "fecha_prestamo", "fecha_devolucion_estimada", "fecha_devolucion_real")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col.replace("_", " ").capitalize())
            self.tabla.column(col, width=130)
        self.tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 6))
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def _crear_botones(self):
        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, pady=(0, 10))

        ttk.Button(frame, text="Agregar", command=self.agregar_prestamo, style="Accent.TButton").grid(row=0, column=0, padx=6)
        ttk.Button(frame, text="Modificar", command=self.modificar_prestamo).grid(row=0, column=1, padx=6)
        ttk.Button(frame, text="Eliminar", command=self.eliminar_prestamo).grid(row=0, column=2, padx=6)
        ttk.Button(frame, text="Limpiar", command=self.limpiar_formulario).grid(row=0, column=3, padx=6)

    def listar_prestamos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for prestamo in listar_prestamos():
            self.tabla.insert("", "end", values=prestamo)

    def agregar_prestamo(self):
        dni = self.entry_dni.get().strip()
        codigo = self.entry_codigo.get().strip()
        fecha_prestamo = self.entry_fecha_prestamo.get().strip()
        fecha_devolucion = self.entry_fecha_devolucion.get().strip()
        fecha_real = self.entry_fecha_real.get().strip() or None

        if not dni or not codigo or not fecha_prestamo or not fecha_devolucion:
            messagebox.showwarning("Datos incompletos", "DNI, código, fechas de préstamo y devolución son obligatorios.")
            return

        try:
            insertar_prestamo(dni, codigo, fecha_prestamo, fecha_devolucion, fecha_real)
            self.listar_prestamos()
            self.limpiar_formulario()
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo registrar el préstamo: {exc}")

    def modificar_prestamo(self):
        if not self.nro_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un préstamo de la tabla para modificar.")
            return

        dni = self.entry_dni.get().strip()
        codigo = self.entry_codigo.get().strip()
        fecha_prestamo = self.entry_fecha_prestamo.get().strip()
        fecha_devolucion = self.entry_fecha_devolucion.get().strip()
        fecha_real = self.entry_fecha_real.get().strip() or None

        if not dni or not codigo or not fecha_prestamo or not fecha_devolucion:
            messagebox.showwarning("Datos incompletos", "DNI, código, fechas de préstamo y devolución son obligatorios.")
            return

        actualizar_prestamo(self.nro_seleccionado, dni, codigo, fecha_prestamo, fecha_devolucion, fecha_real)
        self.listar_prestamos()
        self.limpiar_formulario()

    def eliminar_prestamo(self):
        if not self.nro_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un préstamo de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el préstamo número {self.nro_seleccionado}?")
        if not confirmar:
            return

        eliminar_prestamo(self.nro_seleccionado)
        self.listar_prestamos()
        self.limpiar_formulario()

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        self.nro_seleccionado = valores[0]

        self.entry_dni.delete(0, tk.END)
        self.entry_dni.insert(0, valores[1])

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, valores[2])

        self.entry_fecha_prestamo.delete(0, tk.END)
        self.entry_fecha_prestamo.insert(0, valores[3])

        self.entry_fecha_devolucion.delete(0, tk.END)
        self.entry_fecha_devolucion.insert(0, valores[4])

        self.entry_fecha_real.delete(0, tk.END)
        self.entry_fecha_real.insert(0, valores[5] or "")

    def limpiar_formulario(self):
        self.nro_seleccionado = None
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
        for entry in (
            self.entry_dni,
            self.entry_codigo,
            self.entry_fecha_prestamo,
            self.entry_fecha_devolucion,
            self.entry_fecha_real,
        ):
            entry.delete(0, tk.END)
