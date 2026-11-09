#!/usr/bin/env python3
"""
CODSOFT - TASK 3: Password Generator Application
Generates strong, cryptographically random passwords based on user-specified
length and character complexity preferences.

Usage:
    python3 task3_password_generator.py          # Command-Line Interface mode
    python3 task3_password_generator.py --gui    # Tkinter GUI mode
"""

import secrets
import string
import sys
from typing import Tuple

AMBIGUOUS_CHARS = set("lI1O0")


def generate_password(
    length: int = 12,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """
    Generate a cryptographically secure random password guaranteeing at least
    one character from each enabled complexity pool when length permits.
    """
    if length < 1:
        raise ValueError("Password length must be at least 1.")

    pools = []
    if use_lowercase:
        pool = string.ascii_lowercase
        if exclude_ambiguous:
            pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARS)
        if pool:
            pools.append(pool)
    if use_uppercase:
        pool = string.ascii_uppercase
        if exclude_ambiguous:
            pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARS)
        if pool:
            pools.append(pool)
    if use_digits:
        pool = string.digits
        if exclude_ambiguous:
            pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARS)
        if pool:
            pools.append(pool)
    if use_symbols:
        pool = "!@#$%^&*()-_=+[]{};:,.<>?"
        pools.append(pool)

    if not pools:
        raise ValueError("At least one character type must be selected.")

    all_chars = "".join(pools)

    # Ensure at least one character from each selected category if length >= len(pools)
    password_chars = []
    if length >= len(pools):
        for pool in pools:
            password_chars.append(secrets.choice(pool))

    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(all_chars))

    # Shuffle using cryptographically strong SystemRandom
    sys_rng = secrets.SystemRandom()
    sys_rng.shuffle(password_chars)

    return "".join(password_chars)


def evaluate_strength(password: str) -> Tuple[str, int]:
    """
    Evaluate password strength on a 0-100 score and return (label, score).
    """
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    categories = sum([has_lower, has_upper, has_digit, has_symbol])
    score = min(60, length * 4) + categories * 10

    if length < 6:
        score = min(score, 35)

    if score >= 85:
        return "Very Strong", score
    if score >= 65:
        return "Strong", score
    if score >= 45:
        return "Moderate", score
    return "Weak", score


# =====================================================================
# Command-Line Interface (CLI)
# =====================================================================

def ask_yes_no(prompt_text: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    raw = input(f"{prompt_text} {suffix}: ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes", "1", "true")


def run_cli() -> None:
    print("=" * 60)
    print("         CODSOFT TASK 3: PASSWORD GENERATOR")
    print("=" * 60)

    while True:
        try:
            raw_len = input("\nEnter desired password length (e.g., 12, or 'q' to quit): ").strip()
            if raw_len.lower() in ("q", "quit", "exit"):
                print("Goodbye! Keep your accounts secure.")
                break
            length = int(raw_len)
            if length < 1 or length > 256:
                print("  Please enter a length between 1 and 256.")
                continue
        except ValueError:
            print("  Invalid input. Please enter a whole number.")
            continue

        print("\nSelect Complexity Level:")
        print("  1. High Complexity (Uppercase + Lowercase + Digits + Symbols) [Recommended]")
        print("  2. Alphanumeric Only (Uppercase + Lowercase + Digits)")
        print("  3. Letters Only (Uppercase + Lowercase)")
        print("  4. PIN / Digits Only (0-9)")
        print("  5. Custom Character Set")

        comp = input("Choose complexity option (1-5) [default: 1]: ").strip() or "1"

        use_upper, use_lower, use_digits, use_symbols, no_ambig = True, True, True, True, False
        if comp == "2":
            use_symbols = False
        elif comp == "3":
            use_digits = False
            use_symbols = False
        elif comp == "4":
            use_upper = False
            use_lower = False
            use_symbols = False
        elif comp == "5":
            use_upper = ask_yes_no("Include Uppercase letters (A-Z)?", True)
            use_lower = ask_yes_no("Include Lowercase letters (a-z)?", True)
            use_digits = ask_yes_no("Include Digits (0-9)?", True)
            use_symbols = ask_yes_no("Include Symbols (!@#$...)?", True)
            no_ambig = ask_yes_no("Exclude ambiguous characters (l, I, 1, O, 0)?", False)

        try:
            pwd = generate_password(
                length=length,
                use_uppercase=use_upper,
                use_lowercase=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_ambiguous=no_ambig,
            )
            label, score = evaluate_strength(pwd)
            print("\n" + "=" * 60)
            print(f"  Generated Password : {pwd}")
            print(f"  Password Strength  : {label} ({score}/100)")
            print("=" * 60)
        except ValueError as e:
            print(f"\n  Error: {e}")


# =====================================================================
# Tkinter Graphical User Interface (GUI)
# =====================================================================

def run_gui() -> None:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title("CodSoft Task 3 - Password Generator")
    root.geometry("460x440")
    root.resizable(False, False)
    root.configure(bg="#0f172a")

    tk.Label(
        root,
        text="Secure Password Generator",
        bg="#0f172a",
        fg="white",
        font=("Segoe UI", 14, "bold"),
        pady=14,
    ).pack(fill="x")

    frame = tk.Frame(root, bg="#1e293b", padx=20, pady=16)
    frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    len_row = tk.Frame(frame, bg="#1e293b")
    len_row.pack(fill="x", pady=6)
    tk.Label(len_row, text="Password Length:", bg="#1e293b", fg="#e2e8f0", font=("Segoe UI", 10)).pack(side="left")
    len_var = tk.IntVar(value=16)
    tk.Spinbox(len_row, from_=4, to=128, textvariable=len_var, width=8, font=("Segoe UI", 11)).pack(side="right")

    upper_var = tk.BooleanVar(value=True)
    lower_var = tk.BooleanVar(value=True)
    digit_var = tk.BooleanVar(value=True)
    symbol_var = tk.BooleanVar(value=True)
    ambig_var = tk.BooleanVar(value=False)

    for text, var in [
        ("Include Uppercase Letters (A-Z)", upper_var),
        ("Include Lowercase Letters (a-z)", lower_var),
        ("Include Numbers (0-9)", digit_var),
        ("Include Special Symbols (!@#$...)", symbol_var),
        ("Exclude Ambiguous Characters (l, I, 1, O, 0)", ambig_var),
    ]:
        tk.Checkbutton(
            frame,
            text=text,
            variable=var,
            bg="#1e293b",
            fg="#cbd5e1",
            selectcolor="#0f172a",
            activebackground="#1e293b",
            activeforeground="white",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=2)

    pwd_var = tk.StringVar(value="")
    pwd_entry = tk.Entry(
        frame,
        textvariable=pwd_var,
        font=("Consolas", 13, "bold"),
        bg="#0f172a",
        fg="#38bdf8",
        justify="center",
        relief="flat",
    )
    pwd_entry.pack(fill="x", ipady=8, pady=(14, 6))

    strength_var = tk.StringVar(value="Strength: -")
    tk.Label(frame, textvariable=strength_var, bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 9)).pack()

    def on_generate() -> None:
        try:
            pwd = generate_password(
                length=int(len_var.get()),
                use_uppercase=upper_var.get(),
                use_lowercase=lower_var.get(),
                use_digits=digit_var.get(),
                use_symbols=symbol_var.get(),
                exclude_ambiguous=ambig_var.get(),
            )
            pwd_var.set(pwd)
            label, score = evaluate_strength(pwd)
            strength_var.set(f"Strength: {label} ({score}/100)")
        except ValueError as e:
            messagebox.showwarning("Options Error", str(e))

    def on_copy() -> None:
        if not pwd_var.get():
            return
        root.clipboard_clear()
        root.clipboard_append(pwd_var.get())
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    btn_row = tk.Frame(frame, bg="#1e293b")
    btn_row.pack(fill="x", pady=(12, 0))
    tk.Button(
        btn_row,
        text="Generate Password",
        command=on_generate,
        bg="#0284c7",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        pady=6,
        relief="flat",
    ).pack(side="left", fill="x", expand=True, padx=(0, 6))
    tk.Button(
        btn_row,
        text="Copy",
        command=on_copy,
        bg="#475569",
        fg="white",
        font=("Segoe UI", 10),
        pady=6,
        relief="flat",
    ).pack(side="right", padx=(6, 0))

    on_generate()
    root.mainloop()


if __name__ == "__main__":
    if "--gui" in sys.argv:
        run_gui()
    else:
        run_cli()