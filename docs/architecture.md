# System Architecture Details

This document explains how the PawPal AI system is structured.

## Components

### 1. Streamlit UI (`app.py`)
Handles:
- User input (pets, tasks)
- Displaying schedules
- Showing AI suggestions

---

### 2. Scheduler (`pawpal_system.py`)
Responsible for:
- Collecting tasks
- Sorting by priority/time
- Building daily schedule
- Detecting conflicts

---

### 3. AI Engine (`ai/ai_engine.py`)
Implements:
- Retrieval-Augmented Generation (RAG)
- Agentic reasoning steps
- Suggestion generation
- Confidence scoring

Example reasoning:
1. Retrieve knowledge
2. Analyze schedule
3. Detect unsafe patterns
4. Generate suggestions

---

### 4. Knowledge Base (`ai/knowledge/`)
Includes:
- `pet_care.txt`
- `safety_rules.txt`

These provide rules like:
- Avoid walking after feeding
- Space medication tasks

---

### 5. Evaluation Script (`evaluate_ai.py`)
Tests:
- AI correctness
- Reliability
- Confidence scores

---

## Data Flow

User Input  
→ Scheduler builds schedule  
→ AI Engine analyzes schedule  
→ Suggestions generated  
→ User reviews output  

---

## Human-in-the-loop

The system does NOT automatically enforce changes.

Users:
- Review suggestions
- Decide whether to apply them