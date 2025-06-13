#proper imports
import tkinter as tk
import tkinter.font as tkFont
from fault_tree import FaultTree
from mission_control import MissionControl

class MissionBriefing:
    def __init__(self, root, fault_tree, difficulty):
        #build gui
        self.root = root
        self.root.title("Mission Briefing")
        self.root.geometry("1440x750")
        self.root.configure(bg="black")

        self.fault_tree = fault_tree
        self.difficulty = difficulty

        self.font = tkFont.Font(family="Orbitron", size=28)
        self.title_font = tkFont.Font(family="Orbitron", size=36)

        self.canvas = tk.Canvas(self.root, width=1440, height=750, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.setup_gui()

    def setup_gui(self):
        self.canvas.create_text(
            720, 100,
            text="MISSION BRIEFING",
            font=self.title_font,
            fill="lime"
        )

        message = self.get_briefing_text()
        self.canvas.create_text(
            720, 350,
            text=message,
            font=self.font,
            fill="lime",
            justify="center",
            width=1000
        )

        self.draw_launch_button()

    def draw_launch_button(self):
        #custom button
        x_center = 720
        rect = self.canvas.create_rectangle(x_center - 120, 580, x_center + 120, 640, fill="black", outline="lime", width=2)
        text = self.canvas.create_text(x_center, 610, text="LAUNCH MISSION", fill="lime", font=("Orbitron", 18))

        def on_enter(event): self.canvas.itemconfig(rect, fill="#1a1a1a")
        def on_leave(event): self.canvas.itemconfig(rect, fill="black")
        def on_press(event): self.canvas.itemconfig(rect, fill="#333333")
        def on_release(event):
            self.canvas.itemconfig(rect, fill="#1a1a1a")
            self.launch_mission()

        for item in (rect, text):
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)
            self.canvas.tag_bind(item, "<ButtonPress-1>", on_press)
            self.canvas.tag_bind(item, "<ButtonRelease-1>", on_release)

    def get_briefing_text(self):
        return (
            #instructions
            f"Your spacecraft is prepared for launch as {self.difficulty.lower()}.\n\n"
            "You are now the mission’s chief systems officer.\n"
            "As your spacecraft embarks on its critical journey, components will fail.\n\n"
            "- You will use a fault tree to assess system damage.\n"
            "- You must identify and repair the root cause of each fault.\n"
            "- A single incorrect repair will terminate the mission.\n\n"
            "Remain alert. Launch when ready."
        )

    def launch_mission(self):
        self.root.destroy()
        new_root = tk.Tk()
        MissionControl(new_root, self.fault_tree, self.difficulty)
        new_root.mainloop()
