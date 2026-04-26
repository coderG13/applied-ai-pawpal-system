# AI System Design

## Type of AI System
This project uses:

- Retrieval-Augmented Generation (RAG)
- Rule-based reasoning
- Agentic workflow

---

## Why not a full LLM?

Instead of using a large model:
- The system uses structured rules
- Ensures predictable behavior
- Avoids hallucinations

---

## Knowledge Sources

The system loads multiple documents:

- pet_care.txt
- safety_rules.txt

Example rule:
"Pets should not have long tasks back-to-back."

---

## Agentic Workflow

The AI follows:

1. Retrieve knowledge  
2. Inspect schedule  
3. Detect patterns  
4. Generate suggestions  
5. Assign confidence  

---

## Confidence Scoring

Each suggestion gets a confidence value:
- Feeding + walk → 0.90  
- Medication conflict → 0.85  
- Long tasks → 0.80  

Average confidence is returned per run.

---

## Limitations

- Rule-based → limited flexibility  
- No learning from new data  
- Depends on predefined rules  

---

## Future Improvements

- Add LLM-based reasoning  
- Expand knowledge base  
- Add user feedback loop  