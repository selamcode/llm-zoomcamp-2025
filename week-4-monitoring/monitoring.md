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


### summary

1. `rag retrival -> evaluation -> week 3 evaluation`

- Recall
- mrr
- hitrate

2. `llm evaluation -> monitoring`

- using evaluation metrics and llm-as-a-judge(offline)
- user feedback

