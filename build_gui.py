#import gui and attributes, blueprints, fault tree, mission briefing, game over, and image handleing
import tkinter as tk
from tkinter import ttk
from blueprint_loader import load_blueprint
from fault_tree import FaultTree
from mission_briefing import MissionBriefing
from game_over import GameOverScreen
from PIL import Image, ImageTk


class BuildGUI:
    def __init__(self, root, difficulty):
        #building the gui
        self.root = root
        self.difficulty = difficulty
        self.root.title("Spacecraft Build - " + difficulty.title())
        self.root.geometry("1430x750")
        self.root.configure(bg="black")
        self.mistake_count = 0
        self.blueprint = load_blueprint(difficulty)
        self.fault_tree = FaultTree()
        self.added_components = set()
        self.preload_roots()
        self.setup_gui()

    def preload_roots(self):
        #preload the components for top dependency
        preload_map = {
            "easy": ["Battery"],
            "medium": ["Battery", "Solar Panel"],
            "hard": ["Space Craft Structure"]
        }
        roots = preload_map.get(self.difficulty, [])
        for root in roots:
            self.fault_tree.add_component(root)
            self.added_components.add(root)

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="black", borderwidth=0)
        style.configure("TNotebook.Tab", background="black", foreground="lime", font=("Orbitron", 16), padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", "#1a1a1a")])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        #Tab 1: Blueprint image based om difficulty
        blueprint_tab = tk.Frame(notebook, bg="black")
        notebook.add(blueprint_tab, text="Blueprint")

        try:
            blueprint_path = f"assets/blueprints/{self.difficulty.lower()}.png"
            image = Image.open(blueprint_path)

            max_height = 700
            w, h = image.size
            scale_factor = max_height / h
            new_width = int(w * scale_factor)
            new_height = int(h * scale_factor)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.blueprint_image = ImageTk.PhotoImage(image)

            canvas = tk.Canvas(blueprint_tab, bg="black", width=1430, height=750, highlightthickness=0)
            canvas.pack()
            canvas.create_image(715, 375, image=self.blueprint_image)
        except Exception as e:
            tk.Label(
                blueprint_tab,
                text=f"Failed to load blueprint: {e}",
                fg="lime",
                bg="black",
                font=("Orbitron", 16)
            ).pack(pady=20)

        #Tab 2: Builder. combo selection for component. all added components displayed as checkboxes to select combo box selection's dependencies
        #button to add component handling different mistakes or success. complete build button functional once build is complete
        builder_tab = tk.Frame(notebook, bg="black")
        notebook.add(builder_tab, text="Build Spacecraft")

        canvas = tk.Canvas(builder_tab, width=1430, height=750, bg="black", highlightthickness=0)
        canvas.pack()

        center_frame = tk.Frame(canvas, bg="black")
        canvas.create_window(715, 375, window=center_frame)

        tk.Label(center_frame, text="Select Component:", font=("Orbitron", 20), fg="lime", bg="black").pack(pady=(20, 0))

        self.component_var = tk.StringVar()
        self.component_dropdown = ttk.Combobox(center_frame, textvariable=self.component_var, state="readonly", font=("Orbitron", 18))
        self.component_dropdown.pack(pady=10)
        self.component_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_dependency_checkboxes())

        tk.Label(center_frame, text="Select Dependencies:", font=("Orbitron", 20), fg="lime", bg="black").pack(pady=(20, 0))

        self.dependencies_frame = tk.Frame(center_frame, bg="black")
        self.dependencies_frame.pack(pady=10)

        self.add_button_canvas = tk.Canvas(center_frame, width=250, height=60, bg="black", highlightthickness=0)
        self.add_button_canvas.pack(pady=10)
        self.add_button_rect = self.add_button_canvas.create_rectangle(0, 0, 250, 60, fill="black", outline="lime", width=2)
        self.add_button_text = self.add_button_canvas.create_text(125, 30, text="ADD COMPONENT", fill="lime", font=("Orbitron", 18))
        self.add_button_canvas.tag_bind(self.add_button_rect, "<ButtonRelease-1>", lambda e: self.handle_add_component())
        self.add_button_canvas.tag_bind(self.add_button_text, "<ButtonRelease-1>", lambda e: self.handle_add_component())

        self.status_log = tk.Text(center_frame, height=2, width=60, font=("Orbitron", 20), fg="lime", bg="black", insertbackground="lime", borderwidth=0, highlightthickness=0)
        self.status_log.pack(pady=10)
        self.status_log.config(state="disabled")

        self.complete_button_canvas = tk.Canvas(center_frame, width=450, height=60, bg="black", highlightthickness=0)
        self.complete_button_canvas.pack(pady=20)
        self.complete_button_rect = self.complete_button_canvas.create_rectangle(0, 0, 450, 60, fill="black", outline="lime", width=2)
        self.complete_button_text = self.complete_button_canvas.create_text(225, 30, text="COMPLETE BUILD AND LAUNCH MISSION", fill="lime", font=("Orbitron", 18))
        self.complete_button_canvas.tag_bind(self.complete_button_rect, "<ButtonRelease-1>", lambda e: self.handle_complete_build() if self.complete_button_canvas.itemcget(self.complete_button_rect, 'state') != 'disabled' else None)
        self.complete_button_canvas.tag_bind(self.complete_button_text, "<ButtonRelease-1>", lambda e: self.handle_complete_build() if self.complete_button_canvas.itemcget(self.complete_button_rect, 'state') != 'disabled' else None)

        self.refresh_component_dropdown()

    def refresh_component_dropdown(self):
        #refresh the components in combo box to all components not added yet
        available = [c for c in self.blueprint if c not in self.added_components]
        self.component_dropdown['values'] = ["Select Component"] + available
        self.component_var.set("Select Component")
        self.component_dropdown.current(0)
        self.refresh_dependency_checkboxes()

    def refresh_dependency_checkboxes(self):
        #refresh checkboxes to all components added
        for widget in self.dependencies_frame.winfo_children():
            widget.destroy()

        current = self.component_var.get()
        if not current or current == "Select Component":
            return

        options = sorted(list(self.added_components))
        self.dependency_vars = {}
        columns = 3

        for i, comp in enumerate(options):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.dependencies_frame, text=comp, variable=var)
            chk.grid(row=i // columns, column=i % columns, padx=20, pady=10, sticky='w')
            self.dependency_vars[comp] = var

    def handle_add_component(self):
        #add component handling no input, dependencies for component missing, incorrect dependencies selected, successful add, and completed build
        component = self.component_var.get()

        if not component or component in self.added_components or component == "Select Component":
            self.handle_mistake("Invalid component.")
            return

        expected_deps = set(self.blueprint[component])
        if not expected_deps.issubset(self.added_components):
            missing = expected_deps - self.added_components
            self.handle_mistake(f"Missing dependencies: {', '.join(missing)}")
            return

        selected_deps = set(comp for comp, var in self.dependency_vars.items() if var.get())
        if selected_deps != expected_deps:
            self.handle_mistake(f"Incorrect dependencies for {component}")
            return

        self.fault_tree.add_component(component)
        for dep in selected_deps:
            self.fault_tree.add_dependency(component, dep)
        self.added_components.add(component)

        self.log(f"{component} successfully added.")
        self.refresh_component_dropdown()

        if len(self.added_components) == len(self.blueprint):
            self.log("Build complete! Craft ready for launch.")
            self.complete_button_canvas.itemconfig(self.complete_button_rect, state='normal')
            self.complete_button_canvas.itemconfig(self.complete_button_text, state='normal')

    def log(self, message):
        #display status message from add component button selection
        self.status_log.config(state="normal")
        self.status_log.delete("1.0", tk.END)
        self.status_log.insert(tk.END, message)
        self.status_log.tag_configure("center", justify='center')
        self.status_log.tag_add("center", "1.0", "end")
        self.status_log.config(state="disabled")

    def handle_complete_build(self):
        #complete build to continue game
        self.root.destroy()
        new_root = tk.Tk()
        MissionBriefing(new_root, self.fault_tree, self.difficulty)
        new_root.mainloop()

    def handle_mistake(self, message):
        #gamer gets three mistakes before failure
        self.mistake_count += 1
        self.log(f"{message}\n(Strike {self.mistake_count}/3)")

        if self.mistake_count >= 3:
            self.end_build_failure()

    def end_build_failure(self):
        #on failure end game
        self.root.destroy()
        new_root = tk.Tk()
        GameOverScreen(new_root, reason="Build Failure: Too many mistakes")
        new_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = BuildGUI(root, difficulty="easy")
    root.mainloop()
