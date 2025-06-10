# Q5 prompt building

import requests
from openai import OpenAI
from dotenv import load_dotenv

from tqdm import tqdm
import time

from elasticsearch import Elasticsearch

load_dotenv()

es_client = Elasticsearch("http://localhost:9200/")
index_name = "course-questions"

print(es_client.info())

def get_top_3_unique_answers(query):
    search_query = {
        "size": 10,  # Fetch more to have room to filter duplicates
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^4", "text"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "machine-learning-zoomcamp"
                    }
                }
            }
        }
    }
    response = es_client.search(index=index_name, body=search_query)

    seen_answers = set()
    unique_results = []
    for hit in response['hits']['hits']:
        answer = hit['_source'].get('text', 'N/A').strip()
        if answer not in seen_answers:
            seen_answers.add(answer)
            unique_results.append(hit)
        if len(unique_results) >= 3:
            break

    return unique_results


query = "How do copy a file to a Docker container?"
results = get_top_3_unique_answers(query)

print(f"Top 3 unique answers for query: '{query}'\n")

for i, hit in enumerate(results, start=1):
    score = round(hit['_score'], 2)
    question = hit['_source'].get('question', 'N/A')
    answer = hit['_source'].get('text', 'N/A')
    print(f"Result #{i}")
    print(f"Score: {score}")
    print(f"Question: {question}")
    print(f"Answer: {answer}\n")
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



def get_top_3_docs(query):
    search_query = {
        "size": 3,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^4", "text"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "machine-learning-zoomcamp"
                    }
                }
            }
        }
    }
    response = es_client.search(index=index_name, body=search_query)
    return [hit['_source'] for hit in response['hits']['hits']]


docs = get_top_3_docs("How do copy a file to a Docker container?")
for i, doc in enumerate(docs, 1):
    print(f"{i}. {doc['question']}")

context_template = """
Q: {question}
A: {text}
""".strip()

prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

# Build the context from Q4 results
context = "\n\n".join([
    context_template.format(question=doc['question'], text=doc['text']) for doc in docs
])

# Q5 question
query_q5 = "How do I execute a command in a running docker container?"

# Build final prompt
final_prompt = prompt_template.format(question=query_q5, context=context)

# Print prompt length
print(f"\n🔍 Length of prompt: {len(final_prompt)}")
