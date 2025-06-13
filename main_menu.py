#imports
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from build_instructions import BuildInstructions

class MainMenu:
    def __init__(self, root):
        #build gui
        self.root = root
        self.root.title("Mission Zero")
        self.root.geometry("1440x775")
        self.root.configure(bg="black")
        self.create_widgets()

    def create_widgets(self):
        #add difficulty buttons
        frame = tk.Frame(self.root, bg="black")
        frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(
            frame, 
            text="Choose Your Difficulty", 
            font=("Orbitron", 48), 
            fg="lime", 
            bg="black", 
            justify="center"
        )
        title.pack(pady=40)

        canvas = tk.Canvas(self.root, width=1440, height=750, bg="black", highlightthickness=0)
        canvas.pack()

        #center-aligned X positions
        button_width = 150
        button_spacing = 60
        total_width = 3 * button_width + 2 * button_spacing
        start_x = (1440 - total_width) // 2

        #define button positions
        button_positions = [
            start_x + button_width // 2, #center of first button
            start_x + button_width + button_spacing + button_width // 2, #second
            start_x + 2 * (button_width + button_spacing) + button_width // 2 #third
        ]

        #define buttons
        buttons = [
            {"label": "RECRUIT", "x": button_positions[0], "callback": lambda: self.start_game("easy")},
            {"label": "LIEUTENANT", "x": button_positions[1], "callback": lambda: self.start_game("medium")},
            {"label": "COMMANDER", "x": button_positions[2], "callback": lambda: self.start_game("hard")},
        ]

        for btn in buttons:
            rect = canvas.create_rectangle(
                btn["x"] - button_width // 2, 250,
                btn["x"] + button_width // 2, 310,
                fill="black", outline="lime", width=2
            )
            text = canvas.create_text(
                btn["x"], 280, text=btn["label"], fill="lime", font=("Orbitron", 16)
            )

            #hover/click behavior
            def make_hover_handlers(r=rect):
                return (
                    lambda e: canvas.itemconfig(r, fill="#1a1a1a"),
                    lambda e: canvas.itemconfig(r, fill="black"),
                    lambda e: canvas.itemconfig(r, fill="#333333"),
                    lambda e: canvas.itemconfig(r, fill="#1a1a1a")
                )

            on_enter, on_leave, on_press, on_release = make_hover_handlers()

            for item in (rect, text):
                canvas.tag_bind(item, "<Enter>", on_enter)
                canvas.tag_bind(item, "<Leave>", on_leave)
                canvas.tag_bind(item, "<ButtonPress-1>", on_press)
                canvas.tag_bind(item, "<ButtonRelease-1>", on_release)
                canvas.tag_bind(item, "<ButtonRelease-1>", lambda e, f=btn["callback"]: f())

    def start_game(self, difficulty):
        #destroy the main menu window
        self.root.destroy()

        #launch the build phase GUI for the selected difficulty
        new_root = tk.Tk()
        app = BuildInstructions(new_root, difficulty)
        new_root.mainloop()

#run Main Menu
if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
