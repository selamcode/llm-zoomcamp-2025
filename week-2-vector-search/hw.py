from fastembed import TextEmbedding

import numpy as np

query:list[str] =  ["I just discovered the course. Can I join now?"]
model = TextEmbedding(model_name='jinaai/jina-embeddings-v2-small-en')
embeddings = list(model.embed(query))


print("\nQuestion-1-Answer\n")
print(min(embeddings[0]))


q = embeddings[0]

''' computes the Euclidean norm (also called the L2 norm), which is 
just the length (or magnitude) of that vector. 

Why this is important
If the norm is 1.0, the vector is unit-length (normalized).
Helps verify whether embeddings are ready for cosine-based comparison.
This is what allows you to compute cosine similarity using just dot(a, b).

'''

np.linalg.norm(q)
print("\n", q.dot(q))

