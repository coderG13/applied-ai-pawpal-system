from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta


@dataclass
class Task:
    """Represents one pet-care task in the system."""

    title: str
    category: str
    duration_minutes: int
    priority: str
    preferred_time: Optional[str] = None
    frequency: str = "once"   # once, daily, weekly
    due_date: Optional[date] = None
    notes: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def conflicts_with(self, other: "Task") -> bool:
        """Check whether this task conflicts with another task."""
        if self.preferred_time is None or other.preferred_time is None:
            return False
        return self.preferred_time == other.preferred_time

    def priority_score(self) -> int:
        """Return a numeric score for sorting by priority."""
        scores = {"high": 3, "medium": 2, "low": 1}
        return scores.get(self.priority.lower(), 0)

    def create_next_recurring_task(self) -> Optional["Task"]:
        """Create the next recurring copy of this task if needed."""
        if self.frequency == "daily":
            next_due = (self.due_date or date.today()) + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = (self.due_date or date.today()) + timedelta(days=7)
        else:
            return None

        return Task(
            title=self.title,
            category=self.category,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            preferred_time=self.preferred_time,
            frequency=self.frequency,
            due_date=next_due,
            notes=self.notes,
            completed=False,
        )


@dataclass
class Pet:
    """Represents a pet and its care tasks."""

    name: str
    species: str
    age: int = 0
    breed: str = ""
    medical_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title."""
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Represents the pet owner."""

    name: str
    available_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's account."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class ScheduledTask:
    """Represents a scheduled version of a task."""

    task: Task
    pet: Pet
    start_time: str
    end_time: str
    reason: str = ""


@dataclass
class Scheduler:
    """Handles daily schedule building and explanation."""

    owner: Owner
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)

    def collect_tasks(self) -> List:
        """Collect all pet-task pairs that should be considered for scheduling."""
        pet_tasks = []
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                if not task.completed:
                    pet_tasks.append((pet, task))
        return pet_tasks

    def sort_tasks(self, pet_tasks: List) -> List:
        """Sort tasks by priority first, then preferred time."""
        return sorted(
            pet_tasks,
            key=lambda item: (
                -item[1].priority_score(),
                item[1].preferred_time if item[1].preferred_time is not None else "99:99",
            ),
        )

    def sort_by_time(self, pet_tasks: List) -> List:
        """Sort pet-task pairs by preferred time."""
        return sorted(
            pet_tasks,
            key=lambda item: item[1].preferred_time if item[1].preferred_time else "99:99",
        )

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List:
        """Filter tasks by pet name and/or completion status."""
        filtered = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                if pet_name is not None and pet.name != pet_name:
                    continue
                if completed is not None and task.completed != completed:
                    continue
                filtered.append((pet, task))

        return filtered

    def detect_conflicts(self, pet_tasks: List) -> List[str]:
        """Detect simple task conflicts based on exact time matches."""
        conflicts = []

        for i in range(len(pet_tasks)):
            pet1, task1 = pet_tasks[i]
            for j in range(i + 1, len(pet_tasks)):
                pet2, task2 = pet_tasks[j]

                if task1.conflicts_with(task2):
                    conflicts.append(
                        f"Warning: '{task1.title}' for {pet1.name} and "
                        f"'{task2.title}' for {pet2.name} are both set for {task1.preferred_time}."
                    )

        return conflicts

    def clear_schedule(self) -> None:
        """Clear previously scheduled tasks before rebuilding."""
        self.scheduled_tasks.clear()

    def _add_minutes(self, time_str: str, minutes: int) -> str:
        """Return a new HH:MM time after adding minutes."""
        hours, mins = map(int, time_str.split(":"))
        total = hours * 60 + mins + minutes
        new_hours = total // 60
        new_mins = total % 60
        return f"{new_hours:02d}:{new_mins:02d}"

    def build_daily_schedule(self, start_time: str = "08:00") -> List[ScheduledTask]:
        """Build a daily plan for the owner."""
        self.clear_schedule()

        pet_tasks = self.collect_tasks()
        sorted_pet_tasks = self.sort_tasks(pet_tasks)

        current_time = start_time
        used_minutes = 0

        for pet, task in sorted_pet_tasks:
            if used_minutes + task.duration_minutes > self.owner.available_minutes:
                continue

            end_time = self._add_minutes(current_time, task.duration_minutes)
            reason = f"Scheduled because it is a {task.priority} priority {task.category} task"

            scheduled_task = ScheduledTask(
                task=task,
                pet=pet,
                start_time=current_time,
                end_time=end_time,
                reason=reason,
            )

            self.scheduled_tasks.append(scheduled_task)
            current_time = end_time
            used_minutes += task.duration_minutes

        return self.scheduled_tasks

    def explain_schedule(self) -> List[str]:
        """Explain why each task appears in the schedule."""
        explanations = []
        for item in self.scheduled_tasks:
            line = (
                f"{item.start_time}-{item.end_time}: {item.task.title} for {item.pet.name} "
                f"({item.reason})"
            )
            explanations.append(line)
        return explanations

    def mark_task_complete(self, pet_name: str, task_title: str) -> Optional[Task]:
        """Mark a task complete and create the next recurring task if needed."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                for task in pet.tasks:
                    if task.title == task_title and not task.completed:
                        task.mark_complete()
                        next_task = task.create_next_recurring_task()
                        if next_task is not None:
                            pet.add_task(next_task)
                        return next_task
        return None