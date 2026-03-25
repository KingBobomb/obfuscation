class Item:
    def __init__(self, name, description, can_be_taken=True, is_evidence=False, required_location=None):
        self.name = name 
        self.description = description 
        self.can_be_taken = can_be_taken  
        self.is_evidence = is_evidence  
        self.required_location = required_location   
        self.is_barred = False  

    def use(self, current_location):
        # Check if the item requires a specific location to be used 
        if self.required_location and current_location != self.required_location:
            print(f"The {self.name} can't be used here. You need to be in the {self.required_location}.")
            return False
        
        print(f"You used the {self.name}: {self.description}")
        self.apply_effect()
        return True

    def apply_effect(self):
        pass