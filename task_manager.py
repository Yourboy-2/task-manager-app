"""
Task Manager Application
Author: Awenkosi Moyo
Description: A command-line task manager that lets users create, view,
             complete, and delete tasks. Tasks are saved to a JSON file
             so they persist between sessions.
Tech: Python, JSON, OOP, datetime
"""

import json
import os
from datetime import datetime


# ─── File Path ────────────────────────────────────────────────────────────────
TASKS_FILE = "tasks.json"


# ─── Utility ─────────────────────────────────────────────────────────────────
def divider():
    print("-" * 50)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ─── Task Class ───────────────────────────────────────────────────────────────
class Task:
    def __init__(self, task_id, title, description, priority, created_at, completed=False, completed_at=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority  # "High", "Medium", "Low"
        self.created_at = created_at
        self.completed = completed
        self.completed_at = completed_at

    def mark_complete(self):
        self.completed = True
        self.completed_at = get_timestamp()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "created_at": self.created_at,
            "completed": self.completed,
            "completed_at": self.completed_at
        }

    def display(self):
        status = "✓ Done" if self.completed else "○ Pending"
        priority_symbols = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        symbol = priority_symbols.get(self.priority, "⚪")
        print(f"\n  [{self.task_id}] {self.title}")
        print(f"      Status   : {status}")
        print(f"      Priority : {symbol} {self.priority}")
        print(f"      Details  : {self.description}")
        print(f"      Created  : {self.created_at}")
        if self.completed_at:
            print(f"      Completed: {self.completed_at}")


# ─── Task Manager Class ───────────────────────────────────────────────────────
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(TASKS_FILE):
            self.tasks = []
            return
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            self.tasks = [Task(**t) for t in data]

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def get_next_id(self):
        if not self.tasks:
            return 1
        return max(t.task_id for t in self.tasks) + 1

    def add_task(self):
        divider()
        print("  ADD NEW TASK")
        divider()
        title = input("  Task title: ").strip()
        if not title:
            print("  ✗ Title cannot be empty.")
            return

        description = input("  Description (optional): ").strip()
        if not description:
            description = "No description provided."

        print("  Priority: 1. High   2. Medium   3. Low")
        priority_choice = input("  Choose priority (1/2/3): ").strip()
        priority_map = {"1": "High", "2": "Medium", "3": "Low"}
        priority = priority_map.get(priority_choice, "Medium")

        task = Task(
            task_id=self.get_next_id(),
            title=title,
            description=description,
            priority=priority,
            created_at=get_timestamp()
        )
        self.tasks.append(task)
        self.save_tasks()
        print(f"\n  ✓ Task '{title}' added successfully (ID: {task.task_id}).")

    def view_tasks(self, filter_by=None):
        """
        filter_by: None = all, 'pending' = incomplete only, 'done' = complete only
        """
        divider()
        if filter_by == "pending":
            tasks_to_show = [t for t in self.tasks if not t.completed]
            print("  PENDING TASKS")
        elif filter_by == "done":
            tasks_to_show = [t for t in self.tasks if t.completed]
            print("  COMPLETED TASKS")
        else:
            tasks_to_show = self.tasks
            print("  ALL TASKS")
        divider()

        if not tasks_to_show:
            print("  No tasks found.")
            return

        # Sort: pending first, then by priority
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        tasks_to_show = sorted(
            tasks_to_show,
            key=lambda t: (t.completed, priority_order.get(t.priority, 3))
        )

        for task in tasks_to_show:
            task.display()
        divider()
        print(f"  Total: {len(tasks_to_show)} task(s)")

    def complete_task(self):
        self.view_tasks(filter_by="pending")
        if not any(not t.completed for t in self.tasks):
            return
        try:
            task_id = int(input("\n  Enter Task ID to mark as complete: "))
            task = next((t for t in self.tasks if t.task_id == task_id), None)
            if not task:
                print("  ✗ Task not found.")
                return
            if task.completed:
                print("  ✗ Task is already completed.")
                return
            task.mark_complete()
            self.save_tasks()
            print(f"  ✓ Task '{task.title}' marked as complete!")
        except ValueError:
            print("  ✗ Please enter a valid task ID.")

    def delete_task(self):
        self.view_tasks()
        if not self.tasks:
            return
        try:
            task_id = int(input("\n  Enter Task ID to delete: "))
            task = next((t for t in self.tasks if t.task_id == task_id), None)
            if not task:
                print("  ✗ Task not found.")
                return
            confirm = input(f"  Delete '{task.title}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                self.tasks = [t for t in self.tasks if t.task_id != task_id]
                self.save_tasks()
                print(f"  ✓ Task deleted.")
            else:
                print("  Deletion cancelled.")
        except ValueError:
            print("  ✗ Please enter a valid task ID.")

    def summary(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.completed)
        pending = total - done
        high = sum(1 for t in self.tasks if t.priority == "High" and not t.completed)

        divider()
        print("  TASK SUMMARY")
        divider()
        print(f"  Total tasks   : {total}")
        print(f"  Completed     : {done}")
        print(f"  Pending       : {pending}")
        print(f"  High priority : {high} pending")
        divider()

    def run(self):
        while True:
            print()
            divider()
            print("  TASK MANAGER — Awenkosi Moyo")
            divider()
            print("  1. Add Task")
            print("  2. View All Tasks")
            print("  3. View Pending Tasks")
            print("  4. View Completed Tasks")
            print("  5. Mark Task as Complete")
            print("  6. Delete Task")
            print("  7. Summary")
            print("  8. Exit")
            divider()
            choice = input("  Select option: ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.view_tasks(filter_by="pending")
            elif choice == "4":
                self.view_tasks(filter_by="done")
            elif choice == "5":
                self.complete_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                self.summary()
            elif choice == "8":
                print("\n  Goodbye! Stay productive.\n")
                break
            else:
                print("  ✗ Invalid option. Please try again.")

            input("\n  Press Enter to continue...")


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    manager = TaskManager()
    manager.run()
