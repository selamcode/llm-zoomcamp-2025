from fastembed import TextEmbedding

import numpy as np

query:list[str] =  ["I just discovered the course. Can I join now?"]
model = TextEmbedding(model_name='jinaai/jina-embeddings-v2-small-en')
embeddings = list(model.embed(query))


print("\nQuestion-1-Answer\n")
print(min(embeddings[0]))


q = embeddings[0]

''' 
computes the Euclidean norm (also called the L2 norm), which is 
just the length (or magnitude) of that vector. 

Why this is important
If the norm is 1.0, the vector is unit-length (normalized).
Helps verify whether embeddings are ready for cosine-based comparison.
This is what allows you to compute cosine similarity using just dot(a, b).

'''
# not necessary for similarity check, as FastEmbed embeddings are already normalized to length 1.
# only for explantion purpose
normalization = np.linalg.norm(q)

print("\nnormalizing our query\n",np.linalg.norm(q),"\n")


'''
When vectors are normalized:
The dot product between two vectors becomes cosine similarity, and:

As the dot product → 1
- The similarity increases
- The vectors point in nearly the same direction
- Their meanings are almost identical

As the dot product → 0

- The vectors are unrelated (orthogonal in space)
- The meanings are dissimilar

As the dot product → -1
- They point in opposite directions
- This is very rare in semantic embeddings, but would suggest opposing meanings

'''
dot_product = q.dot(q)
print("\nif you use a dot product of a query on it self it will be 1\n",dot_product,"\n")



print("Question-2-Answer\n")

doc:list[str] =  ['Can I still join the course after the start date?']
doc_model = TextEmbedding(model_name='jinaai/jina-embeddings-v2-small-en')
doc_embedding = list(model.embed(doc))

d = doc_embedding[0]

# not necessary for similarity check, as FastEmbed embeddings are already normalized to length 1.
normalization = np.linalg.norm(d) 

print(d.dot(q),"\n")



documents = [{'text': "Yes, even if you don't register, you're still eligible to submit the homeworks.\nBe aware, however, that there will be deadlines for turning in the final projects. So don't leave everything for the last minute.",
  'section': 'General course-related questions',
  'question': 'Course - Can I still join the course after the start date?',
  'course': 'data-engineering-zoomcamp'},
 {'text': 'Yes, we will keep all the materials after the course finishes, so you can follow the course at your own pace after it finishes.\nYou can also continue looking at the homeworks and continue preparing for the next cohort. I guess you can also start working on your final capstone project.',
  'section': 'General course-related questions',
  'question': 'Course - Can I follow the course after it finishes?',
  'course': 'data-engineering-zoomcamp'},
 {'text': "The purpose of this document is to capture frequently asked technical questions\nThe exact day and hour of the course will be 15th Jan 2024 at 17h00. The course will start with the first  “Office Hours'' live.1\nSubscribe to course public Google Calendar (it works from Desktop only).\nRegister before the course starts using this link.\nJoin the course Telegram channel with announcements.\nDon’t forget to register in DataTalks.Club's Slack and join the channel.",
  'section': 'General course-related questions',
  'question': 'Course - When will the course start?',
  'course': 'data-engineering-zoomcamp'},
 {'text': 'You can start by installing and setting up all the dependencies and requirements:\nGoogle cloud account\nGoogle Cloud SDK\nPython 3 (installed with Anaconda)\nTerraform\nGit\nLook over the prerequisites and syllabus to see if you are comfortable with these subjects.',
  'section': 'General course-related questions',
  'question': 'Course - What can I do before the course starts?',
  'course': 'data-engineering-zoomcamp'},
 {'text': 'Star the repo! Share it with friends if you find it useful ❣️\nCreate a PR if you see you can improve the text or the structure of the repository.',
  'section': 'General course-related questions',
  'question': 'How can we contribute to the course?',
  'course': 'data-engineering-zoomcamp'}]

'''
# Collect just the texts
docs = []
for dics in documents:
    current_text = dics.get("text")
    docs.append(current_text)

# Create the embedding model
model = TextEmbedding(model_name='jinaai/jina-embeddings-v2-small-en')

# Embed the documents
docs_embedding = list(model.embed(docs))

# Embed a sample query
#q = list(model.embed(["Can I still join the course?"]))[0]

# Compare each document's vector to the query vector
for i in range(len(docs_embedding)):
    print("Text", i, "cosine similarity with query vector is ->", docs_embedding[i].dot(q), "\n")
'''
'''
    Text 0 cosine similarity with query vector is -> 0.7629684518721929 

    Text 1 cosine similarity with query vector is -> 0.8182378156620136 

    Text 2 cosine similarity with query vector is -> 0.8085397445747489 

    Text 3 cosine similarity with query vector is -> 0.7133078832064158 

    Text 4 cosine similarity with query vector is -> 0.7304499196411822 
'''



docs = []
for dics in documents:
    current_text = dics['question'] + ' ' + dics['text']
    docs.append(current_text)
    
# print(docs)



# Create the embedding model
model = TextEmbedding(model_name='jinaai/jina-embeddings-v2-small-en')

# Embed the documents
docs_embedding = list(model.embed(docs))

# Embed a sample query
#q = list(model.embed(["Can I still join the course?"]))[0]

# Compare each document's vector to the query vector
for i in range(len(docs_embedding)):
    print("Text", i, "cosine similarity with query vector is ->", docs_embedding[i].dot(q), "\n")

'''

Text 0 cosine similarity with query vector is -> 0.851454319443226 

Text 1 cosine similarity with query vector is -> 0.8436594005975434 

Text 2 cosine similarity with query vector is -> 0.8408287224005013 

Text 3 cosine similarity with query vector is -> 0.7755157657626951 

Text 4 cosine similarity with query vector is -> 0.8086007917931164 

'''


