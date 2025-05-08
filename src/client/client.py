import socket
import pickle
from src.utils import utils

# Colors
RED = utils.RED
GREEN = utils.GREEN
YELLOW = utils.YELLOW
CYAN = utils.CYAN
RESET = utils.RESET
BOLD = utils.BOLD

PORT = 65432

def game_loop(conn, player1, player2):

    print(f"\n{utils.BOLD}--- New Turn ---{utils.RESET}")
    print(f"{player1.name}: {utils.render_hp_bar(player1.current_hp, player1.max_hp)}")
    print(f"{player2.name}: {utils.render_hp_bar(player2.current_hp, player2.max_hp)}\n")


    while True:
        # Wait for server signal to take turn
        data = conn.recv(4096)

        if data == b'GAMEOVER':
            break
        elif data == b'YOUR_TURN':
            spell = utils.choose_spell(player2)
            conn.sendall(pickle.dumps(spell))

        # First attack result
        data = conn.recv(4096)
        if data == b'GAMEOVER':
            break

        update = pickle.loads(data)

        # Handle both attacks
        for attack in update['attacks']:
            print(f"{CYAN}{attack['attacker']} used {attack['spell']} on {attack['target']}! {attack['target']} HP is now {attack['target_hp']}.{RESET}")

        # Update players
        player1 = update['player1']
        player2 = update['player2']

        print(f"\n{utils.BOLD}--- New Turn ---{utils.RESET}")
        print(f"{player1.name}: {utils.render_hp_bar(player1.current_hp, player1.max_hp)}")
        print(f"{player2.name}: {utils.render_hp_bar(player2.current_hp, player2.max_hp)}\n")



    print(f"\n{utils.YELLOW}Game over!{utils.RESET}")


def client():

    HOST = input("Enter server IP address: ")  # Example: 192.168.1.5
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Receive Pokémon list
    data = client.recv(4096)
    pokemon_list = pickle.loads(data)

    # Receive Player1 Pokémon
    player1 = pickle.loads(client.recv(4096))

    # Pick Pokémon
    player2 = utils.choose_pokemon(pokemon_list)


    client.sendall(pickle.dumps(player2))


    # Start game
    game_loop(client, player1, player2)

    client.close()
    print(f"{YELLOW}Game over!{RESET}")

if __name__ == "__main__":
    client()

