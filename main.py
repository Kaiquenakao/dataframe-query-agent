import streamlit as st
import pandas as pd

st.title("Visualizador de DataFrame")

arquivo = st.file_uploader("Selecione um arquivo", type=["csv", "parquet", "json"])

if arquivo is not None:
    prompt = st.text_input("Digite o que deseja realizar com o dataframe")

    if st.button("Carregar DataFrame Original"):
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        elif arquivo.name.endswith(".parquet"):
            df = pd.read_parquet(arquivo)
        elif arquivo.name.endswith(".json"):
            df = pd.read_json(arquivo)
        else:
            st.error("Formato de arquivo não suportado.")
            df = None

        if df is not None:
            st.success("DataFrame carregado com sucesso!")
            st.write(df)

            


with st.sidebar:
    st.header("Menu")
    openai_token = st.text_input("OpenAI API Token", type="password")
    
    temperatura = st.slider(
        "Temperatura do LLM",
        min_value=0.0,
        max_value=1.0,
        value=0.7,  # valor padrão
        step=0.1,
        help="Controla a aleatoriedade das respostas. 0 = mais determinístico, 1 = mais criativo."
    )

    if st.button("Salvar Token"):
        if openai_token:
            st.session_state["openai_token"] = openai_token
            st.success("Token salvo!")
        else:
            st.warning("Digite o token antes de salvar.")
