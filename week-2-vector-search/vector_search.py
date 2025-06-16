from qdrant_client import QdrantClient, models
import requests

client = QdrantClient("http://localhost:6333")



docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()