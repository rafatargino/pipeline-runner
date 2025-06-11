import os
import base64
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # Default

    def configure_model(self, **kwargs):
        """
        Atualiza a configuração do modelo, como temperatura, top_p, etc.
        """
        self.model = kwargs.get("model", self.model)
        self.temperature = kwargs.get("temperature", 1.0)
        self.top_p = kwargs.get("top_p", 1.0)
        self.frequency_penalty = kwargs.get("frequency_penalty", 0.0)
        self.presence_penalty = kwargs.get("presence_penalty", 0.0)

    def send_prompt(self, system_prompt, user_prompt, attachments=[]):
        """
        Envia um prompt padrão de texto para o Chat Completions API.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        )

        return response.choices[0].message.content

    def send_prompt_with_image_url(self, system_prompt, user_prompt, image_url):
        """
        Envia um prompt com uma imagem via URL usando Chat Completions API (visão).
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        )

        return response.choices[0].message.content

    def send_prompt_with_file_url(self, system_prompt, user_prompt, file_url):
        """
        Similar a imagem, mas se precisar tratar outro tipo de URL.
        """
        return self.send_prompt_with_image_url(system_prompt, user_prompt, file_url)

    def send_prompt_with_assistants(self, system_prompt, user_prompt, attachments=[]):
        """
        Usa Assistants API para gerar um arquivo (Word, PDF, CSV) real e baixa ele.
        """
        assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

        # Cria uma thread
        thread = self.client.beta.threads.create()

        # Cria a lista de mensagens
        messages = [
            {
                "role": "user",
                "content": user_prompt,
            }
        ]

        # Enviar mensagem para a thread
        for msg in messages:
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role=msg["role"],
                content=msg["content"],
            )

        # Executa o assistente
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        if run.status != "completed":
            raise Exception(f"Assistants API Run failed with status: {run.status}")

        # 🟢 Busca mensagens da thread para encontrar arquivos
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)

        for message in messages.data:
            for item in message.content:
                if item.type == "file":
                    file_id = item.file_id
                    # Faz download do arquivo
                    return self.download_file(file_id)

        raise Exception("Nenhum arquivo foi gerado pela Assistants API.")

    def download_file(self, file_id):
        """
        Baixa o conteúdo do arquivo usando o file_id e retorna os bytes + filename.
        """
        file_obj = self.client.files.retrieve(file_id)
        file_name = file_obj.filename

        # Pega o conteúdo binário
        response = self.client.files.content(file_id)

        return response.read(), file_name  # Conteúdo binário + nome original
