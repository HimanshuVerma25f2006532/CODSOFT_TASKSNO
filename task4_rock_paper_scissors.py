"""Task 4: Rock-Paper-Scissors with score tracking."""
import random

CHOICES = ["rock", "paper", "scissors"]
BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}


def winner(user, comp):
    if user == comp:
        return "tie"
    return "user" if BEATS[user] == comp else "computer"


def main():
    print("=== ROCK - PAPER - SCISSORS ===")
    print("Type rock, paper or scissors (or r/p/s).")
    user_score = comp_score = 0
    short = {"r": "rock", "p": "paper", "s": "scissors"}

    while True:
        raw = input("\nYour choice: ").strip().lower()
        user = short.get(raw, raw)
        if user not in CHOICES:
            print("Invalid choice, try again.")
            continue

        comp = random.choice(CHOICES)
        print(f"You chose: {user} | Computer chose: {comp}")
        result = winner(user, comp)
        if result == "tie":
            print("It's a tie!")
        elif result == "user":
            user_score += 1
            print("You win this round!")
        else:
            comp_score += 1
            print("You lose this round!")
        print(f"Score -> You: {user_score} | Computer: {comp_score}")

        if input("Play again? (y/n): ").strip().lower() != "y":
            print(f"\nFinal score -> You: {user_score} | Computer: {comp_score}")
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
