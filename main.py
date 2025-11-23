"""
Visualizador de DataFrame com Streamlit e OpenAI API.
Permite ao usuário carregar um arquivo de dados (CSV, Parquet, JSON),
fazer perguntas sobre o DataFrame e obter respostas geradas pela API da OpenAI.
"""

import re


import streamlit as st
import pandas as pd

from src.agent_chat import ChatConversation
from src.utils import get_logger
from src.sidebar import render_sidebar

logger = get_logger("visualizador_df")

st.title("Visualizador de DataFrame")

# --- SIDEBAR ---
openai_token, temperature, max_tokens = render_sidebar()

# --- VERIFICAÇÃO DO TOKEN ---
token_ok = "openai_token" in st.session_state and st.session_state["openai_token"]

arquivo = st.file_uploader("Selecione um arquivo", type=["csv", "parquet", "json"])

df = None

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
            logger.error("Arquivo inválido: %s", arquivo.name)
            df = None
    except Exception as e:
        st.error(
            "Erro ao ler o arquivo. Verifique se é um arquivo válido. Detalhes: %s", e
        )
        logger.error("Erro ao ler o arquivo: %s", e)
        df = None

# --- INPUT DO COMANDO DEPENDENTE DO TOKEN ---
if not token_ok or df is None:
    st.warning(
        "**Antes de continuar:**\n"
        "Para habilitar o campo de comandos, você precisa:\n\n"
        "1. Inserir seu **OpenAI API Token** no menu lateral\n"
        "2. Clicar em **Salvar Token**\n"
        "3. Selecionar um **arquivo** para carregar\n\n"
        "Após isso, o campo de **texto** será liberado!"
    )
    prompt = st.text_input(
        "Digite o que deseja realizar com o dataframe", disabled=True
    )
else:
    prompt = st.text_input("Digite o que deseja realizar com o dataframe")

# --- PROCESSAMENTO DO PROMPT ---
if prompt and df is not None and token_ok:
    logger.info("Executando o prompt: %s", prompt)
    cc = ChatConversation(
        api_key=openai_token, temperature=temperature, max_tokens=max_tokens
    )
    try:
        resp = cc.ask(prompt=prompt, df=df)
        match = re.search(r"```python(.*?)```", resp, re.DOTALL)
    except Exception as e:
        st.error("Erro ao processar o prompt: %s", e)
        logger.error("Erro ao processar o prompt: %s", e)
        resp = None
        match = None

    if match:
        codigo = match.group(1).strip()
        logger.info("=== Código extraído ===")

        try:
            exec(codigo)
            logger.info("Execução do código realizada com sucesso.")
        except Exception as e:
            logger.error("Erro ao executar o código: %s", e)
            st.error("Erro ao executar o código: %s", e)
    else:
        logger.warning("Nenhum código Python encontrado.")
        logger.debug(f"Match result: {match}")

# --- BOTÕES DE AÇÃO PARA CARREGAR/LIMPAR DATAFRAME ---
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
