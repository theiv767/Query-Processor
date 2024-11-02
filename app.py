import streamlit as st

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './scripts')))

import scripts.utils
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