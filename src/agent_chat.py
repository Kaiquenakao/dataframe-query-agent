from openai import OpenAI
import pandas as pd
import json

class ChatConversation:
    def __init__(self, api_key: str, temperature: float = 0.7, model: str = "gpt-4o-mini"):
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
            sample = df.head(5).to_dict(orient="records")
            data_str = json.dumps(sample, ensure_ascii=False)
            system_prompt = (
                "Você é um assistente especializado em análise de dados. "
                "Aqui está uma amostra do DataFrame que o usuário carregou:\n"
                f"{data_str}\n"
                "Use isso como contexto para responder."
            )
        else:
            system_prompt = "Você é um assistente que responde perguntas gerais sobre dados."

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
