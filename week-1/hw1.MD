### elasticsearch
- setting up elasticsearch and run it. we use docker to do so
---
``` docker
docker run -it --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:9.0.2
```
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







