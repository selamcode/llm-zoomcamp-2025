import requests
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm
import time
from elasticsearch import Elasticsearch

load_dotenv()

# Initialize Elasticsearch client
es_client = Elasticsearch("http://localhost:9200/")
index_name = "course-questions"

# Print ES connection info
print("Elasticsearch Info:", es_client.info())

# Check if the index has data
doc_count = es_client.count(index=index_name)['count']
print(f"📦 Total documents in '{index_name}': {doc_count}")

# If no documents, fetch and index them
if doc_count == 0:
    print("Index is empty. Fetching and indexing data...")
    docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
    docs_response = requests.get(docs_url)
    documents_raw = docs_response.json()

    documents = []
    for course in documents_raw:
        for doc in course['documents']:
            doc['course'] = course['course']
            documents.append(doc)

    for doc in tqdm(documents, desc="Indexing"):
        es_client.index(index=index_name, document=doc)

# Function to perform the search and return top score + question
def get_top_score(query):
    search_query = {
        "size": 5,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["question^4", "text"],
                "type": "best_fields"
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    hits = response['hits']['hits']

    if not hits:
        return None, "No results found"

    top_hit = hits[0]
    score = round(top_hit['_score'], 2)
    question = top_hit['_source'].get('question', 'N/A')
    return score, question

# Q3 query
query = "How do execute a command on a Kubernetes pod?"

# Run query and print result
score, question = get_top_score(query)
print(f"\nTop score: {score}")
print(f"Top matching question: {question}")
