# Testing and Evaluation

## Overview
The AI system was tested using an automated evaluation script (`evaluate_ai.py`).

---

## Test Cases

1. Walk after feeding → should warn  
2. Medication too close → should warn  
3. Long tasks back-to-back → should warn  
4. Safe schedule → no warnings  

---

## Results

- 4 out of 4 tests passed  
- Average confidence score: 0.85  

---

## What was validated

- AI detects unsafe patterns  
- AI avoids unnecessary warnings  
- Outputs are consistent  

---

## Conclusion

The system behaves reliably under tested scenarios.  
Performance depends on rule coverage in the knowledge base.