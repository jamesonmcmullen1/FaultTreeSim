#proper imports
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from main_menu import MainMenu

class WelcomeScreen:
    def __init__(self, root):
        #build gui
        self.root = root
        self.root.title("Mission Zero")
        self.root.geometry("1440x750")
        self.root.configure(bg="black")

        self.setup_gui()

    def setup_gui(self):
        frame = tk.Frame(self.root, bg="black")
        frame.pack(expand=True)

        title = tk.Label(
            frame,
            text="Welcome to the Spacecraft Fault Tree Simulator:\nMission Zero",
            font=("Orbitron", 48),
            fg="lime",
            bg="black",
            justify="center"
        )
        title.pack(pady=40)

        canvas = tk.Canvas(self.root, width=750, height=750, bg="black", highlightthickness=0)
        canvas.pack()

        #draw the custom button
        button_rect = canvas.create_rectangle(275, 200, 475, 260, fill="black", outline="lime", width=2)
        button_text = canvas.create_text(375, 230, text="S T A R T", fill="lime", font=("Orbitron", 18))

        #hover/click behavior
        def on_enter(event):
            canvas.itemconfig(button_rect, fill="#1a1a1a")

        def on_leave(event):
            canvas.itemconfig(button_rect, fill="black")

        def on_press(event):
            canvas.itemconfig(button_rect, fill="#333333")

        def on_release(event):
            canvas.itemconfig(button_rect, fill="#1a1a1a")
            self.go_to_difficulty()

        #bind events to the rectangle and text
        for item in (button_rect, button_text):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<ButtonPress-1>", on_press)
            canvas.tag_bind(item, "<ButtonRelease-1>", on_release)

    def go_to_difficulty(self):
        self.root.destroy()
        new_root = tk.Tk()
        MainMenu(new_root)
        new_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    WelcomeScreen(root)
    root.mainloop()
