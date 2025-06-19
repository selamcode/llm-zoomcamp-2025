# python -m pip install -q "qdrant-client[fastembed]>=1.14.2"

from qdrant_client import QdrantClient # for client 
import requests 
from qdrant_client import models # we need the model because we use them to embed
import uuid

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
if not collection_name:
    client.create_collection(
        sparse_vectors_config = {
            "bm25" : models.SparseVectorParams(
                modifier = models.Modifier.IDF, # IDF is a way to rank in BM25
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


"Now lets do our sparse vector search with BM25"


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


