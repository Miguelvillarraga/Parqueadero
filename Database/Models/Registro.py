import sqlite3
from ..Connection import get_connection
import datetime

class Registro:
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Vehiculo.Placa, Vehiculo.Tipo, Vehiculo.Usuario, Registro.HoraEntrada, Registro.HoraSalida
            FROM Registro
            JOIN Vehiculo ON Registro.Placa = Vehiculo.Placa
            ORDER BY Registro.HoraEntrada DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                'placa': row[0],
                'tipo': row[1],
                'usuario': row[2],
                'hora_entrada': row[3],
                'hora_salida': row[4]
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
