#import gui and transition components. imports for fault tree display 
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from fault_controller import FaultController
from game_over import GameOverScreen
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

class DiagnosticsGUI:
    def __init__(self, root, fault_tree, difficulty):
        #build gui
        self.root = root
        self.root.title("Diagnostics Console")
        self.root.geometry("1440x750")
        self.root.configure(bg="black")
        self.orbitron = tkFont.Font(family="Orbitron", size=36)
        self.setup_gui()

        #build fault tree
        self.fault_tree = fault_tree
        self.controller = FaultController(fault_tree, difficulty)
        self.difficulty = difficulty

        #inject faults
        self.controller.inject_faults()
        self.fault_tree.propagate_all()
        self.refresh_fault_tree()
        self.refresh_component_picker()

    def setup_gui(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="black", borderwidth=0)
        style.configure("TNotebook.Tab", background="black", foreground="lime", font=("Orbitron", 16), padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", "#1a1a1a")])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        #Tab 1: Diagnostics Console, displays fault tree
        diag_tab = tk.Frame(notebook, bg="black")
        notebook.add(diag_tab, text="Diagnostics Console")

        canvas = tk.Canvas(diag_tab, width=1440, height=750, bg="black", highlightthickness=0)
        canvas.pack()

        canvas.create_text(720, 40, text="DIAGNOSTICS CONSOLE", font=("Orbitron", 28), fill="lime")

        self.figure = plt.Figure(figsize=(8, 6), dpi=100, facecolor="black")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("black")
        self.figure.patch.set_facecolor("black")
        self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove extra padding

        self.canvas_graph = FigureCanvasTkAgg(self.figure, master=diag_tab)
        self.canvas_graph.get_tk_widget().place(x=270, y=100)

        #Tab 2: Repair Console with combo box & button to select component to fix 
        repair_tab = tk.Frame(notebook, bg="black")
        notebook.add(repair_tab, text="Repair Console")

        canvas = tk.Canvas(repair_tab, width=1440, height=750, bg="black", highlightthickness=0)
        canvas.pack()

        center_frame = tk.Frame(canvas, bg="black")
        canvas.create_window(720, 550, window=center_frame)

        label = tk.Label(center_frame, text="Select Component to Fix:", font=self.orbitron, fg="lime", bg="black")
        label.pack(pady=(0, 10))

        self.selected_component = tk.StringVar()
        self.component_dropdown = ttk.Combobox(center_frame, textvariable=self.selected_component, state="readonly", font=self.orbitron)
        self.component_dropdown.pack(pady=5)

        style.configure("TCombobox", foreground="black", fieldbackground="black", background="black")

        self.submit_button_canvas = tk.Canvas(center_frame, width=300, height=60, bg="black", highlightthickness=0)
        self.submit_button_canvas.pack(pady=20)
        self.submit_button_rect = self.submit_button_canvas.create_rectangle(0, 0, 300, 60, fill="black", outline="lime", width=2)
        self.submit_button_text = self.submit_button_canvas.create_text(150, 30, text="SUBMIT FIX", fill="lime", font=("Orbitron", 28))
        self.submit_button_canvas.tag_bind(self.submit_button_rect, "<ButtonRelease-1>", lambda e: self.submit_fix())
        self.submit_button_canvas.tag_bind(self.submit_button_text, "<ButtonRelease-1>", lambda e: self.submit_fix())

        self.status_log = tk.Text(center_frame, height=10, width=30, font=self.orbitron, fg="lime", bg="black", wrap="word", borderwidth=0, highlightthickness=0)
        self.status_log.pack(pady=10)

    def refresh_fault_tree(self):
        #create the fault tree display
        self.ax.clear()
        G = nx.DiGraph()

        for comp in self.fault_tree.components.values():
            G.add_node(comp.name, status=comp.status())
            for dep in comp.dependencies:
                G.add_edge(dep.name, comp.name)

        color_map = ["red" if self.fault_tree.components[n].failed else "lime" for n in G.nodes]

        pos = nx.kamada_kawai_layout(G)
        nx.draw(
            G, pos, ax=self.ax,
            with_labels=True,
            node_color=color_map,
            node_size=1200,
            font_size=10,
            font_color="white",
            arrows=True,
            edge_color="white",

        )

        self.ax.set_facecolor("black")
        self.figure.patch.set_facecolor("black")
        self.figure.tight_layout(pad=0)

        self.ax.set_title("SPACECRAFT FAULT TREE", fontsize=12, color="lime")
        self.canvas_graph.draw()

    def refresh_component_picker(self):
        #code for the combo box component picker
        all_components = sorted(self.fault_tree.components.keys())
        self.component_dropdown['values'] = all_components
        if all_components:
            self.component_dropdown.current(0)
            self.selected_component.set(all_components[0])

    def submit_fix(self):
        #fixing fault in specified component and handling success/failure
        choice = self.selected_component.get()
        if not choice:
            return

        result = self.controller.fix_component(choice)

        if result == "wrong":
            self.end_game("fail")
        elif result == "win":
            self.end_game("win")
        elif result == "continue":
            self.log(f"{choice} fixed. New fault(s) detected.")
            self.refresh_fault_tree()
            self.refresh_component_picker()

    def log(self, message):
        self.status_log.config(state="normal")
        self.status_log.delete("1.0", tk.END)
        self.status_log.insert(tk.END, message)
        self.status_log.tag_configure("center", justify='center')
        self.status_log.tag_add("center", "1.0", "end")
        self.status_log.config(state="disabled")

    def end_game(self, result):
        #end the game once failure or complete success
        self.root.destroy()
        new_root = tk.Tk()
        if result == "win":
            GameOverScreen(new_root, result="win")
        else:
            GameOverScreen(new_root, result="fail", reason="Incorrect fix attempt terminated the mission.")
        new_root.mainloop()
