
# Pipeline Runner

Um sistema flexível para execução de pipelines configuráveis usando o OpenAI GPT.

## 📦 Estrutura do Projeto

```
pipeline_runner/
├── main.py
├── config.py
├── steps_config/
│   ├── pipeline1/
│   │   ├── step1.yaml
│   │   ├── step2.yaml
│   │   └── step3.yaml
│   ├── pipeline2/
│   │   ├── step1.yaml
│   │   └── step2.yaml
│   └── pipeline3/
│       ├── step1.yaml
│       └── step2.yaml
├── utils/
│   ├── openai_client.py
│   └── file_manager.py
├── data/
│   ├── pipeline1/
│   │   ├── input/
│   │   ├── step1/
│   │   ├── step2/
│   │   └── step3/
│   ├── pipeline2/
│   │   ├── input/
│   │   ├── step1/
│   │   └── step2/
│   └── pipeline3/
│       ├── input/
│       ├── step1/
│       └── step2/
└── logs/
    └── pipeline1/
        └── {ano-mes-dia}/
            ├── pipeline.log
            └── step_logs/
```

## 📝 Sobre os Pipelines

O sistema agora suporta múltiplos pipelines configuráveis:

1. **Criar um novo pipeline**:
   - Crie uma nova subpasta dentro de `steps_config`
   - Adicione arquivos YAML com as configurações dos steps
   - Crie subpastas correspondentes em `data/{pipeline_name}` para input e output
   - Os arquivos serão executados em ordem alfabética

2. **Estrutura dos arquivos YAML**:
   - Cada arquivo YAML deve conter as configurações para um step do pipeline
   - O nome do arquivo deve seguir o padrão `stepX.yaml`
   - Caminhos de arquivos devem ser relativos à pasta do pipeline

3. **Seleção de Pipeline**:
   - Ao executar o programa, você verá uma lista de todos os pipelines disponíveis
   - Selecione o pipeline desejado pelo número correspondente
   - Pressione 0 para sair do programa

## 🚀 Como Executar

1. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

2. **Configure a API Key**:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da OpenAI: `OPENAI_API_KEY=sua-chave-aqui`

3. **Crie seus pipelines**:
   - Crie subpastas dentro de `steps_config` para cada pipeline
   - Adicione arquivos YAML com as configurações dos steps dentro de cada pasta

4. **Execute o programa**:
```bash
python main.py
```

## 📝 Sobre os Pipelines

O sistema agora suporta múltiplos pipelines configuráveis:

1. **Criar um novo pipeline**:
   - Crie uma nova subpasta dentro de `steps_config`
   - Adicione arquivos YAML com as configurações dos steps
   - Os arquivos serão executados em ordem alfabética

2. **Estrutura dos arquivos YAML**:
   - Cada arquivo YAML deve conter as configurações para um step do pipeline
   - O nome do arquivo deve seguir o padrão `stepX.yaml`

3. **Seleção de Pipeline**:
   - Ao executar o programa, você verá uma lista de todos os pipelines disponíveis
   - Selecione o pipeline desejado pelo número correspondente
   - Pressione 0 para sair do programa

## 🛠️ Modos de Execução

### Modo Normal
```bash
python main.py
```

### Modo Debug (pausa entre passos)
```bash
python main.py --debug
```

- No modo debug, o programa pausa após cada step
- Pressione ENTER para continuar para o próximo step

### Especificar Range de Steps
```bash
python main.py --start 2 --end 4
```

- `--start`: Número do step inicial (default: 1)
- `--end`: Número do step final (opcional)

## 📚 Outputs

Os arquivos gerados ficam salvos na pasta `outputs`:
- Cada execução cria uma subpasta com timestamp
- Arquivos de saída são salvos com nomes descritivos
- Logs de execução são mantidos para cada pipeline

## ✨ Funcionalidades

- Suporte a múltiplos pipelines configuráveis
- Interface interativa para seleção de pipeline
- Modo debug para inspeção manual
- Configuração via arquivos YAML
- Logging detalhado de execuções
- Suporte a variáveis de ambiente

## 🔒 Requisitos

- Python 3.8+
- API Key válida da OpenAI (modelo `gpt-4o` recomendado)
