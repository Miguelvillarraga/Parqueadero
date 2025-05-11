import sqlite3
from ..Connection import get_connection
import datetime

class Registro:
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, placa, tipo, usuario, hora_entrada, hora_salida FROM Vehiculo ORDER BY hora_entrada DESC")
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                'id': row[0],
                'placa': row[1],
                'tipo': row[2],
                'usuario': row[3],
                'hora_entrada': row[4],
                'hora_salida': row[5]
            }
            for row in rows
        ]

    @staticmethod
    def registrar_salida(id_registro):
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE Vehiculo SET hora_salida = ? WHERE id = ?", (now, id_registro))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar_registro(id_registro):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Vehiculo WHERE id = ?", (id_registro,))
        conn.commit()
        conn.close()
