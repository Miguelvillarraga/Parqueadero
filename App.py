import streamlit as st
from Database.Models.Vehiculo import Vehiculo
from Database.Models.Registro import Registro
from Database import setup


crear_tablas()
st.title("Gestión de Parqueadero")

placa = st.text_input("Placa")
tipo = st.selectbox("Tipo de Vehículo", ["Carro", "Moto"])
usuario = st.text_input("Usuario")

if st.button("Registrar Entrada"):
    if placa and usuario:
        v = Vehiculo(placa, tipo, usuario)
        v.registrar_entrada()
        st.success("Entrada registrada exitosamente.")
    else:
        st.warning("Por favor, complete todos los campos.")
