import sqlite3
from abc import ABC, abstractmethod

# ==========================================
# 1. BASE DE DATOS (SQLite)
# ==========================================
def crear_base_datos_cun():
    """Crea la base de datos local SQLite y las tablas requeridas."""
    conn = sqlite3.connect('cun_sistema.db')
    cursor = conn.cursor()

    # Tabla Estudiantes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id_estudiante TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            programa TEXT NOT NULL,
            promedio REAL DEFAULT 0.0
        )
    ''')

    # Tabla Tickets de Soporte TI
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets_soporte (
            id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
            id_estudiante TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT DEFAULT 'ABIERTO',
            FOREIGN KEY (id_estudiante) REFERENCES estudiantes (id_estudiante)
        )
    ''')

    conn.commit()
    conn.close()
    print("[Exitoso] Base de datos 'cun_sistema.db' creada correctamente.")


# ==========================================
# 2. MODELO DE CLASES (POO)
# ==========================================

# Abstracción
class UsuarioCUN(ABC):
    def __init__(self, id_usuario: str, nombre: str):
        self.id_usuario = id_usuario
        self.nombre = nombre

    @abstractmethod
    def obtener_rol(self) -> str:
        pass


# Herencia y Encapsulamiento
class Estudiante(UsuarioCUN):
    def __init__(self, id_usuario: str, nombre: str, programa: str, promedio_inicial: float = 0.0):
        super().__init__(id_usuario, nombre)
        self.programa = programa
        self.__promedio = 0.0  # Atributo privado
        self.actualizar_promedio(promedio_inicial)

    def obtener_promedio(self) -> float:
        return self.__promedio

    def actualizar_promedio(self, nuevo_promedio: float):
        if 0.0 <= nuevo_promedio <= 5.0:
            self.__promedio = nuevo_promedio
        else:
            print(f"[Error de Validación]: El promedio debe estar entre 0.0 y 5.0")

    def obtener_rol(self) -> str:
        return f"Estudiante del programa: {self.programa}"

    def guardar_en_bd(self):
        conn = sqlite3.connect('cun_sistema.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO estudiantes (id_estudiante, nombre, programa, promedio)
                VALUES (?, ?, ?, ?)
            ''', (self.id_usuario, self.nombre, self.programa, self.__promedio))
            conn.commit()
            print(f"[OK] Estudiante '{self.nombre}' guardado en la BD.")
        except sqlite3.IntegrityError:
            print(f"[Aviso] El estudiante con ID '{self.id_usuario}' ya existe.")
        finally:
            conn.close()


# Composición / Asociación
class TicketSoporte:
    def __init__(self, estudiante: Estudiante, categoria: str, descripcion: str):
        self.estudiante = estudiante
        self.categoria = categoria
        self.descripcion = descripcion
        self.estado = "ABIERTO"

    def guardar_en_bd(self):
        conn = sqlite3.connect('cun_sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets_soporte (id_estudiante, categoria, descripcion, estado)
            VALUES (?, ?, ?, ?)
        ''', (self.estudiante.id_usuario, self.categoria, self.descripcion, self.estado))
        conn.commit()
        ticket_id = cursor.lastrowid
        conn.close()
        print(f"[OK] Ticket #{ticket_id} registrado para {self.estudiante.nombre}.")


# ==========================================
# 3. EJECUCIÓN Y PRUEBA
# ==========================================
if __name__ == '__main__':
    print("=== INICIANDO SISTEMA DE GESTIÓN CUN ===")
    
    # Crear las tablas
    crear_base_datos_cun()

    # Instanciar estudiantes
    est1 = Estudiante("E-101", "Laura Gómez", "Ingeniería de Sistemas", 4.2)
    est2 = Estudiante("E-102", "Carlos Pérez", "Administración", 3.8)

    # Guardar estudiantes en BD
    est1.guardar_en_bd()
    est2.guardar_en_bd()

    # Crear y guardar tickets de soporte
    ticket1 = TicketSoporte(est1, "Plataforma Virtual", "No puedo acceder al aula")
    ticket2 = TicketSoporte(est2, "Red Wi-Fi", "Sin conexión en la sede")

    ticket1.guardar_en_bd()
    ticket2.guardar_en_bd()

    print("=== PRUEBA FINALIZADA ===")