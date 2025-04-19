from load_spells import load_spells_from_file
from pykemon import Pykemon

# Load all spells from file
all_spells = load_spells_from_file("../docs/spells.txt")

# Create Pykemon
charmander = Pykemon("Charmander", "Fire", defense=25, attack=35)
squirtle = Pykemon("Squirtle", "Water", defense=30, attack=30)
bulbasaur = Pykemon("Bulbasaur", "Grass", defense=35, attack=25)

# Assign spells based on type
for spell in all_spells:
    if spell.spell_type == "Fire":
        charmander.learn_spell(spell)
    elif spell.spell_type == "Water":
        squirtle.learn_spell(spell)
    elif spell.spell_type == "Grass":
        bulbasaur.learn_spell(spell)

# Show initial state
print(charmander)
print(squirtle)
print(bulbasaur)
print("")

# Cast some spells!
charmander.cast_spell(charmander.spells[0], bulbasaur)
bulbasaur.cast_spell(bulbasaur.spells[0], squirtle)
squirtle.cast_spell(squirtle.spells[0], charmander)

# Show updated state
print("")
print(charmander)
print(squirtle)
print(bulbasaur)
