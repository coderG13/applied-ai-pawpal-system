# 🐾 PawPal AI Care Assistant

## 📌 Project Summary
PawPal AI Care Assistant is an intelligent pet-care scheduling system that helps pet owners organize daily tasks while ensuring safety and efficiency. It extends a rule-based scheduler by integrating AI-driven reasoning and retrieval to provide smart suggestions and warnings. This system improves decision-making by combining structured scheduling with AI insights based on real pet-care guidelines.

## 🎥 Demo Vido
[Loom Demo](https://www.loom.com/share/4cd170c264004d85b47e09d1710857db)
---

## 🔙 Original Project (Module 2)
This project is an extension of my earlier project **PawPal+**, a Streamlit-based pet-care scheduler. The original system allowed users to add pets, assign tasks (feeding, walking, medication, grooming, etc.), and generate a daily schedule based on task priority and available time. It also included features like conflict detection and task filtering.

---

## 🤖 What This Version Adds (Applied AI System)

This version enhances PawPal+ with AI capabilities:

- Retrieval-Augmented reasoning (RAG) using a pet-care knowledge base  
- AI-generated suggestions and safety warnings  
- Improved decision-making with explainable outputs  
- Integration of AI directly into the scheduling workflow  

---

## 🏗️ System Architecture

![Architecture Diagram](assets/architecture_diagram.svg)

### Overview
The system is composed of:

- **Streamlit UI (`app.py`)** → handles user input and output  
- **Scheduler (`pawpal_system.py`)** → generates the base schedule  
- **AI Engine (`ai/ai_engine.py`)** → analyzes the schedule and generates suggestions  
- **Knowledge Base (`ai/knowledge/`)** → provides pet-care rules  
- **Evaluation Script (`evaluate_ai.py`)** → tests system reliability  

### Data Flow
User Input → Scheduler → AI Analysis → Suggestions → Final Output  

### Human + Testing Role
- The user reviews AI suggestions before acting  
- Testing ensures outputs are consistent and safe  

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/coderG13/applied-ai-pawpal-system.git
cd applied-ai-pawpal-system

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
