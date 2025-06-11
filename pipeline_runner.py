import importlib
from steps.prompt_step import PromptStep
from steps.custom_step import CustomStep
import yaml

class PipelineRunner:
    def __init__(self, openai_client, file_manager, debug=False):
        self.openai_client = openai_client
        self.file_manager = file_manager
        self.debug = debug

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def run_step(self, step_config):
        step_type = step_config.get("step_type", "prompt")

        if step_type == "prompt":
            from steps.prompt_step import PromptStep
            step = PromptStep(step_config, self.openai_client, self.file_manager)
        else:
            class_name = step_config.get("class_name", "CustomStep")
            module = importlib.import_module(f"steps.{self._camel_to_snake(class_name)}")
            StepClass = getattr(module, class_name)
            step = StepClass(step_config, self.file_manager)

        step.run()

    def run_pipeline(self, config_files, pipeline_name=None, start_step=1, end_step=None):
        total_steps = len(config_files)

        if end_step is None:
            end_step = total_steps

        steps_to_run = config_files[start_step-1:end_step]

        print(f"🚦 Executando steps {start_step} até {end_step}...\n")

        for real_index, config_path in enumerate(range(start_step, end_step + 1), start=start_step):
            step_config = self.load_config(config_files[real_index-1])
            step_config['pipeline_name'] = pipeline_name  # Adiciona o nome do pipeline à configuração
            step_name = step_config.get('step_name', f'Step {real_index}')

            print(f"[{real_index}/{total_steps}] 🚀 Executando Step: {step_name}\n")
            
            self.run_step(step_config)

            if self.debug:
                input(f"[DEBUG] Step '{step_name}' concluído. Pressione Enter para continuar...")

            print("\n")  # 🆕 Separador depois de cada Step (opcional)

    def _camel_to_snake(self, name):
        import re
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)  # <-- r'string' e uma barra só
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
