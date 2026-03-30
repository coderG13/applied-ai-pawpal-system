from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(schedule):
    print("\n===== TODAY'S SCHEDULE =====")
    if not schedule:
        print("No tasks could be scheduled.")
        return

    for item in schedule:
        print(
            f"{item.start_time} - {item.end_time} | "
            f"{item.pet.name} ({item.pet.species}) | "
            f"{item.task.title} | "
            f"Priority: {item.task.priority}"
        )

    print("\n===== SCHEDULE EXPLANATIONS =====")
    for item in schedule:
        print(f"- {item.task.title} for {item.pet.name}: {item.reason}")


def print_pet_tasks(title, pet_tasks):
    print(f"\n===== {title} =====")
    if not pet_tasks:
        print("No tasks found.")
        return

    for pet, task in pet_tasks:
        print(
            f"{pet.name} | {task.title} | time: {task.preferred_time} | "
            f"priority: {task.priority} | completed: {task.completed}"
        )


def main():
    owner = Owner(name="Jordan", available_minutes=90, preferences=["morning tasks"])

    pet1 = Pet(name="Mochi", species="dog", age=3, breed="Shih Tzu")
    pet2 = Pet(name="Luna", species="cat", age=2, breed="Siamese")

    # Add tasks out of order on purpose
    task1 = Task(
        title="Breakfast",
        category="feeding",
        duration_minutes=10,
        priority="high",
        preferred_time="08:30",
        frequency="daily",
        due_date=date.today(),
    )

    task2 = Task(
        title="Morning Walk",
        category="walk",
        duration_minutes=30,
        priority="high",
        preferred_time="08:00",
        frequency="once",
        due_date=date.today(),
    )

    task3 = Task(
        title="Medicine",
        category="medication",
        duration_minutes=5,
        priority="medium",
        preferred_time="09:00",
        frequency="daily",
        due_date=date.today(),
    )

    task4 = Task(
        title="Brush Fur",
        category="grooming",
        duration_minutes=15,
        priority="low",
        preferred_time="09:15",
        frequency="weekly",
        due_date=date.today(),
    )

    # Conflict task: same time as Breakfast
    task5 = Task(
        title="Vet Reminder",
        category="appointment",
        duration_minutes=5,
        priority="medium",
        preferred_time="08:30",
        frequency="once",
        due_date=date.today(),
    )

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet2.add_task(task4)
    pet2.add_task(task5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)

    all_tasks = scheduler.collect_tasks()
    print_pet_tasks("ALL TASKS", all_tasks)

    time_sorted = scheduler.sort_by_time(all_tasks)
    print_pet_tasks("TASKS SORTED BY TIME", time_sorted)

    luna_tasks = scheduler.filter_tasks(pet_name="Luna")
    print_pet_tasks("TASKS FILTERED FOR LUNA", luna_tasks)

    incomplete_tasks = scheduler.filter_tasks(completed=False)
    print_pet_tasks("INCOMPLETE TASKS", incomplete_tasks)

    conflicts = scheduler.detect_conflicts(all_tasks)
    print("\n===== CONFLICT WARNINGS =====")
    if conflicts:
        for conflict in conflicts:
            print(conflict)
    else:
        print("No conflicts found.")

    schedule = scheduler.build_daily_schedule(start_time="08:00")
    print_schedule(schedule)

    print("\n===== MARK TASK COMPLETE + RECURRING TASK =====")
    next_task = scheduler.mark_task_complete("Mochi", "Breakfast")
    if next_task:
        print(
            f"Recurring task created: {next_task.title} | "
            f"next due date: {next_task.due_date}"
        )
    else:
        print("No recurring task created.")

    updated_tasks = scheduler.filter_tasks(pet_name="Mochi")
    print_pet_tasks("UPDATED MOCHI TASKS", updated_tasks)


if __name__ == "__main__":
    main()