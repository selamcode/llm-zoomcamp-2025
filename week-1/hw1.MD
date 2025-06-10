### elasticsearch
- setting up elasticsearch and run it. we use docker to do so
---
``` docker
docker run -it --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:9.0.2
```
---
</br>

| Part                           | Meaning                                      |
|-------------------------------|----------------------------------------------|
| `docker run`                  | Run a new Docker container                    |
| `-it`                        | Interactive mode (see logs, interact)        |
| `--name elasticsearch`        | Name the container                            |
| `-p 9200:9200`               | Map host port 9200 → container port 9200 (HTTP API) |
| `-p 9300:9300`               | Map host port 9300 → container port 9300 (node communication) |
| `-e "discovery.type=single-node"` | Run as single-node (no clustering)        |
| `-e "xpack.security.enabled=false"` | Disable security (no auth)                 |
| `docker.elastic.co/elasticsearch/elasticsearch:9.0.2` | Use Elasticsearch 9.0.2 image           |



##### Q1, What's the version.build_hash value?
Run you elastic search, then when you go to http://localhost:9200/, you will see a JSON, then you will see different key-value pairs. one of those is "build_hash".

or you could run the following command on Terminal and you will see the JSON output

```curl localhost:9200```


##### Answer
    
        ``` docker
        "build_hash" : "0a58bc1dc7a4ae5412db66624aab968370bd44ce",
        ```

### Getting the data

Now let's get the FAQ data. You can run this snippet:

``` python

import requests 

docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)
```

What is the top code doing:

The links take you to a location where there is a JSON file. The JSON file is the JSON format of the FAQ document. 

The Structure of the JSON for our FAQ looks like the this:

```JSON
[
  {
    "course": "string",
    "documents": [
      {
        "question": "string",
        "text": "string",
        "section": "string"
      }
    ]
  }
]
```

`courses` are courses being though by Datatalks.

- Machine Learning Zoomcamp	
- Data Engineering Zoomcamp	
- MLOps Zoomcamp	
- Stock Markets Analytics Zoomcamp	
- LLM Zoomcamp

`documents` is a list of questions and answers inside each course. Each item in this list has:

- a question (the FAQ)
- an answer (called text)
- and a section (which tells the category or type of the question)

The above python code will give something that loos like this

``` json
[
  {
    "question": "What is Python?",
    "text": "Python is a programming language.",
    "section": "basics",
    "course": "Zoomcamp"
  },
  {
    "question": "What is Docker?",
    "text": "Docker is a container system.",
    "section": "tools",
    "course": "Zoomcamp"
  },
  {
    "question": "What is Machine Learning?",
    "text": "ML is teaching computers to learn from data.",
    "section": "intro",
    "course": "ML Course"
  }
]
```
This is easier to work with.

now that we cleaned up the JSON for the FAQs document, it is ready for we elasticserch. Now will configures our elasticserch settings and mappings.


#####  What Are Elasticsearch Settings and Mappings?

>  When you create an `index` in Elasticsearch (like creating a table in a database), you can specify:

> `Settings` — how Elasticsearch should store the data (e.g., how many copies, performance tuning).

> `Mappings` — what kind of data each field holds and how it should behave when searching.

``` python
index_settings = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "question": {
        "type": "text"
      },
      "text": {
        "type": "text"
      },
      "section": {
        "type": "text"
      },
      "course": {
        "type": "keyword"
      }
    }
  }
} 
```


##### What Are number_of_shards and number_of_replicas?

`shards`
Elasticsearch splits your data into shards (smaller pieces) to allow parallel processing.

`number_of_shards`: 1 means all data is in one chunk (fine for dev/testing).

`replicas`
A replica is a backup of your shard.

`number_of_replicas`: 0 means no backup copy — faster, but risky for production.


| Term       | Meaning                                             |
| ---------- | --------------------------------------------------- |
| `text`     | Analyzed, tokenized, used for full-text search      |
| `keyword`  | Not analyzed, used for filtering and exact matching |
| `type`     | Tells Elasticsearch how to store and search a field |




``` python
# Name of the index
index_name = "course-questions"

# Create the index in Elasticsearch with the defined settings
es_client.indices.create(index=index_name, body=index_settings)

# Progress bar tool for visualizing data indexing
from tqdm.auto import tqdm

# Index all the documents one by one into the ES index
for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)


# Example query to test the full pipeline
query = 'I just discovered the course. Can I still join it?'


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


```

#####  1. Create the Index
``` python
index_name = "course-questions"
es_client.indices.create(index=index_name, body=index_settings) 

```
- `index_name`: This is like naming a folder in Elasticsearch to store your data (in this case, FAQ questions).

- `index_settings`: This tells Elasticsearch how to store and search the data (e.g. which fields to analyze, how many copies to keep).

- `es_client.indices.create(...)`: Creates that "folder" with the rules/settings.

##### 2. Indexing the Data

``` python

from tqdm.auto import tqdm  # Just shows a loading bar in the terminal

for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)

```
- documents is a list of all your FAQ entries.

- Loop through every document (each question/answer).

- es_client.index(...): Sends each document to Elasticsearch so it's searchable later.


##### 3. Writing a Search Function

``` python
query = 'I just discovered the course. Can I still join it?'
```
This is an example search input — something a user might type.

##### 4. elastic_search(query) Function
This function searches for the query you give it.

``` python

search_query = {
    "size": 5,  # Return top 5 results 
```
→ You only want the top 5 most relevant matches.

``` python
"query": {
    "bool": {
        "must": {
            "multi_match": {
                "query": query,
                "fields": ["question^3", "text", "section"],
                "type": "best_fields"
            }
        },
  ```
- multi_match: Try to match the query in multiple fields (question, text, section).

- "question^3": Boost the importance of matches in the question field (like saying “if the query matches the question, give it 3x the weight”).

- "type": "best_fields": Elasticsearch will pick the best matching field for each document.

``` python
"filter": {
    "term": {
        "course": "data-engineering-zoomcamp"
    }
}
```

- This part filters results to only return ones from the data-engineering-zoomcamp course.

- Even if other courses have good answers, they will be excluded.

##### 5. Getting the Results

```python

response = es_client.search(index=index_name, body=search_query)

```
- Sends your search query to Elasticsearch.

- Gets back a bunch of matching documents, along with metadata.

``` python
result_docs = []
for hit in response['hits']['hits']:
    result_docs.append(hit['_source'])

```
- Loop through the results.
- hit['_source']: Grabs just the original document (question/answer/etc.), ignoring metadata like scores, ids, etc.

- Append them to result_docs, so they’re ready to be used (like for showing to the user or sending to GPT).



### Looking at `response` from `es_client.search()` inside the `elastic_search` function

This is the result you get back from Elasticsearch after doing a .search().

The structure looks like this:

```json
{
  "hits": {
    "total": { "value": 5, ... },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "course-questions",
        "_id": "abc123",
        "_score": 1.0,
        "_source": {
          "question": "...",
          "text": "...",
          "section": "...",
          "course": "..."
        }
      },
      ...
    ]
  }
}
```

##### So what is hit?

```response['hits']['hits']``` is a list of results.

Each item in that list is called a "hit" — it represents one matching document.

So this line:

``` python
for hit in response['hits']['hits']:
```

Means:
Go through each search result (i.e., document match).

###### `What is hit['_source']?`

`"_source"` contains the actual document data you originally indexed:

``` json
{
  "question": "...",
  "text": "...",
  "section": "...",
  "course": "..."
}
```
So this line:

``` python
result_docs.append(hit['_source'])
```
Means:

- From each search result, grab the original document content (i.e., the actual question/answer) and store it in your result_docs list.

`Final Summary`

| Part               | Meaning                                        |
| ------------------ | ---------------------------------------------- |
| `hit`              | One result/document returned by Elasticsearch  |
| `hit['_source']`   | The actual content of that document (your FAQ) |
| `['hits']['hits']` | List of all matched documents                  |


Even though we clean up our docment and only index the fields you care about (like `question`, `text`, `section`, `course`), Elasticsearch automatically adds metadata to every document when it stores it. that's why we needed to clean up again 

```python

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
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    # Fill the template with actual content
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

# 🔧 Initialize the OpenAI API client
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
rag(query)

```

### 1. `build_prompt(query, search_results)`
- Takes the user's question and the top-matching documents.
- Builds a clear prompt like:
  > You're a teaching assistant... here's the question... here's the context...
- Formats each document into a structured block of:


### 2. `llm(prompt)`
- Sends the prompt to OpenAI’s `gpt-3.5-turbo-1106`.
- Gets a generated answer back from the language model.

### 3. `rag(query)`
- This is the full pipeline:
1. Searches Elasticsearch for relevant FAQs.
2. Builds a prompt from them.
3. Sends the prompt to the LLM.
4. Returns the final answer.


### Answers to the Questions

##### answer 1

```docker

docker run -it --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.17.6

```
##### answer 2

index

##### answer 3

44.50

##### answer 4


How do I copy files from a different folder into docker container’s working directory?

##### answe 5

1446

##### answe 6

320