#!/usr/bin/env python3
"""
CODSOFT - TASK 4: Rock-Paper-Scissors Game
Interactive Rock-Paper-Scissors game against the computer with multi-round
score tracking, win/loss/tie logic, and both CLI and Tkinter GUI interfaces.

Usage:
    python3 task4_rock_paper_scissors.py          # Command-Line Interface mode
    python3 task4_rock_paper_scissors.py --gui    # Tkinter GUI mode
"""

import random
import sys
from typing import Optional, Tuple

CHOICES = ("rock", "paper", "scissors")

ALIASES = {
    "r": "rock",
    "rock": "rock",
    "1": "rock",
    "p": "paper",
    "paper": "paper",
    "2": "paper",
    "s": "scissors",
    "scissors": "scissors",
    "3": "scissors",
}

WIN_RULES = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}


def normalize_choice(user_input: str) -> Optional[str]:
    """Convert user shorthand or full input to canonical choice ('rock', 'paper', 'scissors')."""
    return ALIASES.get(user_input.strip().lower())


def get_computer_choice() -> str:
    """Return a random choice for the computer."""
    return random.choice(CHOICES)


def determine_winner(user_choice: str, computer_choice: str) -> Tuple[str, str]:
    """
    Determine the winner of a round.
    Returns (outcome, explanation) where outcome is 'win', 'lose', or 'tie'.
    """
    u = normalize_choice(user_choice)
    c = normalize_choice(computer_choice)
    if u not in CHOICES or c not in CHOICES:
        raise ValueError("Invalid choice provided.")

    if u == c:
        return "tie", f"Both chose {u.capitalize()}. It's a tie!"

    if WIN_RULES[u] == c:
        return "win", f"{u.capitalize()} beats {c.capitalize()}. You win this round!"
    else:
        return "lose", f"{c.capitalize()} beats {u.capitalize()}. Computer wins this round!"


# =====================================================================
# Command-Line Interface (CLI)
# =====================================================================

def run_cli() -> None:
    print("=" * 60)
    print("       CODSOFT TASK 4: ROCK - PAPER - SCISSORS GAME")
    print("=" * 60)
    print("Rules: Rock beats Scissors | Scissors beats Paper | Paper beats Rock\n")

    user_score = 0
    computer_score = 0
    ties = 0
    round_num = 1

    while True:
        print(f"--- Round {round_num} ---")
        raw = input("Choose [R]ock, [P]aper, [S]cissors (or [Q]uit): ").strip()

        if raw.lower() in ("q", "quit", "exit"):
            break

        user_choice = normalize_choice(raw)
        if not user_choice:
            print("  Invalid input! Please enter 'rock' (r), 'paper' (p), or 'scissors' (s).\n")
            continue

        comp_choice = get_computer_choice()
        outcome, message = determine_winner(user_choice, comp_choice)

        if outcome == "win":
            user_score += 1
        elif outcome == "lose":
            computer_score += 1
        else:
            ties += 1

        print("\n" + "-" * 50)
        print(f"  Your Choice     : {user_choice.capitalize()}")
        print(f"  Computer Choice : {comp_choice.capitalize()}")
        print(f"  Result          : {message}")
        print(f"  Scoreboard      : You {user_score}  |  Computer {computer_score}  |  Ties {ties}")
        print("-" * 50 + "\n")

        again = input("Play another round? (Y/n): ").strip().lower()
        if again in ("n", "no"):
            break
        round_num += 1
        print()

    print("\n" + "=" * 60)
    print("                    FINAL SCOREBOARD")
    print(f"         You: {user_score}   |   Computer: {computer_score}   |   Ties: {ties}")
    if user_score > computer_score:
        print("         Congratulations! You won the match!")
    elif computer_score > user_score:
        print("         Computer won the match! Better luck next time.")
    else:
        print("         The match ended in an overall tie!")
    print("=" * 60)


# =====================================================================
# Tkinter Graphical User Interface (GUI)
# =====================================================================

def run_gui() -> None:
    import tkinter as tk

    root = tk.Tk()
    root.title("CodSoft Task 4 - Rock Paper Scissors")
    root.geometry("480x430")
    root.resizable(False, False)
    root.configure(bg="#0f172a")

    state = {"user": 0, "comp": 0, "ties": 0}

    tk.Label(
        root,
        text="Rock - Paper - Scissors",
        bg="#0f172a",
        fg="white",
        font=("Segoe UI", 16, "bold"),
        pady=14,
    ).pack()

    score_var = tk.StringVar(value="You: 0   |   Computer: 0   |   Ties: 0")
    tk.Label(
        root,
        textvariable=score_var,
        bg="#1e293b",
        fg="#38bdf8",
        font=("Segoe UI", 12, "bold"),
        pady=10,
    ).pack(fill="x", padx=20)

    info_var = tk.StringVar(value="Select Rock, Paper, or Scissors to start playing!")
    tk.Label(
        root,
        textvariable=info_var,
        bg="#0f172a",
        fg="#e2e8f0",
        font=("Segoe UI", 11),
        wraplength=420,
        justify="center",
        pady=24,
    ).pack(fill="x", padx=20)

    def play(user_pick: str) -> None:
        comp_pick = get_computer_choice()
        outcome, msg = determine_winner(user_pick, comp_pick)
        if outcome == "win":
            state["user"] += 1
        elif outcome == "lose":
            state["comp"] += 1
        else:
            state["ties"] += 1

        score_var.set(f"You: {state['user']}   |   Computer: {state['comp']}   |   Ties: {state['ties']}")
        info_var.set(
            f"You chose: {user_pick.capitalize()}\n"
            f"Computer chose: {comp_pick.capitalize()}\n\n"
            f"{msg}"
        )

    def reset_scores() -> None:
        state["user"] = 0
        state["comp"] = 0
        state["ties"] = 0
        score_var.set("You: 0   |   Computer: 0   |   Ties: 0")
        info_var.set("Scores reset! Pick a move to begin a new match.")

    btn_frame = tk.Frame(root, bg="#0f172a")
    btn_frame.pack(pady=10)

    for move, color in [("rock", "#0284c7"), ("paper", "#059669"), ("scissors", "#d97706")]:
        tk.Button(
            btn_frame,
            text=move.capitalize(),
            command=lambda m=move: play(m),
            bg=color,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=10,
            pady=8,
            relief="flat",
        ).pack(side="left", padx=8)

    tk.Button(
        root,
        text="Reset Scoreboard",
        command=reset_scores,
        bg="#334155",
        fg="#cbd5e1",
        font=("Segoe UI", 10),
        pady=5,
        padx=14,
        relief="flat",
    ).pack(pady=16)

    root.mainloop()


if __name__ == "__main__":
    if "--gui" in sys.argv:
        run_gui()
    else:
        run_cli()