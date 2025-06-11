import os
import glob 
from dotenv import load_dotenv
import argparse
from utils.openai_client import OpenAIClient
from utils.file_manager import FileManager
from pipeline_runner import PipelineRunner

def clear_console():
    # Limpa a tela dependendo do sistema operacional
    os.system('cls' if os.name == 'nt' else 'clear')

def select_pipeline():
    """Exibe a lista de pipelines disponíveis e permite a seleção de um."""
    clear_console()
    print("🔍 Listando pipelines disponíveis...\n")
    
    # Lista as subpastas em steps_config
    steps_dir = 'steps_config'
    if not os.path.exists(steps_dir):
        os.makedirs(steps_dir)
        print(f"⚠️ A pasta {steps_dir} não existe. Criando...")
        return None
    
    pipelines = [d for d in os.listdir(steps_dir) if os.path.isdir(os.path.join(steps_dir, d))]
    
    if not pipelines:
        print("❌ Nenhum pipeline encontrado. Crie uma subpasta em steps_config para começar.")
        return None
    
    print("Pipelines disponíveis:")
    for i, pipeline in enumerate(pipelines, 1):
        print(f"{i}. {pipeline}")
    
    while True:
        try:
            choice = int(input("\nDigite o número do pipeline que deseja executar (ou 0 para sair): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(pipelines):
                return pipelines[choice - 1]
            print("❌ Número inválido. Tente novamente.")
        except ValueError:
            print("❌ Por favor, digite um número válido.")

def main(debug_mode=False, start_step=1, end_step=None):
    pipeline_name = select_pipeline()
    if pipeline_name is None:
        print("\n프로그램을 종료합니다...")
        return

    print(f"\n🚀 Iniciando Pipeline '{pipeline_name}'...")

    load_dotenv()
    clear_console()  # 🧹 Limpa a tela no início
    openai_client = OpenAIClient()
    file_manager = FileManager()

    # Instancia runner
    runner = PipelineRunner(openai_client, file_manager, debug=debug_mode)

    # Encontra todos os arquivos de steps no pipeline selecionado
    pipeline_dir = os.path.join('steps_config', pipeline_name)
    steps_to_run = sorted(glob.glob(os.path.join(pipeline_dir, '*.yaml')))
    total_steps = len(steps_to_run)

    if not steps_to_run:
        print(f"❌ Nenhum arquivo YAML encontrado em {pipeline_dir}")
        return

    # Executa o pipeline    
    runner.run_pipeline(steps_to_run, pipeline_name=pipeline_name, start_step=start_step, end_step=end_step)

    print("\n✅ Pipeline executado com sucesso.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executa o pipeline de Steps configurados.")
    parser.add_argument("--debug", action="store_true", help="Ativa o modo debug (pausa entre steps).")
    parser.add_argument("--start", type=int, default=1, help="Número do step inicial (default: 1).")
    parser.add_argument("--end", type=int, help="Número do step final (opcional).")
    args = parser.parse_args()

    main(debug_mode=args.debug, start_step=args.start, end_step=args.end)