import streamlit as st

from scripts.parser import *





st.title("Processador de consultas")

query = st.text_area("Escreva sua consulta SQL aqui:")



if st.button("Processar Consulta"):

    print(query)

    #------------------------------------------------------
    #parser
    status, msg = parser( query )

    st.write(f"Consulta processada: {msg}")

    #------------------------------------------------------
    # otimizador
    if status:

        pass


    #------------------------------------------------------
    # Exibir Grafo
    if status:
        pass