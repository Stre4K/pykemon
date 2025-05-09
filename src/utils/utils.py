# utils.py
import time
from src.core.pykemon import Pykemon
from src.core.spell import Spell

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GRAY   = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"

def choose_pykemon(pykemon_list):
    print(f"{BOLD}Choose your Pykemon:{RESET}")
    for idx, p in enumerate(pykemon_list):
        print(f"{idx + 1}. {p.name} (Type: {p.type})")
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(pykemon_list):
            return pykemon_list[int(choice) - 1]
        else:
            print(f"{YELLOW}Invalid choice. Try again.{RESET}")

def choose_spell(pykemon):
    print(f"\n{BOLD}{pykemon.name}'s Spells:{RESET}")
    for idx, spell in enumerate(pykemon.spells):
        print(f"{idx + 1}. {spell.name} (Type: {spell.spell_type}, Power: {spell.power})")
    while True:
        choice = input("Choose a spell: ")
        if choice.isdigit() and 1 <= int(choice) <= len(pykemon.spells):
            return pykemon.spells[int(choice) - 1]
        else:
            print(f"{YELLOW}Invalid choice. Try again.{RESET}")

def setup_pykemon():
    all_spells = load_spells_from_file("../docs/spells.txt")
    charmander = Pykemon("Charmander", "Fire", defense=25, attack=90, speed=40, max_hp=50)
    squirtle = Pykemon("Squirtle", "Water", defense=30, attack=80, speed=30, max_hp=55)
    bulbasaur = Pykemon("Bulbasaur", "Grass", defense=35, attack=70, speed=35, max_hp=60)
    for spell in all_spells:
        if spell.spell_type == "Fire":
            charmander.learn_spell(spell)
        elif spell.spell_type == "Water":
            squirtle.learn_spell(spell)
        elif spell.spell_type == "Grass":
            bulbasaur.learn_spell(spell)

    pykemon_list = [charmander, squirtle, bulbasaur]

    return pykemon_list


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

def print_each_char(text):
    for char in text:
        print(char, end="")
        time.sleep(0.04)



def render_hp_bar(current, maximum, length=20):
    ratio = current / maximum
    filled_length = int(length * ratio)
    bar = '█' * filled_length + '-' * (length - filled_length)

    if ratio > 0.5:
        color = GREEN
    elif ratio > 0.2:
        color = YELLOW
    else:
        color = RED

    return f"{color}[{bar}] {current}/{maximum} HP{RESET}"

def show_splash():
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    print(f"""{YELLOW}
██████╗ ██╗   ██╗██╗  ██╗███████╗███╗   ███╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝██║ ██╔╝██╔════╝████╗ ████║██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝ █████╔╝ █████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝  ██╔═██╗ ██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
██║        ██║   ██║  ██╗███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
╚═╝        ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
{CYAN}
              Welcome to the world of Pykémon!
                 Gotta cast 'em all! ⚡
{RESET}""")

