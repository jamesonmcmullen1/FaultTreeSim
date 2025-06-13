#creating the component tree 
class Component:
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        self.failed = False
        self.manual_faulted = False

    def add_dependency(self, component):
        #link this component to another it depends on
        self.dependencies.append(component)

    def inject_fault(self):
        #add fault
        self.manual_faulted = True


    def reset(self):
        #reset faults
        self.manual_faulted = False
        self.failed = False


    def evaluate_failure(self):
        #if manually faulted, this component stays failed regardless of dependencies
        if self.manual_faulted:
            self.failed = True
            return self.failed

        if not self.dependencies:
            self.failed = False  #not manually faulted, no failure
            return self.failed

        self.failed = any(dep.failed for dep in self.dependencies)
        
        return self.failed


    def status(self):
        return "FAILED" if self.failed else "OK"

    def __repr__(self):
        return f"<Component '{self.name}': {self.status()}>"

