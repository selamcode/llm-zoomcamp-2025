import requests
from openai import OpenAI
from  dotenv import load_dotenv 

# for prgress bar purpose 
from tqdm import tqdm
import time

# Import Elasticsearch client library
from elasticsearch import Elasticsearch



load_dotenv() # Load variables from .env

# URL of the JSON file hosted on GitHub (contains all courses and their FAQ documents)
docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'

# Send an HTTP GET request to fetch the JSON data from the URL
docs_response = requests.get(docs_url)

# Parse the JSON response into a Python list (each item = a course with documents)
documents_raw = docs_response.json()

# This will store the final flattened list of documents (one item per FAQ)
documents = []

# Loop through each course and its documents (the first list in the structure -> ['course', 'documents'])
for course in documents_raw:
    course_name = course['course']  # Get the name of the course (e.g., "ml-zoomcamp")

    # For every document (question/answer) in the course
    for doc in course['documents']:
        doc['course'] = course_name  # Add the course name to each document
        documents.append(doc)        # Store the enriched document in the final list

# Import Elasticsearch client library
from elasticsearch import Elasticsearch

# Create an Elasticsearch client to connect to the running instance
es_client = Elasticsearch("http://localhost:9200/")

# Print ES server info to confirm connection
print(es_client.info())

# Elasticsearch index settings and mappings
index_settings = {
  "settings": {
    "number_of_shards": 1,       # Dev mode: 1 shard
    "number_of_replicas": 0      # Dev mode: no replicas
  },
  "mappings": {
    "properties": {
      "question": {
        "type": "text"           # For full-text search
      },
      "text": {
        "type": "text"           # For full-text search
      },
      "section": {
        "type": "text"           # Allows search on section content
      },
      "course": {
        "type": "keyword"        # For filtering by course name
      }
    }
  }
}

# Name of the index
index_name = "course-questions"

# Create the index in Elasticsearch with the defined settings
# es_client.indices.create(index=index_name, body=index_settings)

if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name, body=index_settings)
        print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists. Skipping creation.")

# Progress bar tool for visualizing data indexing
'''
# if you don't want moder look
from tqdm.auto import tqdm

Index all the documents one by one into the ES index
for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)
    
'''

for i in tqdm(range(10), desc="📦 Indexing", ncols=100, bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt}"):
    time.sleep(0.1)



# Example query to test the full pipeline
# query 1
query = 'I just discovered the course. Can I still join it?'

# query 2
#query = '"How do execute a command on a Kubernetes pod?"'

# query 2
# query = "How do copy a file to a Docker container?" 



# Define function to search in Elasticsearch
def elastic_search(query):
    search_query = {
        "size": 5,  # Limit results to top 5
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],  # Boost `question`
                        "type": "best_fields"  # Match best field
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"  # Only return results from this course
                    }
                }
            }
        }
    }
    

    # Send the search query to ES
    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    # Extract only the document sources (excluding metadata)
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs


print("The top 5 results of elasticsearch\n")
print(elastic_search(query))
print("\n")


# Template builder: Converts search results into prompt format
def build_prompt(query, search_results):
    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    # Construct context from each document
    for doc in search_results:
         # context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
        context = context + f"question: {doc['question']}\nanswer: {doc['text']}\n\n"
        
    # Fill the template with actual content
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

# Initialize the OpenAI API client
client = OpenAI()

# Ask the LLM to answer the prompt
def llm(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # Model version
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# Retrieval-Augmented Generation (RAG) pipeline
def rag(query):
    search_results = elastic_search(query)       # Retrieve documents
    prompt = build_prompt(query, search_results) # Build prompt from retrieved docs
    answer = llm(prompt)                          # Generate LLM answer
    return answer

# Run the full RAG pipeline with the query
print("RAG answer")
print(rag(query))
