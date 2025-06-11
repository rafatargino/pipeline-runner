
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o"
OUTPUT_DIR = "outputs/"

CLOUDINARY_CLOUD_NAME = "drurz3ji6"
CLOUDINARY_API_KEY = "953762393559534"
CLOUDINARY_API_SECRET = "0iV4qOQ71z747vCFe-dtdwXek2A"

# Período configurável
DATA_INICIO = "2025-05-01"
DATA_FIM = "2025-05-31"

# Funcionalidades para análise
FUNCIONALIDADES = ["ação_educacional"]
