# Task Manager Application ✅

A command-line task management application built in Python. Helps users organise, prioritise, and track their daily tasks with full persistence between sessions.

## Features

- **Add Tasks** — Create tasks with a title, description, and priority level (High / Medium / Low)
- **View Tasks** — View all tasks, filter by pending or completed
- **Complete Tasks** — Mark tasks as done with a completion timestamp
- **Delete Tasks** — Remove tasks with a confirmation prompt
- **Summary View** — Quick overview of total, pending, and completed tasks
- **Persistent Storage** — All tasks saved to a JSON file and reloaded on startup
- **Smart Sorting** — Tasks sorted by status and priority automatically

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| OOP (Classes) | Task and TaskManager logic |
| JSON module | Data persistence |
| datetime | Timestamps |

## How to Run

```bash
python task_manager.py
```

No external libraries required.

## Project Structure

```
task_manager/
│
├── task_manager.py   # Main application
├── tasks.json        # Auto-generated: stores task data
└── README.md
```

## Sample Output

```
--------------------------------------------------
  TASK MANAGER — Awenkosi Moyo
--------------------------------------------------
  1. Add Task
  2. View All Tasks
  3. View Pending Tasks
  ...

  [1] Finish Python project
      Status   : ○ Pending
      Priority : 🔴 High
      Details  : Complete ATM banking system
      Created  : 2024-08-15 09:30
```

## Key Concepts Demonstrated

- Object-Oriented Programming (`Task`, `TaskManager` classes)
- JSON file I/O for persistent data storage
- List filtering, sorting, and manipulation
- Input validation and error handling
- Clean CLI design with a structured menu system

## Author

**Awenkosi Moyo** — Software Developer | Python | Backend Development
