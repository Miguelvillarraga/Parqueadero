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
    if 'actualizar' in st.session_state:
        del st.session_state['actualizar']
    placa = st.text_input("Placa")
    tipo = st.selectbox("Tipo de Vehículo", ["Carro", "Moto"])
    usuario = st.text_input("Usuario")
    submit = st.form_submit_button("Registrar Entrada")

    if submit:
        if placa and usuario:
            v = Vehiculo(placa, tipo, usuario)
            v.registrar_entrada()
            st.success("Entrada registrada exitosamente.")
            st.experimental_rerun()
        else:
            st.warning("Por favor, complete todos los campos.")

# -------------------------------
# Mostrar registros actuales
# -------------------------------
st.subheader("Registros de Vehículos")

registros = Registro.obtener_todos()  # Debe incluir: id, placa, tipo, hora_entrada, hora_salida

# Cabeceras de tabla
cab1, cab2, cab3, cab4, cab5, cab6 = st.columns([2, 2, 2, 2, 2, 1])
cab1.markdown("**Placa**")
cab2.markdown("**Tipo**")
cab3.markdown("**Hora Entrada**")
cab4.markdown("**Hora Salida**")
cab5.markdown("**Registrar Salida**")
cab6.markdown("**Eliminar**")

# Filas de registros
for reg in registros:
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])

    col1.write(reg.get('placa', 'N/A'))
    col2.write(reg.get('tipo', 'N/A'))
    col3.write(reg.get('hora_entrada', 'N/A'))
    col4.write(reg['hora_salida'] if reg.get('hora_salida') else "🟥 En parqueadero")

    # Botón para registrar salida
    if not reg['hora_salida']:
        if col5.button("Registrar salida", key=f"salida_{reg['id']}"):
            Registro.registrar_salida(reg['id'])
            st.success(f"Salida registrada para {reg['placa']}")
            st.session_state['actualizar'] = True
            st.stop()  # Detiene ejecución y reinicia desde arriba (seguro)
    else:
        col5.write("✅")

    # Botón para eliminar
    if col6.button("🗑️", key=f"eliminar_{reg['id']}"):
        Registro.eliminar_registro(reg['id'])
        st.warning(f"Registro de {reg['placa']} eliminado.")
        st.experimental_rerun()
