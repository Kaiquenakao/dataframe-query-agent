from openai import OpenAI
import pandas as pd
import json
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("OPENAI_API_KEY")

class ChatConversation:
    def __init__(self, temperature: float = 0.1, model: str = "gpt-4o-mini"):
        """
        Inicializa a classe de conversação com o modelo da OpenAI.
        """
        self.client = OpenAI(api_key=api_key)
        self.temperature = temperature
        self.model = model
        self.history = [] 

    def ask(self, prompt: str, df: pd.DataFrame | None = None) -> str:
        """
        Envia um prompt para o modelo, opcionalmente com o DataFrame.
        """
        if df is not None:
            sample = df.head().to_dict(orient="records")
            data_str = json.dumps(sample, ensure_ascii=False)
            system_prompt = (
                "Você é um assistente especializado em análise de dados usando Python. "
                "O usuário carregou um DataFrame, e aqui está uma amostra:\n"
                f"{data_str}\n\n"
                "Use este DataFrame como contexto para gerar código Python que faça análise"
                "O código deve ser completo, comentado e pronto para rodar no Streamlit, "
                "usando `st.write` para exibir resultados"
            )

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": reply})

        return reply
