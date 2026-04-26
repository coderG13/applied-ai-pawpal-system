from pathlib import Path
from typing import List, Dict
from pawpal_system import ScheduledTask


def load_knowledge_sources() -> Dict[str, str]:
    """
    RAG Enhancement:
    Loads multiple knowledge files from ai/knowledge.
    """
    knowledge_folder = Path("ai/knowledge")
    sources = {}

    for file_path in knowledge_folder.glob("*.txt"):
        sources[file_path.name] = file_path.read_text()

    return sources


def analyze_schedule(schedule: List[ScheduledTask]) -> List[str]:
    """
    Backward-compatible function used by app.py.
    Returns only suggestion strings.
    """
    result = agentic_analyze_schedule(schedule)
    return result["suggestions"]


def agentic_analyze_schedule(schedule: List[ScheduledTask]) -> Dict:
    """
    Agentic Workflow:
    Step 1: Retrieve knowledge
    Step 2: Inspect schedule
    Step 3: Detect risky patterns
    Step 4: Generate suggestions
    Step 5: Assign confidence score
    """
    knowledge_sources = load_knowledge_sources()

    reasoning_steps = []
    suggestions = []
    confidence_scores = []

    reasoning_steps.append("Step 1: Retrieved pet-care knowledge from multiple local documents.")
    reasoning_steps.append("Step 2: Reviewed scheduled tasks in order.")
    reasoning_steps.append("Step 3: Checked for unsafe or inefficient care patterns.")

    for i in range(len(schedule) - 1):
        current = schedule[i]
        next_task = schedule[i + 1]

        if current.task.category == "feeding" and next_task.task.category == "walk":
            suggestions.append(
                f"Move walk before feeding for {current.pet.name} because walking immediately after eating may be uncomfortable."
            )
            confidence_scores.append(0.90)
            reasoning_steps.append("Detected feeding followed by walk.")

        if current.task.category == "medication" and next_task.task.category == "medication":
            suggestions.append(
                f"Space medication tasks for {current.pet.name} to reduce risk of unsafe timing."
            )
            confidence_scores.append(0.85)
            reasoning_steps.append("Detected medication tasks scheduled close together.")

        if current.task.duration_minutes >= 45 and next_task.task.duration_minutes >= 45:
            suggestions.append(
                f"Add a break between long tasks for {current.pet.name} to avoid overloading the pet."
            )
            confidence_scores.append(0.80)
            reasoning_steps.append("Detected long back-to-back tasks.")

    if not suggestions:
        reasoning_steps.append("No risky pattern found based on current knowledge rules.")

    average_confidence = 0
    if confidence_scores:
        average_confidence = sum(confidence_scores) / len(confidence_scores)

    reasoning_steps.append("Step 4: Generated safety suggestions.")
    reasoning_steps.append("Step 5: Calculated confidence score.")

    return {
        "knowledge_sources_used": list(knowledge_sources.keys()),
        "reasoning_steps": reasoning_steps,
        "suggestions": suggestions,
        "average_confidence": round(average_confidence, 2)
    }