from langchain_groq.chat_models import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import GROQ_API_KEY

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0.3
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
