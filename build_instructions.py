#proper imports for gui and transition
import tkinter as tk
import tkinter.font as tkFont
from build_gui import BuildGUI

class BuildInstructions:
    def __init__(self, root, difficulty):
        #gui build
        self.root = root
        self.difficulty = difficulty
        self.root.title("Build Instructions")
        self.root.configure(bg="black")
        self.root.geometry("1440x750")
        self.orbitron = tkFont.Font(family="Orbitron", size=16)
        self.canvas = tk.Canvas(self.root, width=1440, height=750, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.display_instructions()
        self.create_start_button()

    def display_instructions(self):
        #instructions for the building phase 
        instructions = (
            "BUILD PHASE INSTRUCTIONS\n\n"
            "- Use the blueprint to identify all components.\n"
            "- You must add dependencies before the component that depends on them.\n"
            "- For each component, select the correct dependencies.\n"
            "- You have 3 mistakes before the Space Craft becomes too unstable.\n"
            "- Once all components are correctly added, complete the build to continue."
        )

        self.canvas.create_text(
            720, 225,
            text=instructions,
            fill="lime",
            font=("Orbitron", 32),
            justify="center",
            width=1000
        )

    def create_start_button(self):
        #custom button to continue game
        x_center = 720
        rect = self.canvas.create_rectangle(x_center - 100, 500, x_center + 100, 560, fill="black", outline="lime", width=2)
        text = self.canvas.create_text(x_center, 530, text="BEGIN BUILD", fill="lime", font=("Orbitron", 18))

        def on_enter(event): self.canvas.itemconfig(rect, fill="#1a1a1a")
        def on_leave(event): self.canvas.itemconfig(rect, fill="black")
        def on_press(event): self.canvas.itemconfig(rect, fill="#333333")
        def on_release(event):
            self.canvas.itemconfig(rect, fill="#1a1a1a")
            self.root.destroy()
            new_root = tk.Tk()
            BuildGUI(new_root, self.difficulty)
            new_root.mainloop()

        for item in (rect, text):
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)
            self.canvas.tag_bind(item, "<ButtonPress-1>", on_press)
            self.canvas.tag_bind(item, "<ButtonRelease-1>", on_release)

