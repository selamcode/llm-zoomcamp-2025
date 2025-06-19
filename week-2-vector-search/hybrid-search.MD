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