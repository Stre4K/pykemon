import socket
import pickle
import utils

# Colors
RED = utils.RED
GREEN = utils.GREEN
YELLOW = utils.YELLOW
CYAN = utils.CYAN
RESET = utils.RESET
BOLD = utils.BOLD

PORT = 65432

def game_loop(conn, player1, player2):
    while True:
        spell = utils.choose_spell(player2)
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
    player2 = utils.choose_pokemon(pokemon_list)


    client.sendall(pickle.dumps(player2))

    player1 = None  # Server player

    # Start game
    game_loop(client, player1, player2)

    client.close()
    print(f"{YELLOW}Game over!{RESET}")

if __name__ == "__main__":
    client()

