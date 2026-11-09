"""Task 1: Command-line To-Do List (saved to todo.json)."""
import json
import os

FILE = "todo.json"


def load():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def show(tasks):
    if not tasks:
        print("\nNo tasks yet.")
        return
    print("\nYour tasks:")
    for i, t in enumerate(tasks, 1):
        mark = "x" if t["done"] else " "
        print(f"  {i}. [{mark}] {t['title']}")


def ask_index(tasks, prompt):
    try:
        n = int(input(prompt))
        if 1 <= n <= len(tasks):
            return n - 1
    except ValueError:
        pass
    print("Invalid task number.")
    return None


def main():
    tasks = load()
    while True:
        print("\n--- TO-DO LIST ---")
        print("1. View  2. Add  3. Update  4. Mark done  5. Delete  6. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            show(tasks)
        elif choice == "2":
            title = input("New task: ").strip()
            if title:
                tasks.append({"title": title, "done": False})
                save(tasks)
                print("Task added.")
        elif choice in ("3", "4", "5"):
            show(tasks)
            if not tasks:
                continue
            i = ask_index(tasks, "Task number: ")
            if i is None:
                continue
            if choice == "3":
                new = input("New title: ").strip()
                if new:
                    tasks[i]["title"] = new
            elif choice == "4":
                tasks[i]["done"] = True
            else:
                tasks.pop(i)
            save(tasks)
            print("Done.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please pick 1-6.")


if __name__ == "__main__":
    main()
