import streamlit as st
from src.utils import get_logger

logger = get_logger("sidebar")

def render_sidebar():
    with st.sidebar:
        st.header("Menu")

        openai_token = st.text_input("OpenAI API Token", type="password")
        
        temperature = st.slider(
            "Temperatura do LLM",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controla a aleatoriedade das respostas."
        )

        max_tokens = st.number_input(
            "Máximo de tokens da resposta",
            min_value=50,
            max_value=2000,
            value=1000,
            help="Limita o tamanho da resposta"
        )

        if st.button("Salvar Token"):
            if openai_token:
                st.session_state["openai_token"] = openai_token
                st.success("Token salvo!")
                logger.info("Token OpenAI salvo no session_state.")
            else:
                st.warning("Digite o token antes de salvar.")
                logger.warning("Tentativa de salvar token vazio.")

    return openai_token, temperature, max_tokens
