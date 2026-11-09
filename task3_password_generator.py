"""Task 3: Password generator."""
import secrets
import string


def generate(length, use_upper, use_digits, use_symbols):
    pools = [string.ascii_lowercase]
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    # Guarantee at least one character from each chosen pool
    chars = [secrets.choice(p) for p in pools]
    all_chars = "".join(pools)
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def yes(prompt):
    return input(prompt + " (y/n): ").strip().lower() == "y"


def main():
    print("=== PASSWORD GENERATOR ===")
    while True:
        try:
            length = int(input("Password length (min 4): "))
            if length >= 4:
                break
            print("Length must be at least 4.")
        except ValueError:
            print("Enter a whole number.")

    upper = yes("Include uppercase letters?")
    digits = yes("Include digits?")
    symbols = yes("Include symbols?")
    print("\nGenerated password:", generate(length, upper, digits, symbols))


if __name__ == "__main__":
    main()
