import os
from dotenv import load_dotenv
from llama_index.core import Settings
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv()

MEM0_API_KEY = os.environ['MEM0_API_KEY']
GROQ_API_KEY = os.environ['GROQ_API_KEY']
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_API_BASE = os.environ["OPENAI_API_BASE"]

CHAT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-ada-002"
STORE_DIRECTORY = "../data/store/nutritional_db"
STORE_COLLECTION = "nutritional_hypotheticals"

# Initialize LLM
llm = ChatOpenAI(
    openai_api_base=OPENAI_API_BASE,
    openai_api_key=OPENAI_API_KEY,
    model=CHAT_MODEL,
    streaming=False
)

# Initialize embedding model
embedding_model = OpenAIEmbeddings(
    openai_api_base=OPENAI_API_BASE,
    openai_api_key=OPENAI_API_KEY,
    model=EMBEDDING_MODEL
)

# Initialize the OpenAI embedding function for Chroma
embedding_function = OpenAIEmbeddingFunction(
    api_base=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY,
    model_name=EMBEDDING_MODEL
)

# Set global defaults in LlamaIndex
Settings.llm = llm
Settings.embedding = embedding_model
