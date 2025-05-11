import streamlit as st
from Database.Models.Vehiculo import Vehiculo
from Database.Models.Registro import Registro
from Database.setup import crear_tablas
import datetime

# Crear tablas si no existen
crear_tablas()
st.title("Gestión de Parqueadero")

# -------------------------------
# Formulario para registrar entrada
# -------------------------------
with st.form("form_entrada"):
    placa = st.text_input("Placa")
    tipo = st.selectbox("Tipo de Vehículo", ["Carro", "Moto"])
    usuario = st.text_input("Usuario")
    submit = st.form_submit_button("Registrar Entrada")

    if submit:
        if placa and usuario:
            v = Vehiculo(placa, tipo, usuario)
            v.registrar_entrada()
            st.success("Entrada registrada exitosamente.")
            # Limpiar campos: esto se logra indirectamente porque el formulario se reinicia en Streamlit
            st.experimental_rerun()
        else:
            st.warning("Por favor, complete todos los campos.")

# -------------------------------
# Mostrar registros actuales
# -------------------------------
st.subheader("Registros de Vehículos")

registros = Registro.obtener_todos()  # Suponiendo que esta función retorna lista de dicts o tuplas

for reg in registros:
    col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 3, 2])
    col1.write(reg['placa'])
    col2.write(reg['tipo'])
    col3.write(reg['hora_entrada'])
    col4.write(reg['hora_salida'] if reg['hora_salida'] else "🟥 En parqueadero")

    # Botón para registrar salida
    if not reg['hora_salida']:
        if col5.button("Registrar salida", key=f"salida_{reg['id']}"):
            Registro.registrar_salida(reg['id'])
            st.success(f"Salida registrada para {reg['placa']}")
            st.experimental_rerun()

    # Botón para eliminar
    if st.button(f"🗑️ Eliminar {reg['placa']}", key=f"eliminar_{reg['id']}"):
        Registro.eliminar_registro(reg['id'])
        st.warning(f"Registro de {reg['placa']} eliminado.")
        st.experimental_rerun()
