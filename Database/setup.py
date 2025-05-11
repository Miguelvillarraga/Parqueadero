import sqlite3

def crear_tablas():
    conn = sqlite3.connect("parqueadero.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vehiculo (
            Placa TEXT PRIMARY KEY,
            Tipo TEXT,
            Usuario TEXT
        );
    """)

    conn.commit()
    conn.close()
