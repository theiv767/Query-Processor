import streamlit as st

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './scripts')))

import scripts.utils
from scripts.parser import *
from scripts.optimizer import *
from scripts.plot import *
from scripts.utils import *






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
        sql_formatada = replace_sql_keywords(query)
        algebra_result = convert_sql_to_algebra(sql_formatada)

        st.write(f"Algebra Relacional: {algebra_result}")

        tree = construct_tree(algebra_result)
        plot_tree(tree)

        st.pyplot(plt)
        pass