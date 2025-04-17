from spell import Spell

# Simple elemental advantage system
ELEMENTAL_EFFECTIVENESS = {
    ("Fire", "Grass"): 2.0,
    ("Water", "Fire"): 2.0,
    ("Grass", "Water"): 2.0,
    ("Fire", "Water"): 0.5,
    ("Water", "Grass"): 0.5,
    ("Grass", "Fire"): 0.5,
}

class Pykemon:
    def __init__(self, name, pykemon_type, level=1, max_hp=50, attack=100, defense=20, speed=5):
        self.name = name
        self.type = pykemon_type # 3 types available, Fire, Water, Grass
        self.level = level
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack # 100 attack results in a 1.0 multiplier of spell damage
        self.defense = defense # Number between 0 - 100 where 100 is 100% dmg reduction
        self.speed = speed
        self.experience = 0
        self.spells = []

    def take_damage(self, spell, attacker):
        # Determine elemental multiplier
        elemental_multiplier = ELEMENTAL_EFFECTIVENESS.get((spell.spell_type, self.type), 1.0)

        # Apply pykemon attack multiplier, elemental multiplier and defense scaling
        base_damage = spell.power * (attacker.attack / 100)
        raw_damage = base_damage * elemental_multiplier
        reduced_damage = raw_damage * (1 - self.defense / 100)
        damage = max(0, int(reduced_damage))

        self.current_hp = max(0, self.current_hp - damage)

        print(f"{self.name} took {damage} damage from {spell.name}!")

        if elemental_multiplier > 1:
            print("It's super effective!")
        elif elemental_multiplier < 1:
            print("It's not very effective...")

    def is_fainted(self):
        return self.current_hp <= 0

    def attack_other(self, other):
        print(f"{self.name} attacks {other.name}!")
        other.take_damage(self.attack)

    def heal(self):
        self.current_hp = self.max_hp
        print(f"{self.name} has been healed to full HP!")

    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gained {amount} XP!")
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.attack += 2
        self.defense += 2
        self.speed += 1
        self.experience = 0
        self.current_hp = self.max_hp
        print(f"{self.name} leveled up to level {self.level}!")

    def learn_spell(self, spell):
        self.spells.append(spell)
        print(f"{self.name} learned {spell.name}!")

    def cast_spell(self, spell, other):
        if spell not in self.spells:
            print(f"{self.name} doesn't know {spell.name}!")
            return

        print(f"{self.name} casts {spell.name} on {other.name}!")

        multiplier = ELEMENTAL_EFFECTIVENESS.get((spell.spell_type, other.type), 1.0)

        if multiplier > 1:
            print("It's super effective!")
        elif multiplier < 1:
            print("It's not very effective...")

        other.take_damage(spell, other)

    def __str__(self):
        return f"{self.name} (Lv. {self.level}, Type: {self.type}) - HP: {self.current_hp}/{self.max_hp}"
