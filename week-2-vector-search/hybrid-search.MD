### What is Hybrid Search in Qdrant?
When you search something, there are two main ways to do it:

1. Vector Search (Dense Embeddings)

- This is what AI models use.
- It’s smart — it understands the meaning of your search.

- Example: If you search for "fast car," it might also find results with "speedy    vehicle" even if those words weren’t used.

> Think of it as semantic search — it gets what you mean.

</br>

### 2. Keyword Search (Sparse Embeddings)

- This is the old-school, but still powerful method.

- It looks for exact words or phrases.

- If you type "fast car," it tries to find documents with those exact words.

 > Think of it like Google in the early days — it just matches the words you type.

</br>

#### What Are Sparse Vectors?

Imagine a giant list of every word in a dictionary.

If a document uses the word "apple", the vector will have a 1 at the "apple" position and 0 everywhere else.

##### Example

`Imagine a dictionary with these 6 words:`

> These are called sparse because most of the numbers in the list are zeros (since most documents only use a few words from the full dictionary).


[ "banana", "orange", "apple", "car", "laptop", "cat" ]

| Word   | Position |
| ------ | -------- |
| banana | 0        |
| orange | 1        |
| apple  | 2        |
| car    | 3        |
| laptop | 4        |
| cat    | 5        |

If you're searching for `"apple"`, your sparse vector would look like:

``` css
[ 0, 0, 1, 0, 0, 0 ]
```
 
If a document contains `"apple"` and `"car"`, its sparse vector would be:

``` css
[ 0, 0, 1, 1, 0, 0 ]
```


</br>

#### What is BM25?

BM25 is a smart scoring formula used in keyword search. It helps figure out which documents match your search best.

It works using 3 ideas:

##### 1. Term Frequency (TF):
If a word appears more often in a document, the document might be more relevant.

But... seeing it 10 times doesn’t make it 10× better. The effect slows down.

##### 2. Inverse Document Frequency (IDF):

Rare words are more meaningful than common words.

For example, the word "quantum" is more useful in search than "the".

##### 3. Document Length:

Longer documents naturally have more words.

BM25 adjusts scores so long documents don’t get unfair advantage just for being longer.

</br>

| Search Type                            | Strengths                               | Weaknesses                         |
| -------------------------------------- | --------------------------------------- | ---------------------------------- |
| **Vector Search** (Dense)              | Understands meaning, synonyms, language | Not good with exact codes or names |
| **Keyword Search** (Sparse, like BM25) | Exact matches, fast, great for keywords | Doesn’t understand meaning         |

</br>

So in hybrid search, you get the best of both worlds!

</br>

---

### Example


You have 3 small documents:

``` 
Doc 1: "apple is good"

Doc 2: "apple can be used for breakfast"

Doc 3: "orange is good" 

```

You want to search for `"apple"` using hybrid search, meaning:

</br>

### Step 1: Sparse Search (Keyword / BM25)

Sparse search creates vectors like this:

| Word      | Index |
| --------- | ----- |
| apple     | 0     |
| is        | 1     |
| good      | 2     |
| can       | 3     |
| be        | 4     |
| used      | 5     |
| for       | 6     |
| breakfast | 7     |
| orange    | 8     |


Now each doc becomes a sparse vector (only non-zero terms shown):

``` json
Doc 1: {0:1, 1:1, 2:1} → ("apple", "is", "good")

Doc 2: {0:1, 3:1, 4:1, 5:1, 6:1, 7:1} → ("apple", "can", "be", ...)

Doc 3: {8:1, 1:1, 2:1} → ("orange", "is", "good")

```

> Your query "apple" becomes: {0:1}

So BM25 scores:

Doc 1 ✅ match

Doc 2 ✅ match

Doc 3 ❌ no match

`Filtered result: Doc 1 & Doc 2 go to next round`


### Step 2: Semantic Search (Dense Embeddings)
Now, on top of the BM25 matches, you apply semantic scoring using embeddings.

- Convert Doc 1 and Doc 2 to dense vectors (hundreds of numbers that capture meaning).

- Convert your query ("apple") to another dense vector.

- Compute `cosine similarity` between the query vector and each doc vector.

Maybe:

- Doc 1 score = 0.91

- Doc 2 score = 0.78

So final ranked result:

✅ Doc 1

✅ Doc 2

❌ Doc 3 (filtered out in sparse step)


- `BM25` quickly narrows down docs by keywords — saves time and cost.

- Dense embeddings then rank results based on meaning, not just exact matches.

`This is fast and accurate`:

- Keyword filters, then AI(semantic search) ranks what matters most.


<br>

-----

### Why Hybrid Search?

##### Search queries vary:

- Some users write keywords (e.g., "Nike shoes size 10") → sparse (BM25) works great.

- Others write natural language (e.g., "what are the best shoes for running?") → dense embeddings shine.

Hybrid search combines both, giving you the best of both worlds.

<br>

### Fusion vs. Reranking

| Term          | Meaning                                                                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Reranking** | Take one method (e.g., dense) to fetch top candidates, and then rerank using another (e.g., BM25 or an LLM).                                 |
| **Fusion**    | Combine **results from multiple methods** (e.g., BM25 + embeddings), **without favoring one** — and merge them into one unified ranked list. |

<br>

### What Is Reciprocal Rank Fusion (RRF)?

> RRF combines multiple ranked lists by looking at how highly ranked a document is in each list — regardless of the raw scores.


| Document | Dense Ranking | Sparse Ranking | RRF Score | Final Ranking |
| -------- | ------------- | -------------- | --------- | ------------- |
| D1       | 1             | 5              | 0.0318    | 2             |
| D2       | 2             | 4              | 0.0317    | 3             |
| D3       | 3             | 2              | 0.0320    | 1             |
| D4       | 4             | 3              | 0.0315    | 5             |
| D5       | 5             | 1              | 0.0318    | 2             |

<br>

##### What does this mean?
- If a document is ranked high in both BM25 and dense search → it will appear high in the final result.

- Even if it’s not top-1 in either method, it could still win because it’s consistently good.

<br>

``` python

def rrf_search(query: str, limit: int = 1) -> list[models.ScoredPoint]:
    results = client.query_points(
        collection_name="zoomcamp-sparse-and-dense",
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

```

<br>

| Feature                | Purpose                                         |
| ---------------------- | ----------------------------------------------- |
| `prefetch`             | Runs dense & sparse search independently        |
| `FusionQuery(RRF)`     | Merges those two result sets by rank, not score |
| `limit`                | Final number of top fused results you want      |
| `models.Document(...)` | Defines query format (text + model used)        |


