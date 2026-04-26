# PawPal+ Project Reflection

## 1. System Design

### a. Initial design

I started with four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. I wanted to keep it close to real life — an owner has pets, each pet has tasks, and the scheduler figures out what to do today. Each `Task` needed a duration, a priority, and an optional preferred time so the scheduler could sort them properly.

I didn't plan a `ScheduledTask` class at first. I thought the scheduler could just return the tasks directly.

### b. Design changes

A few things changed once I actually started building:

- **Added `ScheduledTask`** — when I started writing `build_daily_schedule`, I realized returning just a list of tasks wasn't enough. I needed to store the calculated start/end times and a reason for each one. A separate class made the output way cleaner to display in Streamlit.
- **Stored the full `Pet` object instead of just the name** — I originally had `pet_name: str` in `ScheduledTask`, but when I connected it to the UI I needed to show the pet's name next to each task. Storing the actual `Pet` object made that easy without any extra lookup.
- **Added `clear_schedule()`** — I noticed tasks were doubling up every time the schedule button was pressed. Calling `clear_schedule()` at the start of `build_daily_schedule` fixed it.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

My scheduler uses three things to decide what gets scheduled:

- **Time budget** — a task only gets added if the total time used so far plus its duration doesn't go over `available_minutes`. If it doesn't fit, it gets skipped.
- **Completion status** — `collect_tasks()` only picks up incomplete tasks, so already-done tasks are ignored.
- **Preferred time** — this is used for sorting, not strict enforcement. A task set for `09:00` will come before one set for `10:00`, but it might not actually start at exactly that time depending on what came before it.

Priority is the main sort key. If two tasks have the same priority, earlier preferred time wins.

### b. Tradeoffs

The scheduler goes through the sorted list in order and adds tasks as long as they fit — it doesn't go back and try rearranging things to squeeze in more. So a single long high-priority task could push out a few shorter lower-priority ones. That felt like a fair tradeoff for this project since the goal is to get the most important stuff done first.

For conflict detection, I only flag tasks that share the exact same preferred time string. It won't catch overlapping time ranges (like a 60-minute task at 08:00 and a 10-minute task at 08:30). It's not perfect but it's simple and handles the obvious cases.

---

## 3. AI Collaboration

### a. How I used AI

I used Copilot and Claude at different points. Copilot was helpful while writing code — it filled in list comprehensions and repetitive patterns quickly, and I accepted those suggestions when they matched what I was going for. Claude was more useful for design questions, like whether `ScheduledTask` should be its own class and where `scheduled_tasks` should live.

I wrote the tests myself after the logic was done. I wanted to make sure I actually understood what each test was checking rather than just copying something that looked right.

### b. What I accepted and rejected

A couple of times I pushed back on AI suggestions:

- **Rejected a fancier conflict check** — AI suggested replacing the simple time-string comparison with a full datetime range overlap calculation. The logic was correct but it made the method much longer and harder to test. The simple version does the job for this project, so I kept it.
- **Rejected adding a priority field to `Pet`** — the idea was that some pets could have higher overall priority than others. I decided against it because task-level priorities already handle this. A high-priority feeding task for any pet will naturally rank above a low-priority grooming task. Adding pet-level priority would've made the sort logic harder for no real gain.

I tested things manually in the Python shell before writing tests — if the output looked right, I moved forward.

---

## 4. Testing and Verification

### a. What I tested

| Test | What it checks |
|------|---------------|
| `test_mark_complete_changes_status` | `mark_complete()` actually sets `completed` to `True` |
| `test_add_task_to_pet` | Tasks added to a pet are saved correctly |
| `test_sort_by_time_returns_chronological_order` | Tasks sort by time no matter what order they were added |
| `test_daily_task_completion_creates_next_recurring_task` | Completing a daily task marks it done and creates tomorrow's copy |
| `test_conflict_detection_flags_duplicate_times` | Two tasks at the same time produce exactly one warning |
| `test_pet_with_no_tasks_returns_empty_list` | An empty pet gives back an empty task list |

I focused on the things most likely to break without being obvious in the UI — sorting, recurring tasks, and conflict detection.

### b. How confident am I

Pretty confident in the core stuff. Each test checks a real outcome, not just that nothing crashed. The recurring task test, for example, checks that the original is marked done *and* that the new one has the right due date.

If I had more time I'd add tests for the time budget cutoff (making sure tasks that don't fit are actually excluded) and for `filter_tasks` with multiple filters at once.

---

## 5. Reflection

### a. What went well

Keeping all the logic in `pawpal_system.py` separate from Streamlit was probably the best decision I made. I could run tests and debug everything without touching the UI, and hooking it up to `app.py` at the end was straightforward.

### b. What I'd improve

The scheduler silently skips tasks that don't fit, which isn't great UX. I'd add a "not scheduled" section to the UI so the owner knows what got left out and why. I'd also improve conflict detection to catch overlapping time ranges, not just exact matches.

### c. Key takeaway

AI tools are genuinely useful but you have to stay in the driver's seat. A few times I accepted a suggestion without thinking it through and had to undo it later. When I described what I wanted clearly and then checked whether the suggestion actually made sense for my design, it went a lot smoother. The code is better when I use AI to think things through rather than just to write things for me.
