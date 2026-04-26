# 🐾 PawPal AI Care Assistant

## 🎥 Demo Video
▶️ [Watch Full Demo](https://www.loom.com/share/4cd170c264004d85b47e09d1710857db)

---

## 📌 Project Summary
PawPal AI Care Assistant is an intelligent pet-care scheduling system that helps pet owners organize daily tasks while ensuring safety and efficiency. It extends a rule-based scheduler by integrating AI-driven reasoning and retrieval to provide smart suggestions and warnings. This system improves decision-making by combining structured scheduling with AI insights based on real pet-care guidelines.

---

## 🔗 Project Repository
GitHub: https://github.com/coderG13/applied-ai-pawpal-system

---

## 🔙 Original Project (Module 2)
This project is an extension of my earlier project **PawPal+**, a Streamlit-based pet-care scheduler. The original system allowed users to add pets, assign tasks (feeding, walking, medication, grooming, etc.), and generate a daily schedule based on task priority and available time. It also included features like conflict detection and task filtering.

---

## 🤖 What This Version Adds (Applied AI System)

This version enhances PawPal+ with AI capabilities:

- Retrieval-Augmented reasoning (RAG) using a pet-care knowledge base  
- AI-generated suggestions and safety warnings  
- Agentic reasoning workflow with observable steps  
- Reliability evaluation through a testing script with confidence scoring  

---

## 🧠 Core AI Feature

The main AI feature combines:

- **Retrieval-Augmented Generation (RAG):** loads multiple knowledge files (`pet_care.txt`, `safety_rules.txt`)  
- **Agentic Workflow:** structured reasoning process with observable steps  
- **Reliability Evaluation:** test harness that validates system behavior  

This feature is fully integrated into the system. Every generated schedule is automatically analyzed by the AI engine, which applies rules and produces suggestions that directly affect output behavior.

---

## 🏗️ System Architecture

![Architecture Diagram](assets/architecture_diagram.svg)

### Overview
The system is composed of:

- **Streamlit UI (`app.py`)** → handles user input and output  
- **Scheduler (`pawpal_system.py`)** → generates the base schedule  
- **AI Engine (`ai/ai_engine.py`)** → analyzes schedules and generates suggestions  
- **Knowledge Base (`ai/knowledge/`)** → stores pet-care rules  
- **Evaluation Script (`evaluate_ai.py`)** → tests reliability  

### Data Flow
User Input → Scheduler → AI Analysis → Suggestions → Final Output  

### Human + Testing Role
- The user reviews AI suggestions before acting  
- Evaluation script verifies correctness and consistency  

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/coderG13/applied-ai-pawpal-system.git
cd applied-ai-pawpal-system

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python3 -m streamlit run app.py