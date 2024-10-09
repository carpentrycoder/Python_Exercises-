# Knowledge base of facts and rules
class ForwardChaining:
    def __init__(self):
        # Initial facts
        self.facts = {
            "number_is_even": False,
            "number_is_greater_than_5": False,
            "number_is_greater_than_10": False
        }
        
        # Rules to derive new facts
        self.rules = [
            {"conditions": ["number_is_even", "number_is_greater_than_5"], 
             "conclusion": "number_is_greater_than_10"}
        ]
    
    def add_fact(self, fact):
        """Add a new fact to the knowledge base"""
        if fact in self.facts:
            self.facts[fact] = True

    def apply_rules(self):
        """Apply rules to infer new facts"""
        new_facts_inferred = True
        
        # Apply rules until no new facts are derived
        while new_facts_inferred:
            new_facts_inferred = False
            for rule in self.rules:
                conditions_met = all([self.facts[cond] for cond in rule["conditions"]])
                if conditions_met and not self.facts[rule["conclusion"]]:
                    self.facts[rule["conclusion"]] = True
                    new_facts_inferred = True
                    print(f"New fact inferred: {rule['conclusion']}")

    def display_facts(self):
        """Display current facts"""
        print("Current Facts:")
        for fact, is_true in self.facts.items():
            print(f"{fact}: {is_true}")


# Main function
def main():
    # Initialize forward chaining system
    fc = ForwardChaining()

    # Add some initial facts
    number = 8  # You can change the number here to test different scenarios
    if number % 2 == 0:
        fc.add_fact("number_is_even")
    if number > 5:
        fc.add_fact("number_is_greater_than_5")

    # Display initial facts
    print("Initial facts based on the number", number)
    fc.display_facts()

    # Apply rules to infer new facts
    fc.apply_rules()

    # Display final facts
    print("\nFinal facts after applying rules:")
    fc.display_facts()

# Run the program
if __name__ == "__main__":
    main()
