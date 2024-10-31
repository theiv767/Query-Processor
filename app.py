import streamlit as st

from scripts.query_processing_functions import *




st.title("Processador de consultas")

query = st.text_area("Escreva sua consulta SQL aqui:")



if st.button("Processar Consulta"):

    print(query)

    statues, msg = parser( query )

    st.write(f"Consulta processada: {msg}")