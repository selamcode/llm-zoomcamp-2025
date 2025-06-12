# Index

-An index is a collection of related documents uniquely identified by a name.

> Think of it like a database table.

- A `document` is a single piece of data in Elasticsearch — stored in JSON format.

- A `field`	Each` key-value` pair inside a document (like username, email, etc.)

Think of it like:

📃 One user profile

Example

lets look at an `index user`.

```
Index: users
├── Document 1 → Sara's profile
├── Document 2 → John's profile
├── Document 3 → Lee's profile
```

##### document-1
```json
{
  "username": "sara92",
  "email": "sara@example.com",
  "signup_date": "2023-12-01",
  "is_active": true
}
```

##### document-2
```json
{
  "username": "john_the_dev",
  "email": "john@devmail.com",
  "signup_date": "2022-07-19",
  "is_active": false
}
```

##### document-3
```json
{
  "username": "lee.k",
  "email": "lee@example.org",
  "signup_date": "2024-05-10",
  "is_active": true
}
```

An example of a field can be

``` json
"email": "sara@example.com",
```
the key is `"email"`, and the value is `"sara@example.com"`


##### How to Add Documents (Indexing)


``` python

doc = {
    "username": "sara92",
    "email": "sara@example.com",
    "signup_date": "2023-12-01",
    "is_active": True,
    "age": 30
}

es.index(index="users", document=doc)

```


##### Metadata fields
An indexed document contains data and metadata. Metadata fields are system fields that store information about the documents. In Elasticsearch, metadata fields are prefixed with an underscore. For example, the following fields are metadata fields:

`_index`: The name of the index where the document is stored.

`_id`: The document’s ID. IDs must be unique per index.`

```json

{
  "_index": "my-first-elasticsearch-index",
  "_id": "DyFpo5EBxE8fzbb95DOa",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "email": "john@smith.com",
    "first_name": "John",
    "last_name": "Smith",
    "info": {
      "bio": "Eco-warrior and defender of the weak",
      "age": 25,
      "interests": [
        "dolphins",
        "whales"
      ]
    },
    "join_date": "2024/05/01"
  }
}

```

##### Mappings and data types

Each index has a mapping or schema for how the fields in your documents are indexed. A mapping defines the data type for each field, how the field should be indexed, and how it should be stored.

In other words:

``` text 
A mapping defines the structure of your documents:

- What fields exist

- What type of data they hold (text, number, date, etc.)

- Whether the field should be searchable, sortable, etc.

- Think of it like a schema in a relational database.

``` 

Example of mapping in python:

``` python

from elasticsearch import Elasticsearch

# Connect to Elasticsearch on localhost
es = Elasticsearch("http://localhost:9200")

# Define the mapping
mapping = {
    "mappings": {
        "properties": {
            "username": {"type": "text"},
            "email": {"type": "keyword"},
            "signup_date": {"type": "date"},
            "is_active": {"type": "boolean"}
        }
    }
}

# Create the index with the mapping
index_name = "users"

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created with mapping.")
else:
    print(f"Index '{index_name}' already exists.")

```

##### What is a Field Data Type?
A field data type tells Elasticsearch what kind of data a field holds — like text, keyword, boolean, date, integer, etc.

##### Common Field Types:

| Field Type | Use Case                                                |
| ---------- | ------------------------------------------------------- |
| `text`     | For full-text search (e.g., names, titles)              |
| `keyword`  | For exact match, sorting, filtering (e.g., email, tags) |
| `boolean`  | True/false values                                       |
| `date`     | For date/time fields                                    |
| `integer`  | Whole numbers                                           |
| `float`    | Decimal numbers                                         |


##### text vs keyword (Most important)

|               | `text`                 | `keyword`             |
| ------------- | ---------------------- | --------------------- |
| Use for       | Search in words        | Exact match/filtering |
| Analyzed      | Yes (split into words) | No (stored as-is)     |
| Example Field | `username`             | `email`               |




##### Now if you lets look at out python code to make sens out of it

| Field Name    | Value                | Type      | Why                                  |
| ------------- | -------------------- | --------- | ------------------------------------ |
| `username`    | `"sara92"`           | `text`    | Searchable by parts (e.g., `"sara"`) |
| `email`       | `"sara@example.com"` | `keyword` | Filter/sort exact email              |
| `signup_date` | `"2023-12-01"`       | `date`    | Sort or filter by time               |
| `is_active`   | `true`               | `boolean` | True/false logic                     |
| `age`         | `30`                 | `integer` | Numeric filters or stats             |



##### What Are settings in Elasticsearch?
In Elasticsearch, settings are configurations for how an index behaves, especially for:

Sharding (splitting data)

Replicas (backup & availability)

Analyzers (how text is processed for search)


##### Think of it like:

> If `mappings` are about what kind of data you're storing, then `settings` are about how that data is stored and searched.

##### Why You Should Use settings

- Better performance

You control how many shards to create. Too many = overhead, too few = bottlenecks.

- High availability

You define how many replicas (copies) of your data exist. More replicas = safer and faster reads.

- Custom search behavior

You can define custom analyzers (like lowercasing, removing punctuation) for more precise full-text search.


##### Example: With settings and mappings Combined


```python

from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

index_name = "users"

settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "username": {"type": "text"},
            "email": {"type": "keyword"},
            "signup_date": {"type": "date"},
            "is_active": {"type": "boolean"},
            "age": {"type": "integer"}
        }
    }
}

# Create the index with settings and mappings
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=settings)
    print(f"Index '{index_name}' created with custom settings.")
else:
    print(f"Index '{index_name}' already exists.")

```




| Tip                                                                      | Why It Matters                                                     |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Set your settings *before* adding data**                            | You can't change some things later (like shard count)              |
| **1 shard + 1 replica is fine**                                       | Great for small projects and local testing                         |
|  **Replicas = backups**                                                | If 1 machine goes down, your data is still safe                    |
|  **Shards = slices of your data**                                      | Elasticsearch splits your index into smaller parts for faster work |
|  You **can change the number of replicas later**                       | No need to worry about it upfront                                  |
| You **cannot change the number of shards after the index is created** | So plan ahead for big apps                                         |
| You usually **don’t need custom analyzers** at first                  | Stick with defaults unless you’re doing complex text search        |
|  Use custom settings only if you know why                              | Otherwise the defaults are fine to start with                      |
