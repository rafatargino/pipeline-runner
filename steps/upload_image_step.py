import os
import glob
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from steps.custom_step import CustomStep
from config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

class UploadImageStep(CustomStep):
    def __init__(self, config, file_manager):
        super().__init__(config, file_manager)
        
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True
        )

    def run(self):
        inputs = self.config.get("inputs", [])
        custom_params = self.config.get("custom_params", {})
        pipeline_name = self.config.get("pipeline_name", "default")  # Nome do pipeline atual
        step_name = self.config.get('step_name', 'Step1')  # Nome do step atual

        # Pegando a configuração de input
        if not inputs:
            raise ValueError("Nenhum input definido no YAML.")

        input_conf = inputs[0]  # Assume que há pelo menos 1 entrada
        folder = input_conf["input_folder"]
        pattern = input_conf["input_pattern"]
        
        # Caminho completo para os inputs
        base_path = os.path.join("data", pipeline_name)
        input_path = os.path.join(base_path, "input", folder)
        full_pattern = os.path.join(input_path, pattern)

        # Pegando todos os arquivos que batem com o padrão
        image_files = glob.glob(full_pattern)
        if not image_files:
            print(f"⚠️ Nenhum arquivo encontrado no padrão {full_pattern}")
            return

        cloudinary_folder = custom_params.get("cloudinary_folder", "timetrack")
        # Caminho para o output diretamente no diretório do pipeline
        step_dir = os.path.join(base_path, step_name.lower())
        os.makedirs(step_dir, exist_ok=True)
        output_file = os.path.join(step_dir, "funcionalidades_urls.txt")

        image_urls = {}

        for image_path in image_files:
            nome_base = os.path.splitext(os.path.basename(image_path))[0]  # Remove extensão

            url = self.upload_image_to_cloudinary(image_path, nome_base, cloudinary_folder)
            if url:
                image_urls[nome_base] = url
                self.file_manager.log(f"✅ Imagem '{nome_base}' enviada. URL: {url}")
            else:
                self.file_manager.log(f"❌ Falha ao enviar imagem '{nome_base}'.")

        # Salva as URLs em um arquivo CSV-like
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            for nome_base, url in image_urls.items():
                f.write(f"{nome_base},{url}\n")

        print(f"✅ URLs das imagens salvas em: {output_file}")
        return image_urls

    def upload_image_to_cloudinary(self, image_path, nome_base, cloudinary_folder):
        """
        Faz upload da imagem para o Cloudinary.
        Gera o public_id como cloudinary_folder/nome_base
        """
        try:
            upload_result = cloudinary.uploader.upload(
                image_path,
                public_id=f"{cloudinary_folder}/{nome_base}",
                overwrite=True,
                resource_type="image"
            )
            return upload_result.get("secure_url")
        except Exception as e:
            print(f"❌ Erro no upload de '{nome_base}': {e}")
            return None
