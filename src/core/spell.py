class Spell:
    def __init__(self, name, power, spell_type, cost=0):
        self.name = name
        self.power = power
        self.spell_type = spell_type
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.spell_type}) - Power: {self.power}, Cost: {self.cost}"
