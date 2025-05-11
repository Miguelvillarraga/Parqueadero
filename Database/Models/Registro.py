from ..Connection import get_connection
from datetime import datetime

class Registro:
    @staticmethod
    def registrar_salida(placa):
        conn = get_connection()
        cursor = conn.cursor()
        ahora = datetime.now()
        fecha = ahora.date().isoformat()
        hora = ahora.time().strftime('%H:%M:%S')

        cursor.execute("""
            UPDATE Registro
            SET Fecha_Salida = ?, Hora_Salida = ?
            WHERE Placa_Vehiculo = ? AND Fecha_Salida IS NULL
        """, (fecha, hora, placa))
        conn.commit()
        conn.close()

    @staticmethod
    def historial_por_vehiculo(placa):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Fecha_Entrada, Hora_Entrada, Fecha_Salida, Hora_Salida
            FROM Registro
            WHERE Placa_Vehiculo = ?
            ORDER BY ID_Registro DESC
        """, (placa,))
        registros = cursor.fetchall()
        conn.close()
        return registros

    @staticmethod
    def esta_dentro(placa):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Registro
            WHERE Placa_Vehiculo = ? AND Fecha_Salida IS NULL
        """, (placa,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0