from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler
from ai.ai_engine import analyze_schedule


def run_test_case(test_name, tasks, expected_keyword):
    owner = Owner(name="Test Owner", available_minutes=120)
    pet = Pet(name="Buddy", species="dog", age=3)

    for task in tasks:
        pet.add_task(task)

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule(start_time="08:00")
    suggestions = analyze_schedule(schedule)

    output_text = " ".join(suggestions).lower()
    passed = expected_keyword.lower() in output_text

    print(f"\nTest: {test_name}")
    print(f"Expected keyword: {expected_keyword}")
    print(f"AI Suggestions: {suggestions}")
    print(f"Result: {'PASS' if passed else 'FAIL'}")

    return passed


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
        "Safe schedule produces no unnecessary warning",
        [
            Task("Breakfast", "feeding", 10, "high", "08:00", "daily", date.today()),
            Task("Brush Fur", "grooming", 15, "low", "10:00", "weekly", date.today()),
        ],
        ""
    ))

    passed_count = sum(results)
    total_count = len(results)

    print("\n===== EVALUATION SUMMARY =====")
    print(f"{passed_count} out of {total_count} tests passed.")

    if passed_count == total_count:
        print("The AI suggestion system behaved reliably on the tested examples.")
    else:
        print("Some tests failed. More rules or validation may be needed.")


if __name__ == "__main__":
    main()