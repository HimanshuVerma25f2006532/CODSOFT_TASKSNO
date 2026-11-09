#!/usr/bin/env python3
"""
CODSOFT - TASK 2: Simple Calculator Application
Prompts the user to input two numbers and an operation choice, performs the
calculation, and displays the formatted result. Supports both CLI and GUI modes.

Usage:
    python3 task2_calculator.py          # Launches CLI by default (or GUI with --gui)
    python3 task2_calculator.py --cli    # Command-Line Interface mode
    python3 task2_calculator.py --gui    # Tkinter GUI Calculator mode
"""

import math
import sys
from typing import Tuple, Union


OPERATIONS = {
    "1": ("+", "Addition"),
    "+": ("+", "Addition"),
    "2": ("-", "Subtraction"),
    "-": ("-", "Subtraction"),
    "3": ("*", "Multiplication"),
    "*": ("*", "Multiplication"),
    "x": ("*", "Multiplication"),
    "4": ("/", "Division"),
    "/": ("/", "Division"),
    "5": ("%", "Modulo (Remainder)"),
    "%": ("%", "Modulo (Remainder)"),
    "6": ("**", "Exponentiation (Power)"),
    "**": ("**", "Exponentiation (Power)"),
    "^": ("**", "Exponentiation (Power)"),
}


def calculate(num1: float, num2: float, operator: str) -> Tuple[float, str]:
    """
    Perform arithmetic calculation on two numbers.
    Returns (result, formatted_expression).
    Raises ZeroDivisionError on division/modulo by zero or ValueError on invalid operator.
    """
    op_key = operator.strip().lower()
    if op_key not in OPERATIONS:
        raise ValueError(f"Unsupported operation: '{operator}'")

    symbol, _ = OPERATIONS[op_key]

    if symbol == "+":
        result = num1 + num2
    elif symbol == "-":
        result = num1 - num2
    elif symbol == "*":
        result = num1 * num2
    elif symbol == "/":
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        result = num1 / num2
    elif symbol == "%":
        if num2 == 0:
            raise ZeroDivisionError("Cannot compute modulo by zero.")
        result = num1 % num2
    elif symbol == "**":
        result = math.pow(num1, num2)
    else:
        raise ValueError(f"Invalid operator symbol: {symbol}")

    expr = f"{format_number(num1)} {symbol} {format_number(num2)} = {format_number(result)}"
    return result, expr


def format_number(val: Union[int, float]) -> str:
    """Format floats cleanly (strip trailing .0 for exact integers)."""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    if isinstance(val, float):
        return f"{val:.6g}"
    return str(val)


# =====================================================================
# Command-Line Interface (CLI)
# =====================================================================

def prompt_float(prompt_text: str) -> float:
    while True:
        raw = input(prompt_text).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  Invalid number '{raw}'. Please enter a valid numeric value.")


def run_cli() -> None:
    print("=" * 55)
    print("          CODSOFT TASK 2: SIMPLE CALCULATOR")
    print("=" * 55)
    history = []

    while True:
        print("\nAvailable Operations:")
        print("  1. Addition (+)")
        print("  2. Subtraction (-)")
        print("  3. Multiplication (*)")
        print("  4. Division (/)")
        print("  5. Modulo / Remainder (%)")
        print("  6. Exponentiation (**)")
        print("  H. View Calculation History")
        print("  Q. Quit")

        choice = input("\nChoose an operation (1-6, +, -, *, /, %, **, H, Q): ").strip()
        if choice.lower() in ("q", "quit", "exit"):
            print("Thank you for using the Calculator. Goodbye!")
            break
        if choice.lower() in ("h", "history"):
            if not history:
                print("\n  [No calculations performed yet.]")
            else:
                print("\nCalculation History:")
                for idx, item in enumerate(history, start=1):
                    print(f"  {idx}. {item}")
            continue

        if choice.lower() not in OPERATIONS:
            print("  Invalid choice! Please select a valid operation from the menu.")
            continue

        num1 = prompt_float("Enter the first number: ")
        num2 = prompt_float("Enter the second number: ")

        try:
            _, expression = calculate(num1, num2, choice)
            history.append(expression)
            print("\n" + "-" * 40)
            print(f"  Result: {expression}")
            print("-" * 40)
        except ZeroDivisionError as zde:
            print(f"\n  Math Error: {zde}")
        except OverflowError:
            print("\n  Math Error: Result is too large to represent.")
        except ValueError as ve:
            print(f"\n  Input Error: {ve}")


# =====================================================================
# Tkinter Graphical User Interface (GUI)
# =====================================================================

def run_gui() -> None:
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("CodSoft Task 2 - Calculator")
    root.geometry("420x460")
    root.resizable(False, False)
    root.configure(bg="#0f172a")

    tk.Label(
        root,
        text="Simple Arithmetic Calculator",
        bg="#0f172a",
        fg="#f8fafc",
        font=("Segoe UI", 14, "bold"),
        pady=14,
    ).pack(fill="x")

    card = tk.Frame(root, bg="#1e293b", padx=20, pady=18)
    card.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    tk.Label(card, text="First Number:", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 10)).pack(anchor="w")
    num1_var = tk.StringVar()
    tk.Entry(card, textvariable=num1_var, font=("Segoe UI", 12), bg="#334155", fg="white", insertbackground="white").pack(fill="x", pady=(4, 12))

    tk.Label(card, text="Second Number:", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 10)).pack(anchor="w")
    num2_var = tk.StringVar()
    tk.Entry(card, textvariable=num2_var, font=("Segoe UI", 12), bg="#334155", fg="white", insertbackground="white").pack(fill="x", pady=(4, 12))

    tk.Label(card, text="Operation:", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 10)).pack(anchor="w")
    op_var = tk.StringVar(value="+")
    op_combo = ttk.Combobox(
        card,
        textvariable=op_var,
        values=["+", "-", "*", "/", "%", "**"],
        state="readonly",
        font=("Segoe UI", 11),
    )
    op_combo.pack(fill="x", pady=(4, 16))

    result_var = tk.StringVar(value="Result will appear here")
    result_lbl = tk.Label(
        card,
        textvariable=result_var,
        bg="#0f172a",
        fg="#38bdf8",
        font=("Segoe UI", 12, "bold"),
        pady=12,
        wraplength=340,
    )
    result_lbl.pack(fill="x", pady=(4, 14))

    def on_calculate() -> None:
        try:
            n1 = float(num1_var.get().strip())
            n2 = float(num2_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values in both fields.")
            return
        try:
            _, expr = calculate(n1, n2, op_var.get())
            result_var.set(expr)
        except ZeroDivisionError as e:
            messagebox.showerror("Math Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_clear() -> None:
        num1_var.set("")
        num2_var.set("")
        op_var.set("+")
        result_var.set("Result will appear here")

    btn_row = tk.Frame(card, bg="#1e293b")
    btn_row.pack(fill="x")
    tk.Button(
        btn_row,
        text="Calculate",
        command=on_calculate,
        bg="#0284c7",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        pady=6,
        relief="flat",
    ).pack(side="left", fill="x", expand=True, padx=(0, 6))
    tk.Button(
        btn_row,
        text="Clear",
        command=on_clear,
        bg="#475569",
        fg="white",
        font=("Segoe UI", 10),
        pady=6,
        relief="flat",
    ).pack(side="right", fill="x", expand=True, padx=(6, 0))

    root.mainloop()


if __name__ == "__main__":
    if "--gui" in sys.argv:
        run_gui()
    else:
        run_cli()