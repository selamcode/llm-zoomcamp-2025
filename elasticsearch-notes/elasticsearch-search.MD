### Search in Elasticsearch

##### Concept	Explanation

| Concept                                               | Explanation                                                                                                     |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 🔹 **Search happens inside an index**                 | You always tell Elasticsearch *which* index to search (e.g., `users`)                                           |
| 🔹 **Queries are written in JSON format**             | You send JSON to describe what you want to find                                                                 |
| 🔹 **Search by field**                                | You can target specific fields like `username` or `email`                                                       |
| 🔹 **Full-text search vs exact match**                | Use `match` for searching text fields (partial matches), and `term` for exact matches on keyword or other types |
| 🔹 **Distributed search**                             | Elasticsearch searches all shards and merges the results                                                        |
| 🔹 **Search returns documents that match your query** | The response contains the documents with their data and some extra info                                         |

</br>

What is `['hits']['hits']` in the Search Result?
When you run a search, Elasticsearch returns a JSON response with layers of information.
</br>

> hits (first level) — overall info about how many matches there are, how long the search took, etc.

> hits (second level, inside the first hits) — the actual list of documents matching your search.

</br>

Example response structure:

``` json

{
  "hits": {             <-- overall search info
    "total": 3,         <-- number of documents found
    "max_score": 1.0,
    "hits": [           <-- list of matching documents
      {
        "_index": "users",
        "_id": "1",
        "_score": 1.0,
        "_source": {    <-- the actual document data
          "username": "sara92",
          "email": "sara@example.com",
          "signup_date": "2023-12-01",
          "is_active": true
        }
      },
      {...}, {...}
    ]
  }
}
```

So, to get the matching documents, you look inside:


##### Python Examples Full-text search with `match`

``` python
query = {
  "query": {
    "match": { "username": "sara" }
  }
}

response = es.search(index="users", body=query)
documents = response['hits']['hits']

for doc in documents:
    print(doc['_source'])
This finds users whose usernames contain “sara” (analyzed, partial match).

```

##### Exact match with `term`

```python
query = {
  "query": {
    "term": { "email.keyword": "sara@example.com" }
  }
}

response = es.search(index="users", body=query)
documents = response['hits']['hits']

for doc in documents:
    print(doc['_source'])

```
This finds users whose email exactly matches `sara@example.com.`

</br>

> Note: Use .keyword on text fields to perform exact matches because email might be mapped as text with analyzed tokens.