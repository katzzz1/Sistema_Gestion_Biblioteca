import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from database import crear_conexion, actualizar_socio, eliminar_socio, insertar_socio, listar_socios


class SocioFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.dni_seleccionado = None

        self.configure(style="App.TFrame")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_formulario()
        self._crear_tabla()
        self._crear_botones()
        self.listar_socios()

    def _crear_formulario(self):
        frame = ttk.LabelFrame(self, text="Datos del socio")
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        ttk.Label(frame, text="DNI:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.entry_dni = ttk.Entry(frame, width=22)
        self.entry_dni.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(frame, text="Nombre:", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=6)
        self.entry_nombre = ttk.Entry(frame, width=22)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=6)

        ttk.Label(frame, text="Apellido:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=6)
        self.entry_apellido = ttk.Entry(frame, width=22)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=6)

        ttk.Label(frame, text="Teléfono:", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky="w", padx=5, pady=6)
        self.entry_telefono = ttk.Entry(frame, width=22)
        self.entry_telefono.grid(row=1, column=3, padx=5, pady=6)

        ttk.Label(frame, text="Email:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=6)
        self.entry_email = ttk.Entry(frame, width=22)
        self.entry_email.grid(row=2, column=1, padx=5, pady=6)

    def _crear_tabla(self):
        columnas = ("dni", "nombre", "apellido", "telefono", "email")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120)
        self.tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 6))
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def _crear_botones(self):
        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, pady=(0, 10))

        ttk.Button(frame, text="Agregar", command=self.agregar_socio, style="Accent.TButton").grid(row=0, column=0, padx=6)
        ttk.Button(frame, text="Modificar", command=self.modificar_socio).grid(row=0, column=1, padx=6)
        ttk.Button(frame, text="Eliminar", command=self.eliminar_socio).grid(row=0, column=2, padx=6)
        ttk.Button(frame, text="Limpiar", command=self.limpiar_formulario).grid(row=0, column=3, padx=6)

    def listar_socios(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for socio in listar_socios():
            self.tabla.insert("", "end", values=socio)

    def agregar_socio(self):
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip() or None
        email = self.entry_email.get().strip()

        if not dni or not nombre or not apellido or not email:
            messagebox.showwarning("Datos incompletos", "DNI, nombre, apellido y email son obligatorios.")
            return

        try:
            insertar_socio(dni, nombre, apellido, telefono, email)
            self.listar_socios()
            self.limpiar_formulario()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"Ya existe un socio con DNI {dni}.")

    def modificar_socio(self):
        if not self.dni_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un socio de la tabla para modificar.")
            return

        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip() or None
        email = self.entry_email.get().strip()

        if not nombre or not apellido or not email:
            messagebox.showwarning("Datos incompletos", "Nombre, apellido y email son obligatorios.")
            return

        actualizar_socio(self.dni_seleccionado, nombre, apellido, telefono, email)
        self.listar_socios()
        self.limpiar_formulario()

    def eliminar_socio(self):
        if not self.dni_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un socio de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar al socio con DNI {self.dni_seleccionado}?")
        if not confirmar:
            return

        eliminar_socio(self.dni_seleccionado)
        self.listar_socios()
        self.limpiar_formulario()

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        self.dni_seleccionado = valores[0]

        self.entry_dni.config(state="normal")
        self.entry_dni.delete(0, tk.END)
        self.entry_dni.insert(0, valores[0])
        self.entry_dni.config(state="disabled")

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_apellido.delete(0, tk.END)
        self.entry_apellido.insert(0, valores[2])

        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, valores[3] or "")

        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, valores[4])

    def limpiar_formulario(self):
        self.dni_seleccionado = None
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
        self.entry_dni.config(state="normal")
        for entry in (self.entry_dni, self.entry_nombre, self.entry_apellido, self.entry_telefono, self.entry_email):
            entry.delete(0, tk.END)