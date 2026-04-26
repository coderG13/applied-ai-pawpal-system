import streamlit as st
from datetime import date
from ai.ai_engine import analyze_schedule
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("Smart pet care scheduling for busy pet owners.")

# -------------------------
# Session state
# -------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes=120,
        preferences=["morning tasks"]
    )

# -------------------------
# Owner info
# -------------------------
st.subheader("Owner Information")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
available_minutes = st.number_input(
    "Available minutes today",
    min_value=30,
    max_value=600,
    value=st.session_state.owner.available_minutes
)

st.session_state.owner.name = owner_name
st.session_state.owner.available_minutes = available_minutes

st.divider()

# -------------------------
# Add pet
# -------------------------
st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Age", min_value=0, max_value=50, value=1)
    pet_breed = st.text_input("Breed")
    pet_medical_notes = st.text_area("Medical notes")
    add_pet_button = st.form_submit_button("Add Pet")

    if add_pet_button:
        if pet_name.strip() == "":
            st.warning("Please enter a pet name.")
        else:
            new_pet = Pet(
                name=pet_name,
                species=pet_species,
                age=pet_age,
                breed=pet_breed,
                medical_notes=pet_medical_notes
            )
            st.session_state.owner.add_pet(new_pet)
            st.success(f"{pet_name} was added successfully.")

st.divider()

# -------------------------
# Show pets
# -------------------------
st.subheader("Current Pets")

if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species}) - Age: {pet.age}")
        if pet.breed:
            st.caption(f"Breed: {pet.breed}")
        if pet.medical_notes:
            st.caption(f"Medical notes: {pet.medical_notes}")
else:
    st.info("No pets added yet.")

st.divider()

# -------------------------
# Add task
# -------------------------
st.subheader("Add a Task")

if st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]

    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Choose pet", pet_names)
        task_title = st.text_input("Task title")
        task_category = st.selectbox(
            "Category",
            ["feeding", "walk", "medication", "grooming", "appointment", "play", "other"]
        )
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=15)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        preferred_time = st.text_input("Preferred time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        notes = st.text_area("Notes")
        add_task_button = st.form_submit_button("Add Task")

        if add_task_button:
            if task_title.strip() == "":
                st.warning("Please enter a task title.")
            else:
                new_task = Task(
                    title=task_title,
                    category=task_category,
                    duration_minutes=duration,
                    priority=priority,
                    preferred_time=preferred_time,
                    frequency=frequency,
                    due_date=date.today(),
                    notes=notes
                )

                for pet in st.session_state.owner.pets:
                    if pet.name == selected_pet_name:
                        pet.add_task(new_task)
                        st.success(f"Task '{task_title}' was added to {pet.name}.")
                        break
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# -------------------------
# Show all tasks in sorted order
# -------------------------
st.subheader("All Tasks")

scheduler = Scheduler(st.session_state.owner)
all_tasks = scheduler.collect_tasks()
sorted_tasks = scheduler.sort_by_time(all_tasks)

if sorted_tasks:
    table_data = []
    for pet, task in sorted_tasks:
        table_data.append({
            "Pet": pet.name,
            "Task": task.title,
            "Category": task.category,
            "Time": task.preferred_time,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Completed": task.completed
        })
    st.table(table_data)
else:
    st.info("No tasks added yet.")

# -------------------------
# Conflict warnings
# -------------------------
conflicts = scheduler.detect_conflicts(all_tasks)
if conflicts:
    st.subheader("Conflict Warnings")
    for conflict in conflicts:
        st.warning(conflict)

st.divider()

# -------------------------
# Filter tasks
# -------------------------
st.subheader("Filter Tasks")

if st.session_state.owner.pets:
    filter_pet = st.selectbox(
        "Filter by pet",
        ["All"] + [pet.name for pet in st.session_state.owner.pets]
    )
    filter_status = st.selectbox(
        "Filter by completion",
        ["All", "Completed", "Incomplete"]
    )

    selected_pet_name = None if filter_pet == "All" else filter_pet

    selected_completed = None
    if filter_status == "Completed":
        selected_completed = True
    elif filter_status == "Incomplete":
        selected_completed = False

    filtered_tasks = scheduler.filter_tasks(
        pet_name=selected_pet_name,
        completed=selected_completed
    )

    if filtered_tasks:
        filtered_table = []
        for pet, task in filtered_tasks:
            filtered_table.append({
                "Pet": pet.name,
                "Task": task.title,
                "Time": task.preferred_time,
                "Priority": task.priority,
                "Completed": task.completed
            })
        st.table(filtered_table)
    else:
        st.info("No tasks match the selected filters.")

st.divider()

# -------------------------
# Generate schedule
# -------------------------
st.subheader("Build Daily Schedule")

if st.button("Generate Schedule"):
    schedule = scheduler.build_daily_schedule(start_time="08:00")
    suggestions = analyze_schedule(schedule)

    if schedule:
        st.success("Schedule generated successfully.")

        if suggestions:
            st.subheader("🤖 AI Suggestions")
            for suggestion in suggestions:
                st.warning(suggestion)
        else:
            st.info("No AI suggestions needed. The schedule looks safe based on the current knowledge rules.")

        schedule_table = []
        for item in schedule:
            schedule_table.append({
                "Start": item.start_time,
                "End": item.end_time,
                "Pet": item.pet.name,
                "Task": item.task.title,
                "Priority": item.task.priority
            })

        st.markdown("### Today's Schedule")
        st.table(schedule_table)

        st.markdown("### Why these tasks were chosen")
        for explanation in scheduler.explain_schedule():
            st.write(f"- {explanation}")

    else:
        st.warning("No tasks could be scheduled.")