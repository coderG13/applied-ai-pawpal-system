# Model Card: PawPal AI Care Assistant

## Overview
This system is a rule-based AI assistant designed to analyze pet-care schedules and generate safety suggestions. It uses retrieval from a knowledge base and applies structured reasoning to identify unsafe patterns.

---

## Intended Use
- Help pet owners improve daily care schedules  
- Provide safety suggestions (feeding, walking, medication timing)  

---

## Limitations
- Rule-based → limited flexibility  
- Does not generalize beyond predefined rules  
- Not a replacement for veterinary advice  

---

## Potential Biases
- Knowledge base contains simplified general pet-care rules  
- May not apply to all breeds, medical conditions, or edge cases  

---

## Evaluation Summary
- 4 out of 4 test cases passed  
- Average confidence score: ~0.85  
- System correctly detects unsafe patterns and avoids false positives  

---

## Human Oversight
The system is designed with a human-in-the-loop approach.  
All AI suggestions are advisory and must be reviewed by the user.

---

## AI Collaboration
AI tools were used for structuring the system and improving modular design.  
Some complex suggestions were rejected to maintain simplicity and clarity.