import requests
import json
import random
from qdrant_client.http.exceptions import UnexpectedResponse # when creating collections, I need to skip if already created
from qdrant_client import QdrantClient, models

# choose a model
from fastembed import TextEmbedding

 #connecting to local Qdrant instance
client = QdrantClient("http://localhost:6333")

# get the document we will work on 
docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()
# print(documents_raw)


''' lets pick out text model '''

EMBEDDING_DIMENSIONALITY = 512 # dimention

# let's filter the models with 512 dimention
# TextEmbedding.list_supported_models() # shows you different types of textembedding modelsEMBEDDING_DIMENSIONALITY = 512
for model in TextEmbedding.list_supported_models():
    if model["dim"] == EMBEDDING_DIMENSIONALITY:
        pass
       # print(json.dumps(model, indent=2))
    
# one good model to choose is, so let pick that as our model               
model_handle = "jinaai/jina-embeddings-v2-small-en"



''' Create a Collection'''

# Define the collection name
collection_name = "zoomcamp-rag"

# Create the collection with specified vector parameters
try: 
    # creating if the collection donesn't exist
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size = EMBEDDING_DIMENSIONALITY,  # Dimensionality of the vectors
            distance=models.Distance.COSINE  # Distance metric for similarity search
        )
    )
except UnexpectedResponse as e:
    if "already exists" in str(e):
        print("Collection already exists. Skipping creation.")
    else:
        raise e
    



    
    
''' Step 5: Create, Embed & Insert Points into the Collection '''

''' Points are the core data entities in Qdrant. Each point consists of: '''

points = []
id = 0

for course in documents_raw:
    for doc in course['documents']:

        point = models.PointStruct(
            id=id,
            vector=models.Document(text=doc['text'], model=model_handle), #embed text locally with "jinaai/jina-embeddings-v2-small-en" from FastEmbed
            payload={
                "text": doc['text'],
                "section": doc['section'],
                "course": course['course']
            } #save all needed metadata fields
        )
        # we are adding "point" which contains payload and the vectorized array (the embedded object)
        points.append(point)

        id += 1
        
        
''' Then, the generated points will be upserted (inserted) into the collection, and the vector index will be built.'''

client.upsert(
    collection_name=collection_name,
    points=points
)



'''  Run similarity Search '''

def search(query, limit=1):

    results = client.query_points(
        collection_name=collection_name,
        query=models.Document( #embed the query text locally with "jinaai/jina-embeddings-v2-small-en"
            text=query,
            model=model_handle 
        ),
        limit=limit, # top closest matches
        with_payload=True #to get metadata in the results
    )

    return results

''' let's pick a random question '''


course = random.choice(documents_raw)
course_piece = random.choice(course['documents'])
print(json.dumps(course_piece, indent=2))

result = search(course_piece['question'])

print(result)
print("\n")

print(f"Question:\n{course_piece['question']}\n")
print("Top Retrieved Answer:\n{}\n".format(result.points[0].payload['text']))
print("Original Answer:\n{}".format(course_piece['text']))


print("\n")
print(search("What if I submit homeworks late?").points[0].payload['text'])


''' running similarity search with filters'''

client.create_payload_index(
    collection_name=collection_name,
    field_name="course",
    field_schema="keyword" # exact matching on string metadata fields
)

''' lets's upadte the search function'''
def search_in_course(query, course="mlops-zoomcamp", limit=1):

    results = client.query_points(
        collection_name=collection_name,
        query=models.Document( #embed the query text locally with "jinaai/jina-embeddings-v2-small-en"
            text=query,
            model=model_handle
        ),
        query_filter=models.Filter( # filter by course name
            must=[
                models.FieldCondition(
                    key="course",
                    match=models.MatchValue(value=course)
                )
            ]
        ),
        limit=limit, # top closest matches
        with_payload=True #to get metadata in the results
    )

    return results

print("\n Answer with filter search")
print(search_in_course("What if I submit homeworks late?", "mlops-zoomcamp").points[0].payload['text'])