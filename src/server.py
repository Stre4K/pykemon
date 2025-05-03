import socket
import pickle
from load_spells import load_spells_from_file
from pykemon import Pykemon

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

HOST = '0.0.0.0'
PORT = 65432

def choose_pokemon(pokemon_list):
    print(f"{BOLD}Choose your Pokémon:{RESET}")
    for idx, p in enumerate(pokemon_list):
        print(f"{idx + 1}. {p.name} (Type: {p.type})")
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(pokemon_list):
            return pokemon_list[int(choice) - 1]
        else:
            print(f"{YELLOW}Invalid choice. Try again.{RESET}")

def choose_spell(pokemon):
    print(f"\n{BOLD}{pokemon.name}'s Spells:{RESET}")
    for idx, spell in enumerate(pokemon.spells):
        print(f"{idx + 1}. {spell.name} (Type: {spell.spell_type}, Power: {spell.power})")
    while True:
        choice = input("Choose a spell: ")
        if choice.isdigit() and 1 <= int(choice) <= len(pokemon.spells):
            return pokemon.spells[int(choice) - 1]
        else:
            print(f"{YELLOW}Invalid choice. Try again.{RESET}")

def game_loop(conn, player1, player2):
    while player1.current_hp > 0 and player2.current_hp > 0:
        print("\nYour turn to choose a spell!")
        spell1 = choose_spell(player1)  # Player 1 input

        print("\nWaiting for Player 2 to choose a spell...")
        spell2 = pickle.loads(conn.recv(4096))  # Wait for Player 2

        # Now both players have chosen!

        # Determine who is faster
        if player1.speed >= player2.speed:
            first, first_spell, second, second_spell = player1, spell1, player2, spell2
        else:
            first, first_spell, second, second_spell = player2, spell2, player1, spell1

        # First attack
        print(f"\n{first.name} attacks first!")
        first.cast_spell(first_spell, second)
        conn.sendall(pickle.dumps({'attacker': first.name, 'spell': first_spell.name, 'target': second.name, 'target_hp': second.current_hp}))

        # Check if second is knocked out
        if second.current_hp <= 0:
            break

        # Second attack
        print(f"\n{second.name} attacks second!")
        second.cast_spell(second_spell, first)
        conn.sendall(pickle.dumps({'attacker': second.name, 'spell': second_spell.name, 'target': first.name, 'target_hp': first.current_hp}))

    # Game over
    if player1.current_hp <= 0 and player2.current_hp <= 0:
        print(f"{YELLOW}It's a draw!{RESET}")
    elif player2.current_hp <= 0:
        print(f"{GREEN}You win!{RESET}")
    else:
        print(f"{RED}You lose!{RESET}")
    conn.sendall(b'GAMEOVER')


def main():
    # Setup Pokémon
    all_spells = load_spells_from_file("../docs/spells.txt")
    charmander = Pykemon("Charmander", "Fire", defense=25, attack=35, speed=40)
    squirtle = Pykemon("Squirtle", "Water", defense=30, attack=30, speed=30)
    bulbasaur = Pykemon("Bulbasaur", "Grass", defense=35, attack=25, speed=35)
    for spell in all_spells:
        if spell.spell_type == "Fire":
            charmander.learn_spell(spell)
        elif spell.spell_type == "Water":
            squirtle.learn_spell(spell)
        elif spell.spell_type == "Grass":
            bulbasaur.learn_spell(spell)

    pokemon_list = [charmander, squirtle, bulbasaur]

    print(f"{BOLD}Waiting for player 2 to connect...{RESET}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    conn, addr = server.accept()
    print(f"{GREEN}Player 2 connected from {addr}{RESET}")

    # Player 1 picks Pokémon
    player1 = choose_pokemon(pokemon_list)

    # Send Pokémon list to Player 2
    conn.sendall(pickle.dumps(pokemon_list))
    player2 = pickle.loads(conn.recv(4096))

    print(f"{CYAN}Your opponent chose {player2.name}!{RESET}")

    # Reset HP
    player1.reset()
    player2.reset()

    game_loop(conn, player1, player2)

    conn.close()

if __name__ == "__main__":
    main()

