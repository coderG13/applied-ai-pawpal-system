# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I designed my system using four main classes: Owner, Pet, Task, and Scheduler. I tried to keep it simple and match real life. The Owner has pets, each Pet has tasks, and the Scheduler builds a daily plan. The main actions were adding a pet, adding tasks, and generating a schedule.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I made a few small improvements while building. I changed ScheduledTask to store the Pet object instead of just the name, and I added a method to clear the schedule before rebuilding it. I avoided adding too much complexity so the code stays easy to understand.



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler uses available time, task priority, and preferred time. I focused on these because they are the most useful for a busy pet owner. High-priority tasks like feeding or medication are handled first.



**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff I made is only checking for exact time conflicts instead of full overlapping time ranges. This makes the logic simpler and easier to implement, even though it is not perfectly accurate.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools like VS Code Copilot and Claude to help with different parts of the project. Copilot was helpful for writing code, fixing syntax errors, and generating small functions. Claude was more helpful for explaining concepts, reviewing my design, and suggesting improvements.

I also used separate chats for different phases (design, implementation, testing), which helped me stay organized.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I did not blindly accept AI suggestions. For example, some suggestions added extra complexity like more relationships or advanced structures. I chose to simplify those ideas so the project stayed beginner-friendly and matched the requirements. I always checked if the AI output made sense before using it.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion, adding tasks to pets, sorting by time, recurring task creation, and conflict detection. I also checked simple edge cases like pets with no tasks.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I feel fairly confident in my system because the main features work and the tests pass. If I had more time, I would test more edge cases like overlapping task durations and larger schedules.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The system design stayed clean and easy to follow. I was able to connect the backend logic to the Streamlit UI successfully.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the scheduling algorithm to handle conflicts better and make smarter decisions. I would also improve the UI with more features like editing and deleting tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned is that even with AI tools, I still need to think like the main designer. AI helps speed things up, but I have to decide what makes sense and keep the system simple and clear.