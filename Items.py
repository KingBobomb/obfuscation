class Item:
    def __init__(self, name, description, location,
                 can_be_taken=True, evidence=False, required_location=None):
        self.name = name
        self.description = description
        self.location = location
        self.can_be_taken = can_be_taken
        self.evidence = evidence
        self.required_location = required_location
        self.is_barred = False

    def get_name(self):
        return self.name

    def is_evidence(self):
        return self.evidence
    
    def get_location(self):
        return self.location

    def use(self, current_location):
        # Check if the item requires a specific location to be used
        if self.required_location and current_location != self.required_location:
            print(
                f"The {self.name} can't be used here. "
                f"You need to be in the {self.required_location}."
            )
            return False

        print(f"You used the {self.name}: {self.description}")
        self.apply_effect()
        return True

    def apply_effect(self):
        pass
