import tkinter as tk
from tkinter import ttk

from database import crear_tablas
from vista_libro import LibroFrame
from vista_prestamo import PrestamoFrame
from vista_socio import SocioFrame


def configurar_estilo():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("App.TFrame", background="#f3f7ff")
    style.configure("TFrame", background="#f3f7ff")
    style.configure("TLabelframe", background="#f3f7ff", foreground="#1f2937")
    style.configure("TLabelframe.Label", background="#f3f7ff", foreground="#1f2937", font=("Segoe UI", 10, "bold"))
    style.configure("TNotebook", background="#e7eefb")
    style.configure("TNotebook.Tab", background="#dfeafc", foreground="#1f2937", padding=(14, 8), font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#0f172a")])

    style.configure("TEntry", fieldbackground="#ffffff", foreground="#111827")
    style.configure("TCombobox", fieldbackground="#ffffff", foreground="#111827")
    style.configure("TButton", padding=(14, 8), font=("Segoe UI", 10, "bold"))
    style.configure("Accent.TButton", background="#2563eb", foreground="#ffffff", padding=(14, 8), font=("Segoe UI", 10, "bold"))
    style.map("Accent.TButton", background=[("active", "#1d4ed8"), ("pressed", "#1e40af")], foreground=[("active", "#ffffff")])
    style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#111827", rowheight=28)
    style.configure("Treeview.Heading", background="#dbeafe", foreground="#0f172a", font=("Segoe UI", 9, "bold"))
    style.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", "#0f172a")])


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        configurar_estilo()

        self.title("Sistema de Préstamos - Biblioteca")
        self.geometry("980x620")
        self.minsize(900, 520)
        self.configure(bg="#edf3ff")

        title = tk.Label(
            self,
            text="Biblioteca - Gestión de préstamos",
            font=("Segoe UI", 18, "bold"),
            fg="#0f172a",
            bg="#edf3ff",
            pady=12,
        )
        title.pack(fill="x")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.tab_socios = SocioFrame(notebook)
        self.tab_libros = LibroFrame(notebook)
        self.tab_prestamos = PrestamoFrame(notebook)

        self.tab_socios.configure(style="App.TFrame")
        self.tab_libros.configure(style="App.TFrame")
        self.tab_prestamos.configure(style="App.TFrame")

        notebook.add(self.tab_socios, text="Socios")
        notebook.add(self.tab_libros, text="Libros")
        notebook.add(self.tab_prestamos, text="Préstamos")


if __name__ == "__main__":
    crear_tablas()
    app = App()
    app.mainloop()