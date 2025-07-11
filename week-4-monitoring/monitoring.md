# 4.1 Itroduction to monitoring answers

Is checking the answers we get from our llm is good enough.

---

### how do we monitor quality of llm answers?

#### 1. offline evaluation (no contact with users)
- compute different types of quality metrics -> which is done in evaluation part
    additionally we can use 
     - LLM-as-a-judge to compute the toxicity of llm answers
     - LLM-as-a-judge to asses quality of LLM answers
- Store computed metrics in realtional database
- use `Grafana` to visualize metrics over time 
 
 `Evaluation metrics and llm-as-a judge` -> `store computed metrics in db` -> `Grafana to visualize` 

#### 2. User feedback

- Store chat sessions and collect user feedback in db
- use `Grafana` to visualize metrics over time 

---

### Other areas that need monitoring and may need more expertise (devops, site reliability )

other things we should monitor (cost of used infrasructure, errors, latency, traffic)

---

# summary

#### Evaluation for retrival

- `Recall`
- `mrr`
- `hitrate`

#### evaluation in general can be done in 2 ways for the whole RAG system.

1. offline

In out case: 

- cosign similarity
    
    - cosign_similarity (answer_original(correct one), answer_llm) -> to be discussed more

- llm as a judge 
    
    - llm_as_a_judge((answer_original, answer_llm) )



2. online

In our case:

- `A/B tests`, `experiments`
- `user feedback`

    
#### Monitoring

We check:

- overall health of the system.
- how good the answer is.
