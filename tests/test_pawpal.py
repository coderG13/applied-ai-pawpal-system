from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(
        title="Breakfast",
        category="feeding",
        duration_minutes=10,
        priority="high",
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        title="Morning Walk",
        category="walk",
        duration_minutes=20,
        priority="medium",
    )

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Morning Walk"


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog")

    task1 = Task(
        title="Medicine",
        category="medication",
        duration_minutes=5,
        priority="medium",
        preferred_time="09:00",
    )

    task2 = Task(
        title="Breakfast",
        category="feeding",
        duration_minutes=10,
        priority="high",
        preferred_time="08:30",
    )

    task3 = Task(
        title="Walk",
        category="walk",
        duration_minutes=20,
        priority="high",
        preferred_time="08:00",
    )

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(scheduler.collect_tasks())

    assert sorted_tasks[0][1].title == "Walk"
    assert sorted_tasks[1][1].title == "Breakfast"
    assert sorted_tasks[2][1].title == "Medicine"


def test_daily_task_completion_creates_next_recurring_task():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog")

    task = Task(
        title="Breakfast",
        category="feeding",
        duration_minutes=10,
        priority="high",
        preferred_time="08:00",
        frequency="daily",
        due_date=date.today(),
    )

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete("Mochi", "Breakfast")

    assert task.completed is True
    assert next_task is not None
    assert next_task.title == "Breakfast"
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert len(pet.tasks) == 2


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(name="Jordan", available_minutes=120)
    pet1 = Pet(name="Mochi", species="dog")
    pet2 = Pet(name="Luna", species="cat")

    task1 = Task(
        title="Breakfast",
        category="feeding",
        duration_minutes=10,
        priority="high",
        preferred_time="08:30",
    )

    task2 = Task(
        title="Medicine",
        category="medication",
        duration_minutes=5,
        priority="medium",
        preferred_time="08:30",
    )

    pet1.add_task(task1)
    pet2.add_task(task2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(scheduler.collect_tasks())

    assert len(conflicts) == 1
    assert "08:30" in conflicts[0]


def test_pet_with_no_tasks_returns_empty_list():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    tasks = scheduler.collect_tasks()

    assert tasks == []