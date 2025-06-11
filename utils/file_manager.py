
import os
import requests
from docx import Document
from config import OUTPUT_DIR, DATA_INICIO, DATA_FIM
from datetime import datetime

class FileManager:
    def save_output(self, output_file_path, content, output_type="txt"):
        """
        Salva o conteúdo retornado pela API no formato adequado.
        output_type: 'txt', 'docx', ou 'file' (quando é um link para download).
        """
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        if output_type == "txt":
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(content)

        elif output_type == "docx":
            doc = Document()
            doc.add_paragraph(content)
            doc.save(output_file_path)

        elif output_type == "file":
            # Se for 'file', o `content` precisa ser uma URL pública ou file_id
            self.download_file(content, output_file_path)

        else:
            raise ValueError(f"Tipo de output não suportado: {output_type}")

    def download_file(self, file_url_or_id, output_path):
        """
        Baixa um arquivo binário de uma URL.
        """
        response = requests.get(file_url_or_id)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
        else:
            raise Exception(f"Falha ao baixar arquivo: {file_url_or_id} (status code: {response.status_code})")
