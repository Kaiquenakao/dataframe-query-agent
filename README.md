# 🧠 Agente de Consulta de DataFrame em Python

Este repositório contém um agente inteligente que permite aos usuários interagir com DataFrames do Pandas usando linguagem natural.  
O sistema utiliza modelos da OpenAI para interpretar comandos e gerar automaticamente **código Python seguro**, executado em tempo real dentro da aplicação Streamlit.

---

## ✨ Funcionalidades

- 📂 Carregamento de DataFrames a partir de arquivos CSV  
- 🗣️ Interpretação de consultas em **linguagem natural**  
- 🤖 Geração automática de código Python com base no pedido do usuário  
- 🔒 Execução segura e controlada do código gerado  
- 📊 Exibição de resultados diretamente no Streamlit  

---

## 📁 Estrutura do Projeto
```bash
.
├── src
│ ├── agent_chat.py # Classe responsável pela interação com o modelo da OpenAI
│ ├── sidebar.py # Configurações e UI da barra lateral no Streamlit
│ ├── utils.py # Funções auxiliares (ex: logger)
│
├── dados.csv # Arquivo de exemplo para carregar no DataFrame
├── main.py # Aplicação principal em Streamlit
├── requirements.txt # Dependências do projeto
├── README.md # Documentação
└── .gitignore # Arquivos ignorados pelo Git
```

## 🚀 Como Usar
1. Clone o repositório:  
   `git clone https://github.com/Kaiquenakao/dataframe-query-agent.git`
2. Instale as dependências:
   `pip install -r requirements.txt`
3. Execute a aplicação Streamlit:
   `python -m streamlit run main.py`
4. Carregue um arquivo CSV e comece a fazer perguntas sobre os dados!
5. Insira seu token da OpenAI API na barra lateral para habilitar a geração de código.
6. Digite suas consultas em linguagem natural e veja os resultados!
---
## Benefícios
- Acelera o processo de exploração de dados com respostas rápidas e precisas.
- Proporciona uma experiência interativa e intuitiva para trabalhar com DataFrames.
- Pessoas com pouca ou nenhuma experiência em Python podem realizar análises complexas de dados.
---