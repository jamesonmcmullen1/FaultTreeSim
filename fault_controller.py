import random
class FaultController:
    def __init__(self, fault_tree, difficulty):
        #create a fault tree
        self.tree = fault_tree
        self.difficulty = difficulty.lower()
        self.remaining_rounds = 0
        self.active_faults = set()
        self.history = []
        self.fault_pool = list(self.tree.components.keys())
        random.shuffle(self.fault_pool)

        #how many rounds of faults injected for each difficulty
        if self.difficulty == "easy":
            self.remaining_rounds = 1
        elif self.difficulty == "medium":
            self.remaining_rounds = 3
        elif self.difficulty == "hard":
            self.remaining_rounds = 3

    def inject_faults(self):
        #inject fault(s) based on difficulty level. updates tree and returns list of newly failed components.
        if self.remaining_rounds <= 0:
            return []

        new_faults = []
        if self.difficulty == "easy":
            new_faults = random.sample(self.fault_pool, 1)

        elif self.difficulty == "medium":
            new_faults = [self.fault_pool.pop()]
        
        elif self.difficulty == "hard":
            #3 faults at once
            new_faults = [self.fault_pool.pop() for _ in range(3) if self.fault_pool]

        for name in new_faults:
            component = self.tree.components[name]
            component.inject_fault()
            self.active_faults.add(name)

        self.tree.propagate_all()
        self.remaining_rounds -= 1
        return new_faults

    def get_root_faults(self):
        #return names of failed components whose dependencies are NOT failed. these are valid root faults the player can attempt to fix.
        root_faults = []
        for name in self.active_faults:
            comp = self.tree.components[name]
            if all(not dep.failed for dep in comp.dependencies):
                root_faults.append(name)
        return root_faults

    def fix_component(self, name):
        #attempt to fix a component by name. returns one of: 'success', 'wrong', 'win', 'continue'
        if name not in self.active_faults:
            return "wrong"  #not a known fault

        if name not in self.get_root_faults():
            return "wrong"  #not a root fault — game over

        #correct: fix it
        comp = self.tree.components[name]
        comp.reset()
        self.active_faults.remove(name)

        self.tree.propagate_all()  #reevaluate after fixing

        if not self.active_faults:
            if self.remaining_rounds > 0:
                self.inject_faults()
                return "continue"
            else:
                return "win"

        return "continue"

    def is_game_over(self):
        return self.remaining_rounds <= 0 and not self.active_faults
