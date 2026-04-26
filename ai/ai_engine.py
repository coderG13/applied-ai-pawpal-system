from typing import List
from pawpal_system import ScheduledTask

def load_knowledge():
    with open("ai/knowledge/pet_care.txt", "r") as f:
        return f.read()

def analyze_schedule(schedule: List[ScheduledTask]) -> List[str]:
    """
    AI-like reasoning layer (rule + prompt style)
    """
    knowledge = load_knowledge()
    suggestions = []

    for i in range(len(schedule) - 1):
        current = schedule[i]
        next_task = schedule[i + 1]

        # Example reasoning rules
        if current.task.category == "feeding" and next_task.task.category == "walk":
            suggestions.append(
                f"Move walk before feeding for {current.pet.name} (better digestion)."
            )

        if current.task.category == "medication" and next_task.task.category == "medication":
            suggestions.append(
                f"Space medication tasks for {current.pet.name} to avoid overlap."
            )

    return suggestions