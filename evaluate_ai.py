from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler
from ai.ai_engine import agentic_analyze_schedule


def run_test_case(test_name, tasks, expected_keyword):
    owner = Owner(name="Test Owner", available_minutes=180)
    pet = Pet(name="Buddy", species="dog", age=3)

    for task in tasks:
        pet.add_task(task)

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule(start_time="08:00")
    result = agentic_analyze_schedule(schedule)

    suggestions = result["suggestions"]
    output_text = " ".join(suggestions).lower()

    if expected_keyword == "":
        passed = len(suggestions) == 0
    else:
        passed = expected_keyword.lower() in output_text

    print("\nTest:", test_name)
    print("Knowledge sources used:", result["knowledge_sources_used"])
    print("Reasoning steps:")
    for step in result["reasoning_steps"]:
        print("-", step)

    print("AI Suggestions:", suggestions)
    print("Confidence Score:", result["average_confidence"])
    print("Result:", "PASS" if passed else "FAIL")

    return passed, result["average_confidence"]


def main():
    results = []

    results.append(run_test_case(
        "Walk after feeding warning",
        [
            Task("Breakfast", "feeding", 10, "high", "08:00", "daily", date.today()),
            Task("Morning Walk", "walk", 20, "medium", "08:15", "daily", date.today()),
        ],
        "walk"
    ))

    results.append(run_test_case(
        "Medication spacing warning",
        [
            Task("Medicine 1", "medication", 5, "high", "09:00", "daily", date.today()),
            Task("Medicine 2", "medication", 5, "high", "09:15", "daily", date.today()),
        ],
        "medication"
    ))

    results.append(run_test_case(
        "Long back-to-back task warning",
        [
            Task("Long Training", "play", 50, "medium", "10:00", "once", date.today()),
            Task("Long Grooming", "grooming", 50, "medium", "11:00", "once", date.today()),
        ],
        "break"
    ))

    results.append(run_test_case(
        "Safe schedule produces no warning",
        [
            Task("Breakfast", "feeding", 10, "high", "08:00", "daily", date.today()),
            Task("Brush Fur", "grooming", 15, "low", "10:00", "weekly", date.today()),
        ],
        ""
    ))

    passed_count = sum(1 for passed, score in results if passed)
    total_count = len(results)

    confidence_values = [score for passed, score in results if score > 0]
    avg_confidence = 0
    if confidence_values:
        avg_confidence = sum(confidence_values) / len(confidence_values)

    print("\n===== EVALUATION SUMMARY =====")
    print(f"{passed_count} out of {total_count} tests passed.")
    print(f"Average confidence score: {avg_confidence:.2f}")

    if passed_count == total_count:
        print("The AI system behaved reliably and showed observable reasoning steps.")
    else:
        print("Some tests failed. More rules or validation may be needed.")


if __name__ == "__main__":
    main()