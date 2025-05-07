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
    while True:
        spell = choose_spell(player2)
        conn.sendall(pickle.dumps(spell))

        data = conn.recv(4096)
        if data == b'GAMEOVER':
            break
        update = pickle.loads(data)
        print(f"{CYAN}{update['attacker']} used {update['spell']} on {update['target']}! {update['target']} HP is now {update['target_hp']}.{RESET}")

def client():

    HOST = input("Enter server IP address: ")  # Example: 192.168.1.5
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Receive Pokémon list
    data = client.recv(4096)
    pokemon_list = pickle.loads(data)

    # Pick Pokémon
    player2 = choose_pokemon(pokemon_list)
    #all_spells = load_spells_from_file("../docs/spells.txt")
    #for spell in all_spells:
    #    if spell.spell_type == player1.type:
    #        player1.learn_spell(spell)


    client.sendall(pickle.dumps(player2))

    player1 = None  # Server player

    # Start game
    game_loop(client, player1, player2)

    client.close()
    print(f"{YELLOW}Game over!{RESET}")

if __name__ == "__main__":
    client()

