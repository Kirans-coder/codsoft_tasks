import tkinter as tk
from tkinter import messagebox
import json
import os

BG = "#f0f4f7"
HEADER_COLOR = "#34495e"
BTN_PRIMARY = "#1abc9c"
BTN_ALERT = "#e74c3c"
TEXT_COLOR = "#2c3e50"
TITLE_FONT = ("Helvetica", 22, "bold")
BTN_FONT = ("Helvetica", 12)
ENTRY_FONT = ("Helvetica", 12)

DATA_FILE = "contacts_data.json"

class ModernContactBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Contact Book")
        self.geometry("700x600")
        self.config(bg=BG)
        self.resizable(False, False)
        self.contact_list = []
        self.load_contacts()
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="📇 Modern Contact Book", font=TITLE_FONT, bg=BG, fg=HEADER_COLOR).pack(pady=15)

        form_frame = tk.Frame(self, bg=BG)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:", bg=BG, font=ENTRY_FONT).grid(row=0, column=0, sticky="e")
        self.name_field = tk.Entry(form_frame, width=30, font=ENTRY_FONT)
        self.name_field.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Phone:", bg=BG, font=ENTRY_FONT).grid(row=1, column=0, sticky="e")
        self.phone_field = tk.Entry(form_frame, width=30, font=ENTRY_FONT)
        self.phone_field.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email:", bg=BG, font=ENTRY_FONT).grid(row=2, column=0, sticky="e")
        self.email_field = tk.Entry(form_frame, width=30, font=ENTRY_FONT)
        self.email_field.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Address:", bg=BG, font=ENTRY_FONT).grid(row=3, column=0, sticky="e")
        self.address_field = tk.Entry(form_frame, width=30, font=ENTRY_FONT)
        self.address_field.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Add Contact", width=15, bg=BTN_PRIMARY, fg="white", font=BTN_FONT, command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Contact", width=15, bg=BTN_PRIMARY, fg="white", font=BTN_FONT, command=self.update_contact).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Contact", width=15, bg=BTN_ALERT, fg="white", font=BTN_FONT, command=self.delete_contact).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Search", width=15, bg=BTN_PRIMARY, fg="white", font=BTN_FONT, command=self.search_contact).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Show All", width=15, bg=BTN_PRIMARY, fg="white", font=BTN_FONT, command=self.show_contacts).grid(row=0, column=4, padx=5)

        list_frame = tk.Frame(self, bg=BG)
        list_frame.pack(pady=10)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_box = tk.Listbox(list_frame, width=90, height=18, font=("Courier", 11), yscrollcommand=scrollbar.set)
        self.contact_box.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)
        scrollbar.config(command=self.contact_box.yview)

        self.contact_box.bind("<<ListboxSelect>>", self.on_select)
        self.show_contacts()

    def load_contacts(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.contact_list = json.load(f)

    def save_contacts(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.contact_list, f, indent=4)

    def add_contact(self):
        name = self.name_field.get().strip()
        phone = self.phone_field.get().strip()
        email = self.email_field.get().strip()
        address = self.address_field.get().strip()
        if name and phone:
            self.contact_list.append({"name": name, "phone": phone, "email": email, "address": address})
            self.save_contacts()
            self.show_contacts()
            self.clear_fields()
        else:
            messagebox.showwarning("Missing Data", "Name and Phone are required!")

    def update_contact(self):
        selected = self.contact_box.curselection()
        if selected:
            idx = selected[0]
            name = self.name_field.get().strip()
            phone = self.phone_field.get().strip()
            email = self.email_field.get().strip()
            address = self.address_field.get().strip()
            if name and phone:
                self.contact_list[idx] = {"name": name, "phone": phone, "email": email, "address": address}
                self.save_contacts()
                self.show_contacts()
                self.clear_fields()
            else:
                messagebox.showwarning("Missing Data", "Name and Phone are required!")
        else:
            messagebox.showinfo("Select Contact", "Select a contact to update.")

    def delete_contact(self):
        selected = self.contact_box.curselection()
        if selected:
            idx = selected[0]
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure to delete this contact?")
            if confirm:
                del self.contact_list[idx]
                self.save_contacts()
                self.show_contacts()
                self.clear_fields()
        else:
            messagebox.showinfo("Select Contact", "Select a contact to delete.")

    def search_contact(self):
        query_name = self.name_field.get().strip().lower()
        query_phone = self.phone_field.get().strip()
        self.contact_box.delete(0, tk.END)
        for c in self.contact_list:
            if (query_name and query_name in c["name"].lower()) or (query_phone and query_phone in c["phone"]):
                self.contact_box.insert(tk.END, f"{c['name']:20} | {c['phone']:15} | {c['email']:25} | {c['address']}")

    def show_contacts(self):
        self.contact_box.delete(0, tk.END)
        for c in self.contact_list:
            self.contact_box.insert(tk.END, f"{c['name']:20} | {c['phone']:15} | {c['email']:25} | {c['address']}")

    def on_select(self, event):
        if self.contact_box.curselection():
            idx = self.contact_box.curselection()[0]
            c = self.contact_list[idx]
            self.name_field.delete(0, tk.END)
            self.name_field.insert(0, c["name"])
            self.phone_field.delete(0, tk.END)
            self.phone_field.insert(0, c["phone"])
            self.email_field.delete(0, tk.END)
            self.email_field.insert(0, c["email"])
            self.address_field.delete(0, tk.END)
            self.address_field.insert(0, c["address"])

    def clear_fields(self):
        self.name_field.delete(0, tk.END)
        self.phone_field.delete(0, tk.END)
        self.email_field.delete(0, tk.END)
        self.address_field.delete(0, tk.END)

if __name__ == "__main__":
    app = ModernContactBook()
    app.mainloop()
