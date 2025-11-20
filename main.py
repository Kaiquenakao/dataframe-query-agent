import streamlit as st
import pandas as pd
from src.agent_chat import ChatConversation
from src.utils import get_logger
import re

logger = get_logger("visualizador_df")
cc = ChatConversation()

st.title("Visualizador de DataFrame")

arquivo = st.file_uploader("Selecione um arquivo", type=["csv", "parquet", "json"])

if arquivo is not None:
    try:
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        elif arquivo.name.endswith(".parquet"):
            df = pd.read_parquet(arquivo)
        elif arquivo.name.endswith(".json"):
            df = pd.read_json(arquivo)
        else:
            st.error("Formato de arquivo não suportado.")
            df = None
    except Exception as e:
        st.error(f"Erro ao ler o arquivo. Verifique se é um arquivo válido. Detalhes: {e}")
        logger.error(f"Erro ao ler o arquivo: {e}")
        df = None

    prompt = st.text_input("Digite o que deseja realizar com o dataframe")

    if prompt and df is not None:
        logger.info(f"Executando o prompt: {prompt}")
        resp = cc.ask(prompt=prompt, df=df)
        match = re.search(r"```python(.*?)```", resp, re.DOTALL)

        if match:
            codigo = match.group(1).strip()
            logger.info("=== Código extraído ===")
            
            try:
                exec(codigo)
                logger.info("Execução do código realizada com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao executar o código: {e}")
                st.error(f"Erro ao executar o código: {e}")
        else:
            logger.warning("Nenhum código Python encontrado.")
            logger.debug(f"Match result: {match}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Carregar DataFrame Original"):
            if df is not None:
                st.success("DataFrame carregado com sucesso!")
                st.write(df)
            else:
                st.warning("Nenhum DataFrame foi carregado corretamente.")

    with col2:
        if st.button("Limpar DataFrame Original"):
            if df is not None:
                st.session_state.df = None
                st.success("DataFrame limpo com sucesso!")
                logger.info("DataFrame limpo com sucesso.")
            else:
                st.warning("Nenhum DataFrame foi limpado corretamente.")
            
with st.sidebar:
    st.header("Menu")
    openai_token = st.text_input("OpenAI API Token", type="password")
    
    temperatura = st.slider(
        "Temperatura do LLM",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controla a aleatoriedade das respostas. 0 = mais determinístico, 1 = mais criativo."
    )

    max_tokens = st.number_input(
        "Máximo de tokens da resposta",
        min_value=50,
        max_value=2000,
        value=300,
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
