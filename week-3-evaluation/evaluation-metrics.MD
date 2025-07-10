1. **Precision at k (P@k)**:
   - Measures the number of relevant documents in the top k results.
   - Formula: `P@k = (Number of relevant documents in top k results) / k`

2. **Recall**:
   - Measures the number of relevant documents retrieved out of the total number of relevant documents available.
   - Formula: `Recall = (Number of relevant documents retrieved) / (Total number of relevant documents)`


3. **Mean Average Precision (MAP)**:
   - Computes the average precision for each query and then averages these values over all queries.
   - Formula: `MAP = (1 / |Q|) * Σ (Average Precision(q))` for q in Q

4. **Normalized Discounted Cumulative Gain (NDCG)**:
   - Measures the usefulness, or gain, of a document based on its position in the result list.
   - Formula: `NDCG = DCG / IDCG`
     - `DCG = Σ ((2^rel_i - 1) / log2(i + 1))` for i = 1 to p
     - `IDCG` is the ideal DCG, where documents are perfectly ranked by relevance.

5. **Mean Reciprocal Rank (MRR)**:
   - Evaluates the rank position of the first relevant document.
   - Formula: `MRR = (1 / |Q|) * Σ (1 / rank_i)` for i = 1 to |Q|

6. **F1 Score**:
   - Harmonic mean of precision and recall.
   - Formula: `F1 = 2 * (Precision * Recall) / (Precision + Recall)`

7. **Area Under the ROC Curve (AUC-ROC)**:
   - Measures the ability of the model to distinguish between relevant and non-relevant documents.
   - AUC is the area under the Receiver Operating Characteristic (ROC) curve, which plots true positive rate (TPR) against false positive rate (FPR).

8. **Mean Rank (MR)**:
   - The average rank of the first relevant document across all queries.
   - Lower values indicate better performance.

9. **Hit Rate (HR) or Recall at k**:
   - Measures the proportion of queries for which at least one relevant document is retrieved in the top k results.
   - Formula: `HR@k = (Number of queries with at least one relevant document in top k) / |Q|`

10. **Expected Reciprocal Rank (ERR)**:
    - Measures the probability that a user finds a relevant document at each position in the ranked list, assuming a cascading model of user behavior.
    - Formula: `ERR = Σ (1 / i) * Π (1 - r_j) * r_i` for j = 1 to i-1
      - Where `r_i` is the relevance probability of the document at position i.



### With Example


# Information Retrieval Evaluation Metrics with Examples

This document provides a simple explanation and numeric examples for commonly used evaluation metrics in Information Retrieval (IR). We differentiate clearly between **queries** and **query results**.

---

## 1. Precision at k (P@k)

**Definition**: Measures how many of the top-k retrieved documents are relevant.

**Formula**:
```
P@k = (Number of relevant documents in top k results) / k
```

**Example**:
```python
query_result = [1, 0, 1, 0, 0, 1, 0, 0, 0, 1]  # Top 10 documents returned (1 = relevant)
top_5 = query_result[:5]  # [1, 0, 1, 0, 0]
P@5 = 2 / 5 = 0.4
```

---

## 2. Recall

**Definition**: Measures how many of the relevant documents were retrieved out of all relevant documents available for the query.

**Formula**:
```
Recall = (Number of relevant documents retrieved) / (Total number of relevant documents)
```

**Example**:
```python
query_result = [1, 0, 1, 0, 0, 1, 0, 0, 0, 1]
relevant_found = sum(query_result)  # = 4
total_relevant = 5
Recall = 4 / 5 = 0.8
```

---

## 3. Mean Average Precision (MAP)

**Definition**: Computes the average precision for each query, then averages across all queries.

**Formula**:
```
MAP = (1 / |Q|) * Σ (Average Precision(q)) for q in Q
```

**Example**:
```python
query1_result = [1, 0, 1, 0, 0]
query2_result = [0, 1, 0, 1, 0]

# query1: Precision@1 = 1.0, Precision@3 = 2/3
AP1 = (1.0 + 0.667) / 2 = 0.833

# query2: Precision@2 = 0.5, Precision@4 = 0.5
AP2 = (0.5 + 0.5) / 2 = 0.5

MAP = (0.833 + 0.5) / 2 = 0.666
```

---

## 4. Normalized Discounted Cumulative Gain (NDCG)

**Definition**: Evaluates ranking quality by comparing actual order to ideal order based on relevance scores.

**Formula**:
```
NDCG = DCG / IDCG
DCG = Σ ((2^rel_i - 1) / log2(i + 1)) for i = 1 to p
```

**Example**:
```python
relevance = [3, 2, 3, 0, 1]

DCG = 3/1 + 2/log2(3) + 3/log2(4) + 0 + 1/log2(6)
    ≈ 6.146

IDCG (sorted): [3, 3, 2, 1, 0]
IDCG ≈ 6.32

NDCG = 6.146 / 6.32 ≈ 0.972
```

---

## 5. Mean Reciprocal Rank (MRR)

**Definition**: Measures how early the first relevant document appears in the ranked results.

**Formula**:
```
MRR = (1 / |Q|) * Σ (1 / rank_i) for i = 1 to |Q|
```

**Example**:
```python
query1_result = [0, 0, 1, 0]  → first relevant at rank 3 → 1/3
query2_result = [1, 0, 0, 0]  → rank 1 → 1/1

MRR = (1/3 + 1/1) / 2 = 0.666
```

---

## 6. F1 Score

**Definition**: Harmonic mean of precision and recall.

**Formula**:
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

**Example**:
```python
Precision = 0.4
Recall = 0.8
F1 = 2 * (0.4 * 0.8) / (0.4 + 0.8) = 0.533
```

---

## 7. Area Under the ROC Curve (AUC-ROC)

**Definition**: Measures the model's ability to distinguish between relevant and non-relevant documents.

**Example**:
```python
scores = [0.9, 0.8, 0.3, 0.2]
labels = [1, 1, 0, 0]
```
Plot TPR vs FPR at various thresholds → AUC is area under this curve. Close to 1 = good.

---

## 8. Mean Rank (MR)

**Definition**: Average rank of the first relevant document across queries.

**Example**:
```python
query1_result = [0, 0, 1, 0] → rank = 3
query2_result = [0, 1, 0, 0] → rank = 2
MR = (3 + 2) / 2 = 2.5
```

---

## 9. Hit Rate @k (HR@k)

**Definition**: Measures if at least one relevant document is found in the top k results.

**Formula**:
```
HR@k = (Number of queries with ≥1 relevant doc in top k) / total_queries
```

**Example**:
```python
query1_result = [0, 0, 1, 0, 0]  → yes
query2_result = [0, 0, 0, 0, 0]  → no
query3_result = [1, 0, 0, 0, 0]  → yes

HR@5 = 2 / 3 = 0.667
```

---

## 10. Expected Reciprocal Rank (ERR)

**Definition**: Models probability that user stops at a relevant document.

**Formula**:
```
ERR = Σ (1 / i) * Π (1 - r_j) * r_i  for j = 1 to i-1
```

**Example**:
```python
relevance_probs = [1.0, 0.6, 0.2, 0, 0]

ERR ≈ 
(1/1)*1.0 + 
(1/2)*(1-1.0)*0.6 + 
(1/3)*(1-1.0)*... = 1.0
```
High relevance at top → ERR near 1.

---
