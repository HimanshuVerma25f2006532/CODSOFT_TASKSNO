# CODSOFT Python Programming Internship Tasks (`CODSOFT_TASKSNO`)

**GitHub Repository:** <https://github.com/HimanshuVerma25f2006532/CODSOFT_TASKSNO>

**Git Remote URL:** `https://github.com/HimanshuVerma25f2006532/CODSOFT_TASKSNO.git`

This repository contains complete Python implementations (supporting both **Command-Line Interface (CLI)** and **Tkinter Graphical User Interface (GUI)** modes) for all five tasks of the **CodSoft Python Programming Internship**.

## Repository Structure

| Task | File Name | Description | Modes Supported | 
| ----- | ----- | ----- | ----- | 
| **Task 1** | `task1_todo_list.py` | To-Do List application with task creation, updates, priority & category tags, completion toggling, filtering, and JSON persistence | CLI & Tkinter GUI | 
| **Task 2** | `task2_calculator.py` | Arithmetic calculator supporting addition, subtraction, multiplication, division, modulo, exponentiation, and calculation history | CLI & Tkinter GUI | 
| **Task 3** | `task3_password_generator.py` | Cryptographically secure password generator (`secrets` module) with customizable length, character sets, and strength scoring | CLI & Tkinter GUI | 
| **Task 4** | `task4_rock_paper_scissors.py` | Interactive Rock-Paper-Scissors game against the computer with multi-round score tracking and replay loop | CLI & Tkinter GUI | 
| **Task 5** | `task5_contact_book.py` | Contact Book manager storing name, phone, email, and address with add, view, search, update, delete, and JSON storage | CLI & Tkinter GUI | 

## Requirements

* **Python 3.8+** (uses only standard library modules: `json`, `os`, `sys`, `math`, `secrets`, `string`, `random`, `datetime`, `tkinter`). No external packages are required.

## Cloning the Repository

```
git clone https://github.com/HimanshuVerma25f2006532/CODSOFT_TASKSNO.git
cd CODSOFT_TASKSNO

```

## Running Each Task

### Task 1: To-Do List Application

```
python3 task1_todo_list.py --cli   # Run in terminal (CLI mode)
python3 task1_todo_list.py --gui   # Launch Tkinter desktop window

```

### Task 2: Calculator

```
python3 task2_calculator.py --cli  # Run in terminal (CLI mode)
python3 task2_calculator.py --gui  # Launch Tkinter desktop calculator

```

### Task 3: Password Generator

```
python3 task3_password_generator.py --cli  # Run in terminal (CLI mode)
python3 task3_password_generator.py --gui  # Launch Tkinter GUI generator

```

### Task 4: Rock-Paper-Scissors Game

```
python3 task4_rock_paper_scissors.py --cli  # Play in terminal
python3 task4_rock_paper_scissors.py --gui  # Play in Tkinter GUI window

```

### Task 5: Contact Book

```
python3 task5_contact_book.py --cli  # Run in terminal (CLI mode)
python3 task5_contact_book.py --gui  # Launch Tkinter GUI Contact Book

```

## How to Push These Files to `HimanshuVerma25f2006532/CODSOFT_TASKSNO`

Run the following commands on your machine inside the folder containing the downloaded files to push all 5 tasks to your GitHub repository:

```
# 1. Initialize a local Git repository and stage all files
git init
git add README.md task1_todo_list.py task2_calculator.py task3_password_generator.py task4_rock_paper_scissors.py task5_contact_book.py
git commit -m "Add CodSoft Python Internship Tasks 1 to 5"

# 2. Set the default branch to main
git branch -M main

# 3. Link your GitHub repository
git remote add origin https://github.com/HimanshuVerma25f2006532/CODSOFT_TASKSNO.git

# 4. Push the code to GitHub
git push -u origin main

```