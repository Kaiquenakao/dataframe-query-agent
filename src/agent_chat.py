from openai import OpenAI
import pandas as pd
import io


class ChatConversation:
    def __init__(
        self,
        api_key,
        temperature: float = 0.1,
        model: str = "gpt-4o-mini",
        max_tokens: int = 500,
    ):
        """
        Inicializa a classe de conversação com o modelo da OpenAI.

        api_key: Chave da API da OpenAI.
        temperature: Temperatura para geração de texto.
        model: Modelo da OpenAI a ser utilizado.
        max_tokens: Número máximo de tokens na resposta.

        example:
            cc = ChatConversation(
                api_key="sua_chave_aqui",
                temperature=0.2,
                model="gpt-4o-mini",
                max_tokens=500
            )
        """
        self.client = OpenAI(api_key=api_key)
        self.temperature = temperature
        self.model = model
        self.max_tokens = max_tokens
        self.history = []

    def ask(self, prompt: str, df: pd.DataFrame | None = None) -> str:
        """
        Envia um prompt para o modelo, opcionalmente com o DataFrame.

        prompt: Texto do prompt a ser enviado.
        df: DataFrame pandas carregado (opcional).
        Retorna a resposta do modelo como string.

        example:
            resposta = cc.ask(
                prompt="Me mostre as primeiras 5 linhas do DataFrame.",
                df=meu_dataframe
            )
        """
        if df is not None:
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            system_prompt = (
                "Você é um assistente especializado em análise de dados usando Python. "
                "O usuário carregou um DataFrame em memória na variável `df`. "
                "Aqui está uma amostra dos dados:\n"
                f"{info_str}\n\n"
                "IMPORTANTE:\n"
                "- Nunca gere dados fictícios, exemplos, DataFrames artificiais ou simulações.\n"
                "- Sempre utilize exclusivamente o DataFrame real já carregado na variável `df`.\n"
                "- Nunca crie o df dentro do código; ele já existe.\n\n"
                "REGRAS PARA EXIBIÇÃO:\n"
                "- Sempre que o usuário solicitar múltiplas colunas (existentes ou criadas), "
                "elas devem ser exibidas juntas, lado a lado, em um único dataframe, usando um único st.write().\n"
                "- Não dividir a resposta em múltiplos st.write() separados para colunas relacionadas.\n\n"
                "Sua tarefa é gerar código Python completo, comentado e pronto para rodar no Streamlit.\n"
                "- Use o objeto `df` diretamente para análises e visualizações.\n"
                "- Use `st.write()` para exibir resultados normalmente.\n"
                "- Se o DataFrame estiver vazio, inválido ou não utilizável, exiba um aviso usando `st.warning()` "
                "informando claramente o problema.\n"
            )

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except Exception as e:
            raise e

        reply = response.choices[0].message.content
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": reply})

        return reply
