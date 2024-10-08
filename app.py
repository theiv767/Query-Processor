import streamlit as st


st.title("Processador de consultas")

query = st.text_area("Escreva sua consulta SQL aqui:")



if st.button("Processar Consulta"):

    print(query)


    st.write(f"Consulta processada: {query}")