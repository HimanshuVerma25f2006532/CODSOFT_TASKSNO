#!/usr/bin/env python3
"""
CODSOFT - TASK 1: To-Do List Application
A complete command-line and Tkinter GUI application to create, update,
prioritize, filter, and track tasks with automatic JSON persistence.

Usage:
    python3 task1_todo_list.py          # Launches GUI if display is available, else CLI
    python3 task1_todo_list.py --cli    # Forces Command-Line Interface mode
    python3 task1_todo_list.py --gui    # Forces Tkinter GUI mode
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks_data.json")


class TodoManager:
    """Core logic for managing To-Do tasks with JSON storage."""

    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.tasks: List[Dict] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.tasks = data
            except (json.JSONDecodeError, OSError):
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=4)
        except OSError as e:
            print(f"Warning: Could not save tasks to {self.filepath}: {e}")

    def _next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(task.get("id", 0) for task in self.tasks) + 1

    def add_task(
        self,
        title: str,
        priority: str = "Medium",
        due_date: str = "",
        category: str = "General",
    ) -> Dict:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        priority = priority.capitalize()
        if priority not in ("High", "Medium", "Low"):
            priority = "Medium"
        task = {
            "id": self._next_id(),
            "title": title,
            "priority": priority,
            "category": category.strip() or "General",
            "due_date": due_date.strip(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_task(self, task_id: int) -> Optional[Dict]:
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        category: Optional[str] = None,
    ) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        if title is not None and title.strip():
            task["title"] = title.strip()
        if priority is not None and priority.capitalize() in ("High", "Medium", "Low"):
            task["priority"] = priority.capitalize()
        if due_date is not None:
            task["due_date"] = due_date.strip()
        if category is not None and category.strip():
            task["category"] = category.strip()
        self.save_tasks()
        return True

    def toggle_task(self, task_id: int) -> Optional[bool]:
        task = self.get_task(task_id)
        if not task:
            return None
        task["completed"] = not task["completed"]
        self.save_tasks()
        return task["completed"]

    def delete_task(self, task_id: int) -> bool:
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) < initial_len:
            self.save_tasks()
            return True
        return False

    def clear_completed(self) -> int:
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.get("completed", False)]
        removed = initial_len - len(self.tasks)
        if removed > 0:
            self.save_tasks()
        return removed

    def stats(self) -> Dict[str, int]:
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.get("completed", False))
        pending = total - completed
        return {"total": total, "completed": completed, "pending": pending}


# =====================================================================
# Command-Line Interface (CLI)
# =====================================================================

def print_tasks_table(tasks: List[Dict]) -> None:
    if not tasks:
        print("\n  [No tasks found.]\n")
        return
    print("\n" + "=" * 82)
    print(f"{'ID':<4} | {'Status':<10} | {'Priority':<8} | {'Category':<12} | {'Due Date':<12} | {'Title'}")
    print("-" * 82)
    for t in tasks:
        status = "[x] Done" if t.get("completed") else "[ ] Todo"
        due = t.get("due_date") or "-"
        cat = (t.get("category") or "General")[:12]
        print(
            f"{t['id']:<4} | {status:<10} | {t.get('priority', 'Medium'):<8} | "
            f"{cat:<12} | {due:<12} | {t['title']}"
        )
    print("=" * 82 + "\n")


def run_cli() -> None:
    manager = TodoManager()
    print("=" * 60)
    print("         CODSOFT TASK 1: TO-DO LIST APPLICATION")
    print("=" * 60)

    while True:
        s = manager.stats()
        print(
            f"Summary: {s['total']} Total | {s['pending']} Pending | {s['completed']} Completed"
        )
        print("1. View All Tasks")
        print("2. Add New Task")
        print("3. Update Task Details")
        print("4. Toggle Task Complete / Incomplete")
        print("5. Delete a Task")
        print("6. Filter Tasks (Pending / Completed / Priority)")
        print("7. Clear Completed Tasks")
        print("8. Exit")

        choice = input("\nSelect an option (1-8): ").strip()

        if choice == "1":
            print_tasks_table(manager.tasks)

        elif choice == "2":
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.\n")
                continue
            priority = input("Priority (High / Medium / Low) [default: Medium]: ").strip() or "Medium"
            category = input("Category (e.g., Work, Study, Personal) [default: General]: ").strip() or "General"
            due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
            task = manager.add_task(title, priority, due_date, category)
            print(f"Added Task #{task['id']}: '{task['title']}'\n")

        elif choice == "3":
            print_tasks_table(manager.tasks)
            try:
                tid = int(input("Enter Task ID to update: ").strip())
            except ValueError:
                print("Invalid ID.\n")
                continue
            existing = manager.get_task(tid)
            if not existing:
                print(f"Task #{tid} not found.\n")
                continue
            print("Leave field blank to keep existing value.")
            new_title = input(f"New title [{existing['title']}]: ").strip()
            new_prio = input(f"New priority (High/Medium/Low) [{existing['priority']}]: ").strip()
            new_cat = input(f"New category [{existing.get('category', 'General')}]: ").strip()
            new_due = input(f"New due date [{existing.get('due_date', '')}]: ").strip()
            manager.update_task(
                tid,
                title=new_title if new_title else None,
                priority=new_prio if new_prio else None,
                due_date=new_due if new_due != "" else existing.get("due_date", ""),
                category=new_cat if new_cat else None,
            )
            print(f"Task #{tid} updated.\n")

        elif choice == "4":
            try:
                tid = int(input("Enter Task ID to toggle status: ").strip())
            except ValueError:
                print("Invalid ID.\n")
                continue
            new_state = manager.toggle_task(tid)
            if new_state is None:
                print(f"Task #{tid} not found.\n")
            else:
                label = "Completed" if new_state else "Pending"
                print(f"Task #{tid} marked as {label}.\n")

        elif choice == "5":
            try:
                tid = int(input("Enter Task ID to delete: ").strip())
            except ValueError:
                print("Invalid ID.\n")
                continue
            if manager.delete_task(tid):
                print(f"Task #{tid} deleted.\n")
            else:
                print(f"Task #{tid} not found.\n")

        elif choice == "6":
            f_opt = input("Filter by (1) Pending, (2) Completed, (3) High Priority: ").strip()
            if f_opt == "1":
                filtered = [t for t in manager.tasks if not t.get("completed")]
            elif f_opt == "2":
                filtered = [t for t in manager.tasks if t.get("completed")]
            elif f_opt == "3":
                filtered = [t for t in manager.tasks if t.get("priority") == "High"]
            else:
                filtered = manager.tasks
            print_tasks_table(filtered)

        elif choice == "7":
            removed = manager.clear_completed()
            print(f"Removed {removed} completed task(s).\n")

        elif choice == "8":
            print("Goodbye! Stay productive.")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 8.\n")


# =====================================================================
# Tkinter Graphical User Interface (GUI)
# =====================================================================

def run_gui() -> None:
    import tkinter as tk
    from tkinter import ttk, messagebox

    manager = TodoManager()

    root = tk.Tk()
    root.title("CodSoft Task 1 - To-Do List Manager")
    root.geometry("760x520")
    root.minsize(680, 460)
    root.configure(bg="#f8fafc")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # Header
    header = tk.Frame(root, bg="#1e293b", pady=12, padx=16)
    header.pack(fill="x")
    tk.Label(
        header,
        text="To-Do List Manager",
        fg="white",
        bg="#1e293b",
        font=("Segoe UI", 15, "bold"),
    ).pack(side="left")
    stats_label = tk.Label(
        header,
        text="",
        fg="#cbd5e1",
        bg="#1e293b",
        font=("Segoe UI", 10),
    )
    stats_label.pack(side="right")

    # Input Form
    form = tk.Frame(root, bg="#f8fafc", pady=10, padx=16)
    form.pack(fill="x")

    tk.Label(form, text="Task Title:", bg="#f8fafc", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
    title_var = tk.StringVar()
    title_entry = ttk.Entry(form, textvariable=title_var, width=32)
    title_entry.grid(row=0, column=1, padx=6, pady=4, sticky="we")

    tk.Label(form, text="Priority:", bg="#f8fafc", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w")
    prio_var = tk.StringVar(value="Medium")
    prio_combo = ttk.Combobox(form, textvariable=prio_var, values=["High", "Medium", "Low"], width=10, state="readonly")
    prio_combo.grid(row=0, column=3, padx=6, pady=4)

    tk.Label(form, text="Category:", bg="#f8fafc", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
    cat_var = tk.StringVar(value="General")
    cat_entry = ttk.Entry(form, textvariable=cat_var, width=18)
    cat_entry.grid(row=1, column=1, padx=6, pady=4, sticky="w")

    tk.Label(form, text="Due Date:", bg="#f8fafc", font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w")
    due_var = tk.StringVar()
    due_entry = ttk.Entry(form, textvariable=due_var, width=14)
    due_entry.grid(row=1, column=3, padx=6, pady=4, sticky="w")

    form.columnconfigure(1, weight=1)

    # Treeview Table
    table_frame = tk.Frame(root, bg="#f8fafc", padx=16)
    table_frame.pack(fill="both", expand=True)

    columns = ("id", "status", "priority", "category", "due", "title")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    tree.heading("id", text="ID")
    tree.heading("status", text="Status")
    tree.heading("priority", text="Priority")
    tree.heading("category", text="Category")
    tree.heading("due", text="Due Date")
    tree.heading("title", text="Task Title")

    tree.column("id", width=45, anchor="center")
    tree.column("status", width=95, anchor="center")
    tree.column("priority", width=80, anchor="center")
    tree.column("category", width=100, anchor="center")
    tree.column("due", width=100, anchor="center")
    tree.column("title", width=290, anchor="w")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_table() -> None:
        for row in tree.get_children():
            tree.delete(row)
        for t in manager.tasks:
            status = "Completed" if t.get("completed") else "Pending"
            tree.insert(
                "",
                "end",
                iid=str(t["id"]),
                values=(
                    t["id"],
                    status,
                    t.get("priority", "Medium"),
                    t.get("category", "General"),
                    t.get("due_date") or "-",
                    t["title"],
                ),
            )
        s = manager.stats()
        stats_label.config(text=f"Total: {s['total']} | Pending: {s['pending']} | Done: {s['completed']}")

    def on_add() -> None:
        title = title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Please enter a task title.")
            return
        manager.add_task(title, prio_var.get(), due_var.get(), cat_var.get())
        title_var.set("")
        due_var.set("")
        refresh_table()

    def on_toggle() -> None:
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select Task", "Please select a task from the list.")
            return
        tid = int(sel[0])
        manager.toggle_task(tid)
        refresh_table()

    def on_update() -> None:
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select Task", "Please select a task to update with the form fields.")
            return
        tid = int(sel[0])
        title = title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Enter the updated title in the Task Title field.")
            return
        manager.update_task(
            tid,
            title=title,
            priority=prio_var.get(),
            due_date=due_var.get(),
            category=cat_var.get(),
        )
        refresh_table()

    def on_delete() -> None:
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select Task", "Please select a task to delete.")
            return
        tid = int(sel[0])
        manager.delete_task(tid)
        refresh_table()

    def on_select(_event: object) -> None:
        sel = tree.selection()
        if not sel:
            return
        task = manager.get_task(int(sel[0]))
        if task:
            title_var.set(task["title"])
            prio_var.set(task.get("priority", "Medium"))
            cat_var.set(task.get("category", "General"))
            due_var.set(task.get("due_date", ""))

    tree.bind("<<TreeviewSelect>>", on_select)

    # Action Buttons
    btn_frame = tk.Frame(root, bg="#f8fafc", pady=12, padx=16)
    btn_frame.pack(fill="x")

    ttk.Button(btn_frame, text="Add Task", command=on_add).pack(side="left", padx=4)
    ttk.Button(btn_frame, text="Update Selected", command=on_update).pack(side="left", padx=4)
    ttk.Button(btn_frame, text="Toggle Complete", command=on_toggle).pack(side="left", padx=4)
    ttk.Button(btn_frame, text="Delete Selected", command=on_delete).pack(side="left", padx=4)
    ttk.Button(
        btn_frame,
        text="Clear Completed",
        command=lambda: (manager.clear_completed(), refresh_table()),
    ).pack(side="right", padx=4)

    refresh_table()
    root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    elif "--gui" in sys.argv:
        run_gui()
    else:
        # Auto-detect graphical environment
        if os.environ.get("DISPLAY") or sys.platform in ("win32", "darwin"):
            try:
                run_gui()
            except Exception:
                run_cli()
        else:
            run_cli()