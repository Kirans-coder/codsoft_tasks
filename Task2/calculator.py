import tkinter as tk

BG_COLOR = "#f0f4f7"
BTN_COLOR = "#3498db"
BTN_COLOR_OP = "#1abc9c"
BTN_COLOR_CLEAR = "#e74c3c"
TEXT_COLOR = "#2c3e50"
ENTRY_FONT = ("Arial", 20)
BTN_FONT = ("Arial", 16, "bold")

class HybridCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hybrid Calculator")
        self.geometry("350x500")
        self.config(bg=BG_COLOR)
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        self.entry = tk.Entry(self, font=ENTRY_FONT, borderwidth=5, relief="ridge", justify="right")
        self.entry.pack(fill="both", ipadx=8, pady=10, padx=10, ipady=15)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack()

        buttons = [
            ['7','8','9','/'],
            ['4','5','6','*'],
            ['1','2','3','-'],
            ['0','.','=','+'],
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                if char == "=":
                    btn = tk.Button(btn_frame, text=char, width=5, height=2, bg=BTN_COLOR_OP, fg="white",
                                    font=BTN_FONT, command=self.calculate)
                elif char in "+-*/":
                    btn = tk.Button(btn_frame, text=char, width=5, height=2, bg=BTN_COLOR_OP, fg="white",
                                    font=BTN_FONT, command=lambda ch=char: self.press(ch))
                else:
                    btn = tk.Button(btn_frame, text=char, width=5, height=2, bg=BTN_COLOR, fg="white",
                                    font=BTN_FONT, command=lambda ch=char: self.press(ch))
                btn.grid(row=r, column=c, padx=5, pady=5)

        clear_btn = tk.Button(self, text="C", width=20, height=2, bg=BTN_COLOR_CLEAR, fg="white",
                              font=BTN_FONT, command=self.clear)
        clear_btn.pack(pady=10)

    def press(self, char):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current + char)

    def calculate(self):
        try:
            expr = self.entry.get()
            result = str(eval(expr))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
        except:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")

    def clear(self):
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    app = HybridCalculator()
    app.mainloop()
