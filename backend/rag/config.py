import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Базовые пути
BASE_DIR = Path(__file__).parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
PDF_DIR = BASE_DIR / "pdf_files"

# Настройки модели
OPENAI_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"
RERANKER_MODEL = "BAAI/bge-reranker-large"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройки токенизации
TOKEN_MODEL = "gpt-4o"

# Настройки разделения текста
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Настройки поиска
BM25_K = 5
VECTOR_STORE_K = 5
RERANKER_TOP_N = 3

# Настройки ансамбля
ENSEMBLE_WEIGHTS = [0.6, 0.4]

# Настройки ценообразования OpenAI (по состоянию на март 2024)
INPUT_COST_PER_1M = 0.150  # $0.150 за 1M входных токенов
OUTPUT_COST_PER_1M = 0.600  # $0.600 за 1M выходных токенов 