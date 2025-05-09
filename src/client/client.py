import socket
import pickle
import time

from utils import utils

# Colors
RED = utils.RED
GREEN = utils.GREEN
YELLOW = utils.YELLOW
CYAN = utils.CYAN
RESET = utils.RESET
BOLD = utils.BOLD

PORT = 65432

def game_loop(conn, player1, player2):




    while player1.current_hp > 0 and player2.current_hp > 0:
        print(f"\n{utils.BOLD}              --- New Turn ---{utils.RESET}")
        print(f"{utils.GRAY}{utils.ITALIC}(Opponent){utils.RESET} {utils.render_hp_bar(player1.current_hp, player1.max_hp)} {utils.BOLD}{player1.name}{utils.RESET}")
        print(f"{utils.GRAY}{utils.ITALIC}(You){utils.RESET}      {utils.render_hp_bar(player2.current_hp, player2.max_hp)} {utils.BOLD}{player2.name}{utils.RESET}\n")
        utils.print_each_char(f"{utils.GRAY}{utils.ITALIC}Waiting for opponent to chose a spell...\n{utils.RESET}")
        # Wait for server signal to take turn
        data = conn.recv(4096)

        if data  == b'YOUR_TURN':
            utils.print_each_char(f"{utils.GRAY}{utils.ITALIC}\nYour turn to choose a spell!{utils.RESET}")
            spell = utils.choose_spell(player2)
            conn.sendall(pickle.dumps(spell))

        # Recieve order of attack and chosen spells
        data = conn.recv(4096)
        update = pickle.loads(data)

        # First attack
        print("\n")
        update['firstAttacker'].cast_spell(update['firstSpell'], update['secondAttacker'], False)
        print("\n")
        time.sleep(1)
        # Second attack
        update['secondAttacker'].cast_spell(update['secondSpell'], update['firstAttacker'], False)
        print("\n")
        time.sleep(3)

        # Recieve after combat player data
        data = conn.recv(4096)
        update = pickle.loads(data)

        # Update players
        player1 = update['player1']
        player2 = update['player2']


    # Game over message
    print(f"{utils.GRAY}{utils.ITALIC}(Opponent){utils.RESET} {utils.render_hp_bar(player1.current_hp, player1.max_hp)} {utils.BOLD}{player1.name}{utils.RESET}")
    print(f"{utils.GRAY}{utils.ITALIC}(You){utils.RESET}      {utils.render_hp_bar(player2.current_hp, player2.max_hp)} {utils.BOLD}{player2.name}{utils.RESET}\n")
    if player1.current_hp <= 0 and player2.current_hp <= 0:
        result_msg = f"{utils.YELLOW}It's a draw!{utils.RESET}"
    elif player1.current_hp <= 0:
        result_msg = f"{utils.GREEN}You win!{utils.RESET}"
    else:
        result_msg = f"{utils.RED}You lose!{utils.RESET}"

    utils.print_each_char(result_msg)


def client():

    HOST = input("Enter server IP address: ")  # Example: 192.168.1.5
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    utils.print_each_char(f"{utils.GRAY}{utils.ITALIC}Waiting for opponent to chose a pokemon...\n{utils.RESET}")

    # Receive Pokémon list
    data = client.recv(4096)
    pokemon_list = pickle.loads(data)

    # Receive Player1 Pokémon
    player1 = pickle.loads(client.recv(4096))

    # Pick Pokémon
    player2 = utils.choose_pokemon(pokemon_list)


    client.sendall(pickle.dumps(player2))

    utils.print_each_char(f"{utils.CYAN}Your opponent chose {player1.name}!{utils.RESET}\n\n")
    time.sleep(2)


    # Start game
    game_loop(client, player1, player2)

    client.close()

if __name__ == "__main__":
    client()

