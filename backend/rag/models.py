from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from sentence_transformers import CrossEncoder
from config import OPENAI_MODEL, EMBEDDING_MODEL, RERANKER_MODEL, OPENAI_API_KEY

# Инициализация эмбеддингов
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=OPENAI_API_KEY
)

# Инициализация LLM
openai_llm = ChatOpenAI(
    temperature=0,
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY
)

# Инициализация CrossEncoder для реранкинга
cross_encoder = CrossEncoder(RERANKER_MODEL) 