# python -m pip install -q "qdrant-client[fastembed]>=1.14.2"

from qdrant_client import QdrantClient # for client 
import requests 
from qdrant_client import models # we need the model because we use them to embed
import uuid
import json, random

client = QdrantClient("http://localhost:6333")
client.get_collections()

""" Step 1 Sparse vector search with BM25 """

# get the documnet
docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()


""" 
let's create our collection and since we will be using BM25 we will configure it 
that way

"""
collection_name = "zoomcamp-sparse"

# Ask Qdrant for the actual list of collections
existing_collections = client.get_collections().collections
existing_names = {col.name for col in existing_collections}

if collection_name not in existing_names:
    client.create_collection(
        collection_name=collection_name,
        sparse_vectors_config={
            "bm25": models.SparseVectorParams(
                modifier=models.Modifier.IDF,
            )
        }
    )



""" FastEmbed comes with a BM25 implementation that we can use as any other model. """

# lets send point to the collection


client.upsert(
    
    collection_name = collection_name,
    points = [
        
        models.PointStruct(
            
            # uuid.uuid4() generates a random unique ID.
            # .hex turns it into a 32-character hexadecimal string (letters and numbers).
            
            id = uuid.uuid4().hex,
            vector = {
                "bm25" : models.Document(
                    text = doc["text"],
                    model = "Qdrant/bm25",
                ),
            },
            payload = {
                
                "text":doc["text"],
                "section": doc["section"],
                "course":course["course"],
            }
        )
        for course in documents_raw
        for doc in course["documents"]
    ]
    
)


" Step 3, now lets do our sparse vector search with BM25"


def search(query: str, limit: int =1)->list[models.ScoredPoint]:
    
    results = client.query_points(
        
        collection_name = collection_name,
        query = models.Document(
            text = query,
            model= "Qdrant/bm25",
        ),
        
        using = "bm25",
        limit = limit,
        with_payload = True,
    )
    
    return results.points

results = search("docker", 1)

print(results)

'''choose a random documents'''

random.seed(202506)

course = random.choice(documents_raw)
course_piece = random.choice(course["documents"])
print(json.dumps(course_piece, indent=2))

results = search(course_piece["question"])
print(results[0].payload["text"])



print("\n next let's do a hybrid search \n")

""" we do sparse and then dense """


collection_name = "zoomcamp-sparse-and-dense"
existing_collections = client.get_collections().collections
existing_names = {col.name for col in existing_collections}

if collection_name not in existing_names:
    client.create_collection(
        collection_name=collection_name,
    
        vectors_config={
            # Named dense vector for jinaai/jina-embeddings-v2-small-en
            "jina-small": models.VectorParams(
                size=512,
                distance=models.Distance.COSINE,
            ),
        },
        sparse_vectors_config={
            "bm25": models.SparseVectorParams(
                modifier=models.Modifier.IDF,
            )
        }
    )
 
 
# lets insert our points into the new collection    
client.upsert(
    collection_name= collection_name,
    points=[
        models.PointStruct(
            id=uuid.uuid4().hex,
            vector={
                "jina-small": models.Document(
                    text=doc["text"],
                    model="jinaai/jina-embeddings-v2-small-en",
                ),
                "bm25": models.Document(
                    text=doc["text"], 
                    model="Qdrant/bm25",
                ),
            },
            payload={
                "text": doc["text"],
                "section": doc["section"],
                "course": course["course"],
            }
        )
        for course in documents_raw
        for doc in course["documents"]
    ]
)


# lets do the search function (basically hybrid search)

def multi_stage_search(query: str, limit: int = 1) -> list[models.ScoredPoint]:
    results = client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=models.Document(
                    text=query,
                    model="jinaai/jina-embeddings-v2-small-en",
                ),
                using="jina-small",
                # Prefetch ten times more results, then
                # expected to return, so we can really rerank
                limit=(10 * limit),
            ),
        ],
        query=models.Document(
            text=query,
            model="Qdrant/bm25", 
        ),
        using="bm25",
        limit=limit,
        with_payload=True,
    )

    return results.points

print(json.dumps(course_piece, indent=2))

results = multi_stage_search(course_piece["question"])
print(results[0].payload["text"])




# lets look at  Reciprocal Rank Fusion (RRF)
# we basically give the hybrid search a rank based on dense and parse score

'''
look here for more understanding 

| Document | Dense Ranking | Sparse Ranking | RRF Score | Final Ranking |
| -------- | ------------- | -------------- | --------- | ------------- |
| D1       | 1             | 5              | 0.0318    | 2             |
| D2       | 2             | 4              | 0.0317    | 3             |
| D3       | 3             | 2              | 0.0320    | 1             |
| D4       | 4             | 3              | 0.0315    | 5             |
| D5       | 5             | 1              | 0.0318    | 2             |

'''

'''
Reranking
Reranking is a broader term related to Hybrid Search. 
Fusion is one of the ways to rerank the results of 
multiple methods (dense and sparse in this case)
'''
# let's implement the RRF search 
def rrf_search(query: str, limit: int = 1) -> list[models.ScoredPoint]:
    results = client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=models.Document(
                    text=query,
                    model="jinaai/jina-embeddings-v2-small-en",
                ),
                using="jina-small",
                limit=(5 * limit),
            ),
            models.Prefetch(
                query=models.Document(
                    text=query,
                    model="Qdrant/bm25",
                ),
                using="bm25",
                limit=(5 * limit),
            ),
        ],
        # Fusion query enables fusion on the prefetched results
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        with_payload=True,
    )

    return results.points


print("\n lets do the RRF search. \n")
results = rrf_search(course_piece["question"])
print(json.dumps(course_piece, indent=2))
print(results[0].payload["text"])



