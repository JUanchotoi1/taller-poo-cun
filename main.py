import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

# ==========================================
# 1. CLASES BASE (POO)
# ==========================================

class UsuarioCUN(ABC):
    def __init__(self, identificador: str, nombre: str):
        self._identificador = identificador
        self._nombre = nombre

    @abstractmethod
    def obtener_rol(self) -> str:
        pass


class Estudiante(UsuarioCUN):
    def __init__(self, identificador: str, nombre: str, programa: str, promedio: float = 0.0):
        super().__init__(identificador, nombre)
        self.programa = programa
        self.__promedio = 0.0
        self.actualizar_promedio(promedio)

    def obtener_promedio(self) -> float:
        return self.__promedio

    def actualizar_promedio(self, valor: float):
        if 0.0 <= valor <= 5.0:
            self.__promedio = valor
        else:
            raise ValueError("El promedio debe estar entre 0.0 y 5.0")

    def obtener_rol(self) -> str:
        return f"Estudiante de {self.programa}"


class Docente(UsuarioCUN):
    def __init__(self, identificador: str, nombre: str, especialidad: str):
        super().__init__(identificador, nombre)
        self.especialidad = especialidad

    def obtener_rol(self) -> str:
        return f"Docente de {self.especialidad}"


# ==========================================
# 2. INTERFAZ GRÁFICA (Tkinter)
# ==========================================

class MesaAyudaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesa de Ayuda TI y Gestión Académica - CUN")
        self.root.geometry("700x500")

        # Inicializar BD
        self.inicializar_bd()

        # Componentes de la interfaz
        label_titulo = tk.Label(root, text="Sistema de Gestión CUN", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=10)

        # Botón para cargar datos rápidos de prueba
        btn_cargar = tk.Button(root, text="Cargar Datos de Prueba", command=self.cargar_datos_prueba, bg="#0284c7", fg="white")
        btn_cargar.pack(pady=5)

        # Lista de vista de tickets
        self.tree = ttk.Treeview(root, columns=("ID", "Estudiante", "Categoría", "Estado"), show="headings")
        self.tree.heading("ID", text="ID Ticket")
        self.tree.heading("Estudiante", text="Estudiante ID")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.actualizar_tabla()

    def inicializar_bd(self):
        conn = sqlite3.connect('cun_sistema.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS estudiantes 
            (id_estudiante TEXT PRIMARY KEY, nombre TEXT, programa TEXT, promedio REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS docentes 
            (id_docente TEXT PRIMARY KEY, nombre TEXT, especialidad TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tickets_soporte 
            (id_ticket INTEGER PRIMARY KEY AUTOINCREMENT, id_estudiante TEXT, categoria TEXT, descripcion TEXT, estado TEXT, id_docente_asignado TEXT)''')
        conn.commit()
        conn.close()

    def cargar_datos_prueba(self):
        try:
            est = Estudiante("E-101", "Laura Gómez", "Sistemas", 4.5)
            doc = Docente("D-201", "Dr. Carlos Ruiz", "Ingeniería de Software")

            conn = sqlite3.connect('cun_sistema.db')
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO estudiantes VALUES (?, ?, ?, ?)", 
                           (est._identificador, est._nombre, est.programa, est.obtener_promedio()))
            cursor.execute("INSERT OR REPLACE INTO docentes VALUES (?, ?, ?)", 
                           (doc._identificador, doc._nombre, doc.especialidad))
            cursor.execute("INSERT INTO tickets_soporte (id_estudiante, categoria, descripcion, estado) VALUES (?, ?, ?, ?)",
                           ("E-101", "Plataforma Virtual", "Acceso a aula virtual", "ABIERTO"))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos de prueba cargados correctamente.")
            self.actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        conn = sqlite3.connect('cun_sistema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_ticket, id_estudiante, categoria, estado FROM tickets_soporte")
        registros = cursor.fetchall()
        for r in registros:
            self.tree.insert("", "end", values=r)
        conn.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = MesaAyudaApp(root)
    root.mainloop()