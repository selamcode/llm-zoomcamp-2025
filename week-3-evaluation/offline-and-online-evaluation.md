### RAG Evaluation Overview

- RAG (Retrieval-Augmented Generation) evaluation is typically split across two main phases:

---

#### 1. Retrieval Evaluation

- This evaluates how good the retriever is at finding relevant documents.

| **Evaluation Type** | **Name**                           | **Description**                                                                 |
| ------------------- | ---------------------------------- | ------------------------------------------------------------------------------- |
| ✅ Offline           | **Cosine Similarity**              | Measures semantic similarity between query and retrieved docs (or ground-truth) |
| ✅ Offline           | **Precision / Recall / Recall\@k** | Checks if ground-truth docs are among the top-k retrieved                       |
| ✅ Offline           | **MMR / diversity metrics**        | Checks if retrieval is diverse or repetitive                                    |

---

#### 2. Generation Evaluation

This evaluates how good the answer is after using the retrieved documents.

| **Evaluation Type** | **Name**                               | **Description**                                                                 |
| ------------------- | -------------------------------------- | ------------------------------------------------------------------------------- |
| ✅ Offline           | **LLM-as-a-Judge**                     | Uses a language model to grade the final answer: helpfulness, correctness, etc. |                             |
| ⚡ Online            | **User feedback**                      | Real-time feedback, ratings, upvotes/downvotes                                  |
| ⚡ Online            | **A/B Testing**                        | Deploying versions of RAG and seeing which performs better with users           |
