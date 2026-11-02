import sqlite3

def crear_base_datos_cun():
    """Script para inicializar la base de datos SQLite con las tablas del sistema."""
    conn = sqlite3.connect('cun_sistema.db')
    cursor = conn.cursor()

    # 1. Tabla Estudiantes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id_estudiante TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            programa TEXT NOT NULL,
            promedio REAL DEFAULT 0.0
        )
    ''')

    # 2. Tabla Docentes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docentes (
            id_docente TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL
        )
    ''')

    # 3. Tabla Tickets de Soporte TI
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets_soporte (
            id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
            id_estudiante TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT DEFAULT 'ABIERTO',
            id_docente_asignado TEXT,
            FOREIGN KEY (id_estudiante) REFERENCES estudiantes (id_estudiante),
            FOREIGN KEY (id_docente_asignado) REFERENCES docentes (id_docente)
        )
    ''')

    conn.commit()
    conn.close()
    print("[OK] Base de datos 'cun_sistema.db' creada/verificada correctamente.")

if __name__ == '__main__':
    crear_base_datos_cun()