import streamlit as st


with st.sidebar:
    st.header("Menu")
    openai_token = st.text_input("OpenAI API Token", type="password")
    
    # Botão para salvar
    if st.button("Salvar Token"):
        if openai_token:
            st.session_state["openai_token"] = openai_token
            st.success("Token salvo!")
        else:
            st.warning("Digite o token antes de salvar.")