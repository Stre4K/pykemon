from load_spells import load_spells_from_file
from pykemon import Pykemon  # after you renamed!

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def safe_input(prompt, options):
    while True:
        try:
            choice = input(prompt)
            if not choice.isdigit():
                raise ValueError
            choice = int(choice)
            if 1 <= choice <= options:
                return choice - 1
            else:
                print(f"{YELLOW}Invalid choice. Please select a valid option.{RESET}")
        except ValueError:
            print(f"{YELLOW}Invalid input. Please enter a number.{RESET}")

def choose_pokemon(pokemon_list):
    print(f"{BOLD}Choose your Pokémon:{RESET}")
    for idx, p in enumerate(pokemon_list):
        print(f"{idx + 1}. {p.name} (Type: {p.type})")
    choice = safe_input("Enter the number of your choice: ", len(pokemon_list))
    return pokemon_list[choice]

def choose_spell(pokemon):
    print(f"\n{BOLD}{pokemon.name}'s Spells:{RESET}")
    for idx, spell in enumerate(pokemon.spells):
        print(f"{idx + 1}. {spell.name} (Type: {spell.spell_type}, Power: {spell.power})")
    choice = safe_input("Choose a spell to cast: ", len(pokemon.spells))
    return pokemon.spells[choice]

def battle_round(player1, player2):
    print(f"\n{BOLD}{player1.name} and {player2.name} are choosing their spells...{RESET}")

    spell1 = choose_spell(player1)
    spell2 = choose_spell(player2)

    # Determine attack order based on speed
    if player1.speed > player2.speed:
        first, first_spell, second, second_spell = player1, spell1, player2, spell2
    elif player2.speed > player1.speed:
        first, first_spell, second, second_spell = player2, spell2, player1, spell1
    else:
        # If speed is equal, Player 1 goes first
        first, first_spell, second, second_spell = player1, spell1, player2, spell2

    print(f"\n{CYAN}{first.name} is faster and attacks first!{RESET}")
    first.cast_spell(first_spell, second)

    if second.current_hp > 0:
        second.cast_spell(second_spell, first)

def game_loop(player1, player2):
    while player1.current_hp > 0 and player2.current_hp > 0:
        battle_round(player1, player2)

        # Show updated HP after both moves
        print(f"\n{BOLD}{player1.name} HP: {player1.current_hp}{RESET}")
        print(f"{BOLD}{player2.name} HP: {player2.current_hp}{RESET}")

        # Check for win
        if player1.current_hp <= 0 and player2.current_hp <= 0:
            print(f"\n{YELLOW}Both Pokémon fainted! It's a draw!{RESET}")
            break
        elif player1.current_hp <= 0:
            print(f"\n{GREEN}{player2.name} wins the battle!{RESET}")
            break
        elif player2.current_hp <= 0:
            print(f"\n{GREEN}{player1.name} wins the battle!{RESET}")
            break

def main():
    playing = True

    while playing:
        # Load all spells from file
        all_spells = load_spells_from_file("../docs/spells.txt")

        # Create Pykemon
        charmander = Pykemon("Charmander", "Fire", defense=25, attack=35, speed=40)
        squirtle = Pykemon("Squirtle", "Water", defense=30, attack=30, speed=30)
        bulbasaur = Pykemon("Bulbasaur", "Grass", defense=35, attack=25, speed=35)

        # Assign spells
        for spell in all_spells:
            if spell.spell_type == "Fire":
                charmander.learn_spell(spell)
            elif spell.spell_type == "Water":
                squirtle.learn_spell(spell)
            elif spell.spell_type == "Grass":
                bulbasaur.learn_spell(spell)

        pokemon_list = [charmander, squirtle, bulbasaur]

        # Players pick
        print(f"\n{BOLD}Player 1:{RESET}")
        player1 = choose_pokemon(pokemon_list)
        print(f"\n{BOLD}Player 2:{RESET}")
        player2 = choose_pokemon(pokemon_list)

        # Reset HP
        player1.reset()
        player2.reset()

        # Start game
        game_loop(player1, player2)

        # Play again?
        play_again = input(f"\n{CYAN}Do you want to play again? (y/n): {RESET}").lower()
        if play_again != 'y':
            playing = False
            print(f"\n{YELLOW}Thanks for playing! Goodbye!{RESET}")

if __name__ == "__main__":
    main()

