#proper imports
import tkinter as tk
import tkinter.font as tkFont
import threading
import time
from diagnostics_gui import DiagnosticsGUI

class MissionControl:
    def __init__(self, root, fault_tree, difficulty):
        self.root = root
        self.root.title("Mission Control Panel")
        self.root.geometry("1440x750")
        self.root.configure(bg="black")

        self.fault_tree = fault_tree
        self.difficulty = difficulty

        self.status_text = tk.StringVar()
        self.status_text.set("SYSTEM STATUS: All Systems Nominal")
        self.animation_running = True

        self.orbitron = tkFont.Font(family="Orbitron", size=50)
        self.orbitron_button = tkFont.Font(family="Orbitron", size=18)
        self.orbitron_large = tkFont.Font(family="Orbitron", size=36)

        self.canvas = tk.Canvas(self.root, width=1440, height=750, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.setup_gui()

        threading.Thread(target=self.run_timer_and_fault_trigger, daemon=True).start()

    def setup_gui(self):
        #title
        self.canvas.create_text(
            720, 120,
            text="MISSION CONTROL PANEL",
            fill="lime",
            font=self.orbitron_large
        )

        #status text element
        self.status_label = self.canvas.create_text(
            720, 300,
            text=self.status_text.get(),
            fill="lime",
            font=self.orbitron,
            justify="center"
        )

        #diagnostics button (initially hidden)
        self.diagnostics_button_rect = self.canvas.create_rectangle(
            620, 500, 820, 560, fill="", outline="", width=0
        )
        self.diagnostics_button_text = self.canvas.create_text(
            720, 530, text="", font=self.orbitron_button, fill=""
        )

    def run_timer_and_fault_trigger(self):
        #animate status
        for i in range(5):
            time.sleep(1)
            dots = "." * ((i % 3) + 1)
            status = f"SYSTEM STATUS: All Systems Nominal{dots}"
            self.root.after(0, lambda s=status: self.update_status(s, "lime"))

        #trigger fault
        self.animation_running = False
        self.root.after(0, self.show_fault_detected)

    def update_status(self, text, color):
        self.status_text.set(text)
        self.canvas.itemconfig(self.status_label, text=text, fill=color)

    def show_fault_detected(self):
        self.update_status("FAULT DETECTED!", "red")
        self.draw_diagnostics_button()

    def draw_diagnostics_button(self):
        #show green button
        self.canvas.itemconfig(self.diagnostics_button_rect, fill="black", outline="lime", width=2)
        self.canvas.itemconfig(self.diagnostics_button_text, text="RUN DIAGNOSTICS", fill="lime")

        def on_enter(event): self.canvas.itemconfig(self.diagnostics_button_rect, fill="#1a1a1a")
        def on_leave(event): self.canvas.itemconfig(self.diagnostics_button_rect, fill="black")
        def on_press(event): self.canvas.itemconfig(self.diagnostics_button_rect, fill="#333333")
        def on_release(event):
            self.canvas.itemconfig(self.diagnostics_button_rect, fill="#1a1a1a")
            self.launch_diagnostics()

        for item in (self.diagnostics_button_rect, self.diagnostics_button_text):
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)
            self.canvas.tag_bind(item, "<ButtonPress-1>", on_press)
            self.canvas.tag_bind(item, "<ButtonRelease-1>", on_release)

    def launch_diagnostics(self):
        self.root.destroy()
        new_root = tk.Tk()
        DiagnosticsGUI(new_root, self.fault_tree, self.difficulty)
        new_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    MissionControl(root, fault_tree, "easy")
    root.mainloop()
