import os
import glob

class PromptStep:
    def __init__(self, config, openai_client, file_manager):
        self.config = config
        self.openai_client = openai_client
        self.file_manager = file_manager

    def run(self):
        prompt_data = self.config.get("prompt", {})
        system_prompt = prompt_data.get("system", "")
        user_prompt = prompt_data.get("user", "")
        attachments = prompt_data.get("attachments", [])

        if not system_prompt or not user_prompt:
            raise ValueError("Prompt não encontrado ou incompleto na configuração.")

        inputs = self.config.get("inputs", [])
        if not inputs:
            raise ValueError("Nenhum input definido.")

        model_params = self.config.get("model_params", {})
        output_config = self.config.get("output", {})

        # Configurar modelo (temperatura, top_p etc.)
        self.openai_client.configure_model(**model_params)

        # modo de geração (chat ou assistants)
        generator_mode = self.config.get("generator_mode", "chat")  # Default: chat

        # Aqui lê a saída correta UMA VEZ (fora do loop dos arquivos)
        output_folder = output_config.get("output_folder", "outputs/")
        output_type = output_config.get("output_type", "txt")
        send_files_separately = output_config.get("send_files_separately", True)

        os.makedirs(output_folder, exist_ok=True)

        for input_conf in inputs:
            input_type = input_conf.get("input_type")
            input_folder = input_conf.get("input_folder")
            input_pattern = input_conf.get("input_pattern")
            multiple_files = input_conf.get("multiple_files", False)

            # Buscar arquivos
            files = glob.glob(os.path.join(input_folder, input_pattern))

            if not files:
                print(f"⚠️ Nenhum arquivo encontrado para o padrão: {input_folder}/{input_pattern}")
                continue

            if send_files_separately:
                for file_path in files:
                    self.process_single_file(
                        file_path, input_type, system_prompt, user_prompt,
                        generator_mode, output_folder, output_type
                    )
            else:
                # Se quiser mandar todos juntos (não está 100% implementado aqui ainda)
                raise NotImplementedError("Envio combinado de múltiplos arquivos ainda não implementado.")


    def process_single_file(self, file_path, input_type, system_prompt, user_prompt,
                             generator_mode, output_folder, output_type):
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"📄 Processando arquivo: {file_path}")

        if input_type in ("image", "pdf", "audio"):
            url_path = os.path.splitext(file_path)[0] + ".url"
            if not os.path.exists(url_path):
                raise FileNotFoundError(f"Arquivo .url não encontrado para {file_path}")

            with open(url_path, "r") as f:
                url = f.read().strip()

            if input_type == "image":
                if generator_mode == "assistants":
                    content, filename = self.openai_client.send_prompt_with_assistants(system_prompt, user_prompt, attachments=[url])
                else:
                    content = self.openai_client.send_prompt_with_image_url(system_prompt, user_prompt, url)
            else:
                if generator_mode == "assistants":
                    content, filename = self.openai_client.send_prompt_with_assistants(system_prompt, user_prompt, attachments=[url])
                else:
                    content = self.openai_client.send_prompt_with_file_url(system_prompt, user_prompt, url)

        else:
            if generator_mode == "assistants":
                content, filename = self.openai_client.send_prompt_with_assistants(system_prompt, user_prompt, attachments=[file_path])
            else:
                content = self.openai_client.send_prompt(system_prompt, user_prompt, attachments=[file_path])

        # 📝 Agora salva diferente dependendo do generator_mode
        if generator_mode == "assistants":
            # Conteúdo binário e nome real do arquivo
            output_file = os.path.join(output_folder, filename)
            with open(output_file, "wb") as f:
                f.write(content)
        else:
            # Texto puro
            output_file = os.path.join(output_folder, f"{base_name}.{output_type}")
            self.file_manager.save_output(output_file, content, output_type=output_type)

        print(f"✅ Arquivo gerado: {output_file}")



