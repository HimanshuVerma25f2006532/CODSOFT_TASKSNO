"""Task 5: Contact Book (saved to contacts.json)."""
import json
import os

FILE = "contacts.json"


def load():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save(contacts):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)


def add(contacts):
    name = input("Name: ").strip()
    if not name:
        print("Name is required.")
        return
    contacts.append({
        "name": name,
        "phone": input("Phone: ").strip(),
        "email": input("Email: ").strip(),
        "address": input("Address: ").strip(),
    })
    save(contacts)
    print("Contact added.")


def view(contacts):
    if not contacts:
        print("No contacts saved.")
        return
    for i, c in enumerate(contacts, 1):
        print(f"{i}. {c['name']} - {c['phone']}")


def search(contacts):
    q = input("Search by name or phone: ").strip().lower()
    matches = [c for c in contacts if q in c["name"].lower() or q in c["phone"]]
    if not matches:
        print("No match found.")
    for c in matches:
        print(f"\nName: {c['name']}\nPhone: {c['phone']}\n"
              f"Email: {c['email']}\nAddress: {c['address']}")


def pick(contacts):
    view(contacts)
    if not contacts:
        return None
    try:
        n = int(input("Contact number: "))
        if 1 <= n <= len(contacts):
            return n - 1
    except ValueError:
        pass
    print("Invalid number.")
    return None


def update(contacts):
    i = pick(contacts)
    if i is None:
        return
    print("Press Enter to keep the current value.")
    for field in ("name", "phone", "email", "address"):
        new = input(f"{field.capitalize()} [{contacts[i][field]}]: ").strip()
        if new:
            contacts[i][field] = new
    save(contacts)
    print("Contact updated.")


def delete(contacts):
    i = pick(contacts)
    if i is None:
        return
    removed = contacts.pop(i)
    save(contacts)
    print(f"Deleted {removed['name']}.")


def main():
    contacts = load()
    actions = {"1": add, "2": view, "3": search, "4": update, "5": delete}
    while True:
        print("\n--- CONTACT BOOK ---")
        print("1. Add  2. View all  3. Search  4. Update  5. Delete  6. Exit")
        choice = input("Choose: ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(contacts)
        else:
            print("Please pick 1-6.")


if __name__ == "__main__":
    main()
