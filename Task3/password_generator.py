from tkinter import *
import tkinter.messagebox as msg
import random
import re

class PasswordGenerator(Tk):
    def __init__(self):
        super().__init__()
        # Calculate center position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width = 500
        app_height = 280
        set_x = int((screen_width / 2) - (app_width / 2))
        set_y = int((screen_height / 2) - (app_height / 2))
        self.geometry(f'{app_width}x{app_height}+{set_x}+{set_y}')
        self.title("Password Generator")
        self.resizable(False, False)
        
        # Build UI components
        self.app_heading_frame = self.create_app_heading_frame()
        self.create_heading_label()
        self.length_input_frame = self.create_length_input_frame()
        self.create_password_length_label()
        self.password_length_entry = self.create_password_length_entry()
        self.strength_input_frame = self.create_strength_input_frame()
        self.create_password_strength_label()
        self.choice = StringVar()
        self.choice.set("high") # Default to high security
        self.create_strength_radio_options()
        self.button_frame = self.create_button_frame()
        self.create_generate_button()

    def create_app_heading_frame(self):
        frame = Frame(self, height=50, bg="#2b2e30")
        frame.pack(fill=X)
        return frame

    def create_heading_label(self):
        label = Label(self.app_heading_frame, text="Password Generator", font=("Helvetica", 23, "bold"), fg="#b1ccea", bg="#2b2e30")
        label.pack()

    def create_length_input_frame(self):
        frame = Frame(self, bg="#e5e7ea", height=300, padx=20, pady=20)
        frame.pack(fill=BOTH)
        return frame

    def create_password_length_label(self):
        label = Label(self.length_input_frame, text="Set password length", font=("Helvetica", 16), bg="#e5e7ea", fg="#1a0944")
        label.pack(side=LEFT, padx=(0, 10))

    def create_password_length_entry(self):
        entry = Entry(self.length_input_frame, width=3, fg="#1e4976", font=("Helvetica", 13))
        entry.pack(side=LEFT, ipady=2, ipadx=2)
        return entry

    def create_strength_input_frame(self):
        frame = Frame(self, bg="#e5e7ea", height=300, padx=20, pady=20)
        frame.pack(fill=BOTH)
        return frame

    def create_password_strength_label(self):
        label = Label(self.strength_input_frame, text="Set password strength", font=("Helvetica", 16), bg="#e5e7ea", fg="#1a0944")
        label.pack(anchor=W)

    def create_strength_radio_options(self):
        option1 = Radiobutton(self.strength_input_frame, text="low", value="low", variable=self.choice, font=("Helvetica", 13), bg="#e5e7ea")
        option2 = Radiobutton(self.strength_input_frame, text="medium", value="medium", variable=self.choice, font=("Helvetica", 13), bg="#e5e7ea")
        option3 = Radiobutton(self.strength_input_frame, text="high", value="high", variable=self.choice, font=("Helvetica", 13), bg="#e5e7ea")
        option1.pack(side=LEFT, padx=(50, 0))
        option2.pack(side=LEFT, padx=(50, 0))
        option3.pack(side=LEFT, padx=(50, 0))

    def create_button_frame(self):
        frame = Frame(self, bg="#e5e7ea", height=100, padx=20, pady=20)
        frame.pack(fill=BOTH)
        return frame

    def show_generate_password_window(self, length, strength, password):
        # Creates a new window to display the generated password
        win = Toplevel(self)
        win.geometry("700x215")
        win.resizable(False, False)
        win.title("Your Generated Password")
        label = Label(win, text=f"GENERATED PASSWORD\nLENGTH: {length}\tSTRENGTH: {strength}", fg="#1d3b64", font=("Helvetica", 16))
        label.pack()
        pass_view = Text(win, height=3, width=70, fg="#1d3b64", bg="#e5e7ea", font=("Helvetica", 13))
        pass_view.insert(END, password)
        pass_view.config(state=DISABLED)
        pass_view.pack()
        Button(win, text="Close", width=13, bd=0, bg="#3c8bdf", fg="#ffffff", font=("Helvetica", 13, "bold"), command=win.destroy).pack(side=RIGHT, padx=(0, 20))
        win.mainloop()

    def create_generate_button(self):
        Button(self.button_frame, text="GENERATE", bg="#235d48", fg="#e1e6e4", borderwidth=0, cursor="hand2", padx=20, pady=5, command=lambda: self.collect_password(self.password_length_entry.get(), self.choice.get())).pack()

    def generate_low_security_password(self, length):
        # Only uses upper and lower case letters
        chars = [chr(c) for c in range(65, 91)] + [chr(c) for c in range(97, 123)]
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_medium_security_password(self, length):
        # Uses letters and numbers, ensuring at least one digit is present
        chars = [chr(c) for c in range(65, 91)] + [chr(c) for c in range(97, 123)] + [chr(c) for c in range(48, 58)]
        password = ''.join(random.choice(chars) for _ in range(length))
        if not re.search(r'\d', password):
            return self.generate_medium_security_password(length) # Regenerate if no number found
        return password

    def generate_high_security_password(self, length):
        # Uses letters, numbers, and symbols, ensuring at least one of each is present
        chars = [chr(c) for c in range(65, 91)] + [chr(c) for c in range(97, 123)] + [chr(c) for c in range(48, 58)] + list('!@#$%^&*')
        password = ''.join(random.choice(chars) for _ in range(length))
        if not re.search(r'\d', password) or not re.search(r'[!@#$%^&*]', password):
            return self.generate_high_security_password(length) # Regenerate if constraints not met
        return password

    def collect_password(self, length, strength):
        try:
            length = int(length)
            if length < 4 or length > 80:
                msg.showwarning(title="WARNING", message="Password length must be between 4 and 80")
                return
                
            password = ""
            if strength == "low":
                password = self.generate_low_security_password(length)
            elif strength == "medium":
                password = self.generate_medium_security_password(length)
            else:
                password = self.generate_high_security_password(length)
                
            self.show_generate_password_window(length, strength, password)
        except:
            msg.showwarning(title="WARNING", message="Invalid password length")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = PasswordGenerator()
    app.run()
