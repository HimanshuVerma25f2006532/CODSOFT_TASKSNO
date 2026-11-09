#!/usr/bin/env python3
"""
CODSOFT - TASK 5: Contact Book Application
Manages contacts (Name, Phone Number, Email, Address) with Add, View, Search,
Update, and Delete functionality, automatic JSON persistence, and both CLI and
Tkinter GUI interfaces.

Usage:
    python3 task5_contact_book.py          # Launches GUI if display available, else CLI
    python3 task5_contact_book.py --cli    # Command-Line Interface mode
    python3 task5_contact_book.py --gui    # Tkinter GUI mode
"""

import json
import os
import sys
from typing import Dict, List, Optional

CONTACTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts_data.json")


class ContactBook:
    """Core manager for storing, searching, updating, and deleting contacts."""

    def __init__(self, filepath: str = CONTACTS_FILE):
        self.filepath = filepath
        self.contacts: List[Dict] = []
        self.load_contacts()

    def load_contacts(self) -> None:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.contacts = data
            except (json.JSONDecodeError, OSError):
                self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.contacts, f, indent=4)
        except OSError as e:
            print(f"Warning: Could not save contacts to {self.filepath}: {e}")

    def _next_id(self) -> int:
        if not self.contacts:
            return 1
        return max(c.get("id", 0) for c in self.contacts) + 1

    def add_contact(self, name: str, phone: str, email: str = "", address: str = "") -> Dict:
        name = name.strip()
        phone = phone.strip()
        if not name or not phone:
            raise ValueError("Contact name and phone number are required.")

        contact = {
            "id": self._next_id(),
            "name": name,
            "phone": phone,
            "email": email.strip(),
            "address": address.strip(),
        }
        self.contacts.append(contact)
        self.save_contacts()
        return contact

    def get_contact(self, contact_id: int) -> Optional[Dict]:
        for c in self.contacts:
            if c["id"] == contact_id:
                return c
        return None

    def search_contacts(self, query: str) -> List[Dict]:
        q = query.strip().lower()
        if not q:
            return list(self.contacts)
        return [
            c
            for c in self.contacts
            if q in c.get("name", "").lower()
            or q in c.get("phone", "").lower()
            or q in c.get("email", "").lower()
        ]

    def update_contact(
        self,
        contact_id: int,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
    ) -> bool:
        contact = self.get_contact(contact_id)
        if not contact:
            return False
        if name is not None and name.strip():
            contact["name"] = name.strip()
        if phone is not None and phone.strip():
            contact["phone"] = phone.strip()
        if email is not None:
            contact["email"] = email.strip()
        if address is not None:
            contact["address"] = address.strip()
        self.save_contacts()
        return True

    def delete_contact(self, contact_id: int) -> bool:
        initial_count = len(self.contacts)
        self.contacts = [c for c in self.contacts if c["id"] != contact_id]
        if len(self.contacts) < initial_count:
            self.save_contacts()
            return True
        return False


# =====================================================================
# Command-Line Interface (CLI)
# =====================================================================

def display_contacts(contacts: List[Dict]) -> None:
    if not contacts:
        print("\n  [No contacts found.]\n")
        return
    print("\n" + "=" * 88)
    print(f"{'ID':<4} | {'Name':<22} | {'Phone Number':<16} | {'Email':<22} | {'Address'}")
    print("-" * 88)
    for c in contacts:
        print(
            f"{c['id']:<4} | {c['name'][:22]:<22} | {c['phone'][:16]:<16} | "
            f"{(c.get('email') or '-')[:22]:<22} | {c.get('address') or '-'}"
        )
    print("=" * 88 + "\n")


def run_cli() -> None:
    book = ContactBook()
    print("=" * 60)
    print("          CODSOFT TASK 5: CONTACT BOOK MANAGER")
    print("=" * 60)

    while True:
        print(f"Total Saved Contacts: {len(book.contacts)}")
        print("1. Add New Contact")
        print("2. View Contact List")
        print("3. Search Contact (by Name or Phone)")
        print("4. Update Contact Details")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            name = input("Enter Full Name: ").strip()
            phone = input("Enter Phone Number: ").strip()
            if not name or not phone:
                print("  Error: Name and Phone Number are required.\n")
                continue
            email = input("Enter Email Address (optional): ").strip()
            address = input("Enter Physical Address (optional): ").strip()
            c = book.add_contact(name, phone, email, address)
            print(f"  Contact '{c['name']}' (ID #{c['id']}) saved!\n")

        elif choice == "2":
            display_contacts(book.contacts)

        elif choice == "3":
            q = input("Enter Name or Phone Number to search: ").strip()
            results = book.search_contacts(q)
            print(f"\nFound {len(results)} matching contact(s):")
            display_contacts(results)

        elif choice == "4":
            display_contacts(book.contacts)
            try:
                cid = int(input("Enter Contact ID to update: ").strip())
            except ValueError:
                print("  Invalid ID.\n")
                continue
            existing = book.get_contact(cid)
            if not existing:
                print(f"  Contact #{cid} not found.\n")
                continue
            print("Press Enter to keep the current value.")
            new_name = input(f"Name [{existing['name']}]: ").strip()
            new_phone = input(f"Phone [{existing['phone']}]: ").strip()
            new_email = input(f"Email [{existing.get('email', '')}]: ").strip()
            new_addr = input(f"Address [{existing.get('address', '')}]: ").strip()

            book.update_contact(
                cid,
                name=new_name if new_name else None,
                phone=new_phone if new_phone else None,
                email=new_email if new_email else existing.get("email", ""),
                address=new_addr if new_addr else existing.get("address", ""),
            )
            print(f"  Contact #{cid} updated.\n")

        elif choice == "5":
            try:
                cid = int(input("Enter Contact ID to delete: ").strip())
            except ValueError:
                print("  Invalid ID.\n")
                continue
            if book.delete_contact(cid):
                print(f"  Contact #{cid} deleted.\n")
            else:
                print(f"  Contact #{cid} not found.\n")

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("  Invalid selection. Please enter 1-6.\n")


# =====================================================================
# Tkinter Graphical User Interface (GUI)
# =====================================================================

def run_gui() -> None:
    import tkinter as tk
    from tkinter import ttk, messagebox

    book = ContactBook()

    root = tk.Tk()
    root.title("CodSoft Task 5 - Contact Book")
    root.geometry("780x520")
    root.minsize(700, 460)
    root.configure(bg="#f8fafc")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    header = tk.Frame(root, bg="#1e293b", pady=12, padx=16)
    header.pack(fill="x")
    tk.Label(
        header,
        text="Contact Book Manager",
        fg="white",
        bg="#1e293b",
        font=("Segoe UI", 15, "bold"),
    ).pack(side="left")

    search_var = tk.StringVar()
    search_entry = ttk.Entry(header, textvariable=search_var, width=28)
    search_entry.pack(side="right", padx=6)
    tk.Label(header, text="Search (Name/Phone):", fg="#cbd5e1", bg="#1e293b", font=("Segoe UI", 10)).pack(side="right")

    # Form
    form = tk.Frame(root, bg="#f8fafc", pady=10, padx=16)
    form.pack(fill="x")

    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    addr_var = tk.StringVar()

    tk.Label(form, text="Name *:", bg="#f8fafc").grid(row=0, column=0, sticky="w")
    ttk.Entry(form, textvariable=name_var, width=26).grid(row=0, column=1, padx=6, pady=4, sticky="we")

    tk.Label(form, text="Phone *:", bg="#f8fafc").grid(row=0, column=2, sticky="w")
    ttk.Entry(form, textvariable=phone_var, width=20).grid(row=0, column=3, padx=6, pady=4, sticky="we")

    tk.Label(form, text="Email:", bg="#f8fafc").grid(row=1, column=0, sticky="w")
    ttk.Entry(form, textvariable=email_var, width=26).grid(row=1, column=1, padx=6, pady=4, sticky="we")

    tk.Label(form, text="Address:", bg="#f8fafc").grid(row=1, column=2, sticky="w")
    ttk.Entry(form, textvariable=addr_var, width=28).grid(row=1, column=3, padx=6, pady=4, sticky="we")

    form.columnconfigure(1, weight=1)
    form.columnconfigure(3, weight=1)

    # Table
    table_frame = tk.Frame(root, bg="#f8fafc", padx=16)
    table_frame.pack(fill="both", expand=True)

    cols = ("id", "name", "phone", "email", "address")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
    for col, heading, w in [
        ("id", "ID", 45),
        ("name", "Name", 160),
        ("phone", "Phone Number", 130),
        ("email", "Email", 170),
        ("address", "Address", 210),
    ]:
        tree.heading(col, text=heading)
        tree.column(col, width=w, anchor="w" if col != "id" else "center")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_table(*_args: object) -> None:
        for row in tree.get_children():
            tree.delete(row)
        for c in book.search_contacts(search_var.get()):
            tree.insert(
                "",
                "end",
                iid=str(c["id"]),
                values=(c["id"], c["name"], c["phone"], c.get("email", ""), c.get("address", "")),
            )

    search_var.trace_add("write", refresh_table)

    def clear_form() -> None:
        name_var.set("")
        phone_var.set("")
        email_var.set("")
        addr_var.set("")

    def on_add() -> None:
        try:
            book.add_contact(name_var.get(), phone_var.get(), email_var.get(), addr_var.get())
            clear_form()
            refresh_table()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))

    def on_update() -> None:
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select Contact", "Select a contact from the table to update.")
            return
        cid = int(sel[0])
        if not name_var.get().strip() or not phone_var.get().strip():
            messagebox.showwarning("Validation Error", "Name and Phone cannot be empty.")
            return
        book.update_contact(cid, name_var.get(), phone_var.get(), email_var.get(), addr_var.get())
        refresh_table()

    def on_delete() -> None:
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select Contact", "Select a contact from the table to delete.")
            return
        cid = int(sel[0])
        book.delete_contact(cid)
        clear_form()
        refresh_table()

    def on_select(_event: object) -> None:
        sel = tree.selection()
        if not sel:
            return
        c = book.get_contact(int(sel[0]))
        if c:
            name_var.set(c["name"])
            phone_var.set(c["phone"])
            email_var.set(c.get("email", ""))
            addr_var.set(c.get("address", ""))

    tree.bind("<<TreeviewSelect>>", on_select)

    btn_frame = tk.Frame(root, bg="#f8fafc", pady=12, padx=16)
    btn_frame.pack(fill="x")
    ttk.Button(btn_frame, text="Add Contact", command=on_add).pack(side="left", padx=4)
    ttk.Button(btn_frame, text="Update Selected", command=on_update).pack(side="left", padx=4)
    ttk.Button(btn_frame, text="Delete Selected", command=on_delete).pack(side="left", padx=4)
    ttk.Button(btn_frame, text="Clear Form", command=clear_form).pack(side="right", padx=4)

    refresh_table()
    root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    elif "--gui" in sys.argv:
        run_gui()
    else:
        if os.environ.get("DISPLAY") or sys.platform in ("win32", "darwin"):
            try:
                run_gui()
            except Exception:
                run_cli()
        else:
            run_cli()