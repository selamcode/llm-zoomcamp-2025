#### what is dlt (Data Load Tool)?

helps take the data from source and move it somewhere else.

 - is opensource python library that lets you build modern ELT pipelines using just python code 
 
It helps you:

a. `Extract` data from APIs, databases, files and cutome sorces
b. `Transform` and normalize data
c. `Load data` into destinations like BigQuery, DuckDB,  Redshift, etc
d. Manage `schemas`, `states`, and `incremental loading` automatically  

`Extract Data -> Normalize Data -> Load Data`

![Alt text](images/dlt-1.png) 


main idead of `RAG`:


![Alt text](images/rag-idea.png) 

#### What's cognee ?

1. cognee turns your data into a queryable memeory and knowledge graph

2.  It lets you:

    a.  Add structured and unstructured data(DataFrames, documents, tables)

    b.  Automatically build a knowledge graph from it
    c.  Ask natural langauge questions and get grounded, context-rich answers

    > `DLT` is a tool for getting your data from different places. `Qdrant` is a database for storing vector representations of your data. `Cognee` is a framework that helps organize and understand your data by building a knowledge graph and integrating with vector databases like Qdrant. 



##### what happens when you run cognee.

![Alt text](images/cognee-1.png) 

`Parse Data -> Build Data Knowledge Graph -> Enrich with Metadata -> Save to Cognee Memory`

Knowledge Graph 
![Alt text](images/knowledge-graph.png) 


### Challenges of `RAG` system

##### Challenge 1

`Challenge` -> `Restrival Quality and Relavance`
- RAG may retrive irrelevant, incomplete, or outdated information, leading to poor or misleading output.

`Cognee's Solution`

- Graph-based retreval uses a semantic graph to identify and connect relevant facts, improving precision and contextual relavance.

##### Challenge 2




