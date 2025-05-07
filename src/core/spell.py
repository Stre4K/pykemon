class Spell:
    def __init__(self, name, power, spell_type, cost=0):
        self.name = name
        self.power = power
        self.spell_type = spell_type
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.spell_type}) - Power: {self.power}, Cost: {self.cost}"

    def __eq__(self, other):
        return (
            isinstance(other, Spell) and
            self.name == other.name and
            self.power == other.power and
            self.spell_type == other.spell_type and
            self.cost == other.cost
        )

    def __hash__(self):
        return hash((self.name, self.power, self.spell_type, self.cost))
