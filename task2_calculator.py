"""Task 2: Simple calculator."""


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("=== SIMPLE CALCULATOR ===")
    while True:
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        print("Operations: +  -  *  /  %  **")
        op = input("Choose an operation: ").strip()

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            result = "Error: division by zero" if b == 0 else a / b
        elif op == "%":
            result = "Error: modulo by zero" if b == 0 else a % b
        elif op == "**":
            result = a ** b
        else:
            result = "Error: invalid operation"

        print(f"Result: {result}")
        if input("Calculate again? (y/n): ").strip().lower() != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
