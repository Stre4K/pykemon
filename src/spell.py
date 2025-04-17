class Spell:
    def __init__(self, name, power, spell_type):
        self.name = name
        self.power = power
        self.spell_type = spell_type

    def __str__(self):
        return f"{self.name} ({self.spell_type}) - Power: {self.power}, Cost: {self.cost}"
