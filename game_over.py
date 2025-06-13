#proper imports 
import tkinter as tk
import tkinter.font as tkFont

class GameOverScreen:
    def __init__(self, root, result="fail", reason=None):
        #build gui
        self.root = root
        self.root.title("Mission Outcome")
        self.root.geometry("1440x750")
        self.root.configure(bg="black")
        self.canvas = tk.Canvas(self.root, width=1440, height=750, bg="black", highlightthickness=0)
        self.canvas.pack()
        orbitron_large = tkFont.Font(family="Orbitron", size=42)
        orbitron_med = tkFont.Font(family="Orbitron", size=18)
        orbitron_small = tkFont.Font(family="Orbitron", size=16)

        #on win
        if result == "win":
            headline = "MISSION SUCCESSFUL"
            subtext = "All faults were identified and repaired.\nThe mission is complete."
            color = "lime"
        #on fail
        else:
            headline = "MISSION FAILED"
            subtext = reason if reason else "Incorrect fix attempt terminated the mission."
            color = "red"

        self.canvas.create_text(720, 300, text=headline, font=orbitron_large, fill=color)
        self.canvas.create_text(720, 400, text=subtext, font=orbitron_med, fill="lime", justify="center")

        #restart Button
        restart_rect = self.canvas.create_rectangle(560, 530, 880, 590, fill="black", outline="lime", width=2)
        restart_text = self.canvas.create_text(720, 560, text="RESTART GAME", font=orbitron_small, fill="gray")

        def restart_game(event=None):
            from welcome_screen import WelcomeScreen
            self.root.destroy()
            new_root = tk.Tk()
            WelcomeScreen(new_root)
            new_root.mainloop()

        self.canvas.tag_bind(restart_rect, "<ButtonRelease-1>", restart_game)
        self.canvas.tag_bind(restart_text, "<ButtonRelease-1>", restart_game)
