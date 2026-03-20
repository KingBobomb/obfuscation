class Item:
    def __init__(self, name, evidence=False):
        self.name = name
        self.evidence = evidence
    
    def use(self):
        print(f"You used the item {self.name}.")