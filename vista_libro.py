import tkinter as tk
from tkinter import ttk, messagebox

from database import actualizar_libro, eliminar_libro, insertar_libro, listar_libros


class LibroFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.codigo_seleccionado = None

        self.configure(style="App.TFrame")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_formulario()
        self._crear_tabla()
        self._crear_botones()
        self.listar_libros()

    def _crear_formulario(self):
        frame = ttk.LabelFrame(self, text="Datos del libro")
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        ttk.Label(frame, text="Código:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.entry_codigo = ttk.Entry(frame, width=22)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(frame, text="Título:", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=6)
        self.entry_titulo = ttk.Entry(frame, width=22)
        self.entry_titulo.grid(row=0, column=3, padx=5, pady=6)

        ttk.Label(frame, text="Autor:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=6)
        self.entry_autor = ttk.Entry(frame, width=22)
        self.entry_autor.grid(row=1, column=1, padx=5, pady=6)

        ttk.Label(frame, text="Editorial:", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky="w", padx=5, pady=6)
        self.entry_editorial = ttk.Entry(frame, width=22)
        self.entry_editorial.grid(row=1, column=3, padx=5, pady=6)

        ttk.Label(frame, text="Año publicación:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=6)
        self.entry_anio = ttk.Entry(frame, width=22)
        self.entry_anio.grid(row=2, column=1, padx=5, pady=6)

        ttk.Label(frame, text="Estado:", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, sticky="w", padx=5, pady=6)
        self.estado_var = tk.StringVar(value="disponible")
        self.combo_estado = ttk.Combobox(frame, textvariable=self.estado_var, values=["disponible", "prestado"], state="readonly", width=20)
        self.combo_estado.grid(row=2, column=3, padx=5, pady=6)

    def _crear_tabla(self):
        columnas = ("codigo_libro", "titulo", "autor", "editorial", "anio_publicacion", "estado")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col in columnas:
            titulo = "Año publicación" if col == "anio_publicacion" else col.replace("_", " ").capitalize()
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=130)
        self.tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 6))
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def _crear_botones(self):
        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, pady=(0, 10))

        ttk.Button(frame, text="Agregar", command=self.agregar_libro, style="Accent.TButton").grid(row=0, column=0, padx=6)
        ttk.Button(frame, text="Modificar", command=self.modificar_libro).grid(row=0, column=1, padx=6)
        ttk.Button(frame, text="Eliminar", command=self.eliminar_libro).grid(row=0, column=2, padx=6)
        ttk.Button(frame, text="Limpiar", command=self.limpiar_formulario).grid(row=0, column=3, padx=6)

    def listar_libros(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for libro in listar_libros():
            self.tabla.insert("", "end", values=libro)

    def agregar_libro(self):
        codigo = self.entry_codigo.get().strip()
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        editorial = self.entry_editorial.get().strip() or None
        anio = self.entry_anio.get().strip()
        estado = self.estado_var.get()

        if not codigo or not titulo or not autor:
            messagebox.showwarning("Datos incompletos", "Código, título y autor son obligatorios.")
            return

        try:
            anio_int = int(anio) if anio else None
        except ValueError:
            messagebox.showwarning("Año inválido", "El año debe ser un número entero.")
            return

        insertar_libro(codigo, titulo, autor, editorial, anio_int, estado)
        self.listar_libros()
        self.limpiar_formulario()

    def modificar_libro(self):
        if not self.codigo_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un libro de la tabla para modificar.")
            return

        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        editorial = self.entry_editorial.get().strip() or None
        anio = self.entry_anio.get().strip()
        estado = self.estado_var.get()

        if not titulo or not autor:
            messagebox.showwarning("Datos incompletos", "Título y autor son obligatorios.")
            return

        try:
            anio_int = int(anio) if anio else None
        except ValueError:
            messagebox.showwarning("Año inválido", "El año debe ser un número entero.")
            return

        actualizar_libro(self.codigo_seleccionado, titulo, autor, editorial, anio_int, estado)
        self.listar_libros()
        self.limpiar_formulario()

    def eliminar_libro(self):
        if not self.codigo_seleccionado:
            messagebox.showwarning("Sin selección", "Seleccioná un libro de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar el libro con código {self.codigo_seleccionado}?")
        if not confirmar:
            return

        eliminar_libro(self.codigo_seleccionado)
        self.listar_libros()
        self.limpiar_formulario()

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        self.codigo_seleccionado = valores[0]

        self.entry_codigo.config(state="normal")
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, valores[0])
        self.entry_codigo.config(state="disabled")

        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, valores[1])

        self.entry_autor.delete(0, tk.END)
        self.entry_autor.insert(0, valores[2])

        self.entry_editorial.delete(0, tk.END)
        self.entry_editorial.insert(0, valores[3] or "")

        self.entry_anio.delete(0, tk.END)
        self.entry_anio.insert(0, valores[4] if valores[4] is not None else "")

        self.estado_var.set(valores[5] if valores[5] else "disponible")

    def limpiar_formulario(self):
        self.codigo_seleccionado = None
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection()[0])
        self.entry_codigo.config(state="normal")
        for entry in (self.entry_codigo, self.entry_titulo, self.entry_autor, self.entry_editorial, self.entry_anio):
            entry.delete(0, tk.END)
        self.estado_var.set("disponible")
