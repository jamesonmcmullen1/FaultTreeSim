#proper imports
from component import Component
from rich.tree import Tree
from rich import print

class FaultTree:
    def __init__(self):
        self.components = {}

    def add_component(self, name):
        #add a new component to the system
        if name not in self.components:
            self.components[name] = Component(name)
        return self.components[name]

    def add_dependency(self, component_name, dependency_name):
        #link two components by name
        comp = self.components.get(component_name)
        dep = self.components.get(dependency_name)

        if comp and dep:
            comp.add_dependency(dep)

    def inject_fault(self, name):
        #manually inject a fault into a component
        if name in self.components:
            self.components[name].inject_fault()

    def reset_all(self):
        #reset all component failure states
        for comp in self.components.values():
            comp.reset()

    def propagate_all(self):
        visited = set()

        def dfs(component):
            if component.name in visited:
                return
            visited.add(component.name)
            for dep in component.dependencies:
                dfs(dep)
            component.evaluate_failure()

        for comp in self.components.values():
            dfs(comp)



    def generate_fault_tree(self):
        #create a rich.Tree starting from virtual root node and include all independent components
        from rich.tree import Tree

        #find top-level components (not depended on by any others)
        all_deps = {dep.name for comp in self.components.values() for dep in comp.dependencies}
        roots = [comp for name, comp in self.components.items() if name not in all_deps]

        tree = Tree("[bold cyan]System Root[/bold cyan]")

        for root in roots:
            root_branch = tree.add(f"[bold]{root.name}[/bold] - {root.status()}")
            self._build_tree(root, root_branch)

        return tree


    def _build_tree(self, component, tree_node):
        #recursive helper to add child nodes to tree
        for dep in component.dependencies:
            branch = tree_node.add(f"[bold]{dep.name}[/bold] - {dep.status()}")
            self._build_tree(dep, branch)

    def show_fault_tree(self, root_name):
        #print the full fault tree from a given root component
        tree = self.generate_fault_tree(root_name)
        if tree:
            print(tree)

