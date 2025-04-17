from spell import Spell

def load_spells_from_file(filename):
    spells = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue  # Skip empty lines or comments
            parts = line.split(",")
            if len(parts) != 3:
                print(f"Invalid spell line: {line}")
                continue
            name, power, spell_type = parts
            try:
                power = int(power)
                spell = Spell(name.strip(), power, spell_type.strip())
                spells.append(spell)
            except ValueError:
                print(f"Error parsing spell line: {line}")
    return spells