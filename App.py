import streamlit as st
from Database.Models.Vehiculo import Vehiculo
from Database.Models.Registro import Registro
from Database.setup import crear_tablas
import datetime

# Crear tablas si no existen
crear_tablas()
st.title("Gestión de Parqueadero")

# -------------------------------
# Cargar registros desde la base de datos
# -------------------------------
def cargar_registros():
    registros = Registro.obtener_todos()  # Obtener registros actualizados
    return registros

# -------------------------------
# Formulario para registrar entrada
# -------------------------------
with st.form("form_entrada"):
    placa = st.text_input("Placa", key="placa")  # Usamos key para mantener el estado
    tipo = st.selectbox("Tipo de Vehículo", ["Carro", "Moto"], key="tipo")
    usuario = st.text_input("Usuario", key="usuario")
    submit = st.form_submit_button("Registrar Entrada")

    if submit:
        if placa and usuario:
            v = Vehiculo(placa, tipo, usuario)
            v.registrar_entrada()
            st.success("Entrada registrada exitosamente.")
            
            # Reiniciar los campos inmediatamente después de registrar
            st.session_state.placa = ""
            st.session_state.tipo = "Carro"  # O el valor predeterminado que prefieras
            st.session_state.usuario = ""

            # Actualizar la tabla
            st.session_state.updated = True
        else:
            st.warning("Por favor, complete todos los campos.")

# -------------------------------
# Mostrar registros actuales
# -------------------------------
st.subheader("Registros de Vehículos")

# Cargar los registros y mostrarlos en la tabla
tabla_vacia = st.empty()  # Usamos un contenedor vacío para actualizar la tabla

# Función para mostrar los registros
def mostrar_tabla(registros):
    # Cabeceras de tabla
    cab1, cab2, cab3, cab4, cab5, cab6 = st.columns([2, 2, 2, 2, 2, 1])
    cab1.markdown("**Placa**")
    cab2.markdown("**Tipo**")
    cab3.markdown("**Fecha y Hora Entrada**")
    cab4.markdown("**Fecha y Hora Salida**")
    cab5.markdown("**Registrar Salida**")
    cab6.markdown("**Eliminar**")

    # Filas de registros
    for reg in registros:
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])

        col1.write(reg.get('placa', 'N/A'))
        col2.write(reg.get('tipo', 'N/A'))

        # Mostrar fecha y hora de entrada
        if reg.get('fecha_entrada') and reg.get('hora_entrada'):
            col3.write(f"{reg['fecha_entrada']} {reg['hora_entrada']}")
        else:
            col3.write("N/A")

        # Mostrar fecha y hora de salida
        if reg.get('fecha_salida') and reg.get('hora_salida'):
            col4.write(f"{reg['fecha_salida']} {reg['hora_salida']}")
        else:
            col4.write("🟥 En parqueadero")

        # Botón para registrar salida
        if not reg['hora_salida']:
            if col5.button("Registrar salida", key=f"salida_{reg['id']}"):
                Registro.registrar_salida(reg['id'])
                st.success(f"Salida registrada para {reg['placa']}")
        else:
            col5.write("✅")

        # Botón para eliminar
        if col6.button("🗑️", key=f"eliminar_{reg['id']}"):
            Registro.eliminar_registro(reg['id'])
            st.warning(f"Registro de {reg['placa']} eliminado.")

# Mostrar la tabla inicialmente
registros = cargar_registros()  # Cargamos los registros al inicio
mostrar_tabla(registros)

# Actualizar la tabla después de cada acción
if st.session_state.get('updated', False):  # Verificar si se actualizó el estado
    registros = cargar_registros()  # Recargar los registros
    mostrar_tabla(registros)
    st.session_state.updated = False  # Resetear el flag
