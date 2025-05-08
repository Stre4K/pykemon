import socket
import pickle
import time

from src.utils import utils

HOST = '0.0.0.0'
PORT = 65432

def game_loop(conn, player1, player2):
    while player1.current_hp > 0 and player2.current_hp > 0:
        print(f"\n{utils.BOLD}              --- New Turn ---{utils.RESET}")
        print(f"{utils.GRAY}{utils.ITALIC}(You){utils.RESET}      {utils.render_hp_bar(player1.current_hp, player1.max_hp)} {utils.BOLD}{player1.name}{utils.RESET}")
        print(f"{utils.GRAY}{utils.ITALIC}(Opponent){utils.RESET} {utils.render_hp_bar(player2.current_hp, player2.max_hp)} {utils.BOLD}{player2.name}{utils.RESET}\n")
        utils.print_each_char(f"{utils.GRAY}{utils.ITALIC}Your turn to choose a spell!{utils.RESET}")

        spell1 = utils.choose_spell(player1)

        # Send signal to client it's their turn
        conn.sendall(b'YOUR_TURN')

        # Receive spell from client
        utils.print_each_char(f"{utils.GRAY}{utils.ITALIC}Waiting for opponent to chose a spell...\n{utils.RESET}")
        spell2 = pickle.loads(conn.recv(4096))

        # Determine turn order
        if player1.speed >= player2.speed:
            first, first_spell, second, second_spell = player1, spell1, player2, spell2
        else:
            first, first_spell, second, second_spell = player2, spell2, player1, spell1

        # Send updated attack order and attacks to client
        conn.sendall(pickle.dumps({
            'firstAttacker': first,
            'secondAttacker': second,
            'firstSpell': first_spell,
            'secondSpell': second_spell
        }))

        # First attack
        first.cast_spell(first_spell, second, True)
        print("\n")
        time.sleep(1)
        # Second attack
        second.cast_spell(second_spell, first, True)
        print("\n")
        time.sleep(3)

        # Send updated states of both players to client
        conn.sendall(pickle.dumps({
            'player1': player1,
            'player2': player2,
        }))

    # Game over message
    conn.sendall(b'GAMEOVER')
    print(f"{utils.GRAY}{utils.ITALIC}(You){utils.RESET}      {utils.render_hp_bar(player1.current_hp, player1.max_hp)} {utils.BOLD}{player1.name}{utils.RESET}")
    print(f"{utils.GRAY}{utils.ITALIC}(Opponent){utils.RESET} {utils.render_hp_bar(player2.current_hp, player2.max_hp)} {utils.BOLD}{player2.name}{utils.RESET}\n")
    if player1.current_hp <= 0 and player2.current_hp <= 0:
        result_msg = f"{utils.YELLOW}{utils.BOLD}It's a draw!{utils.RESET}"
    elif player2.current_hp <= 0:
        result_msg = f"{utils.GREEN}{utils.BOLD}You win!{utils.RESET}"
    else:
        result_msg = f"{utils.RED}{utils.BOLD}You lose!{utils.RESET}"

    utils.print_each_char(result_msg)

def server():
    # Set up Pykemon
    pykemon_list = utils.setup_pykemon()

    print(f"{utils.BOLD}Waiting for player 2 to connect...{utils.RESET}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    conn, addr = server.accept()
    print(f"{utils.GREEN}Player 2 connected from {addr}{utils.RESET}\n")

    # Player 1 picks Pokémon
    player1 = utils.choose_pokemon(pykemon_list)

    # Send Pokémon list to Player 2
    conn.sendall(pickle.dumps(pykemon_list))

    # Send Pokémon to Player 2
    conn.sendall(pickle.dumps(player1))

    # Receive Pokémon from Player 2
    utils.print_each_char(f"{utils.GRAY}{utils.ITALIC}Waiting for opponent to chose a pokemon...\n{utils.RESET}")
    player2 = pickle.loads(conn.recv(4096))

    utils.print_each_char(f"{utils.CYAN}Your opponent chose {player2.name}!{utils.RESET}\n\n")
    time.sleep(2)

    # Reset HP
    player1.reset()
    player2.reset()

    game_loop(conn, player1, player2)

    conn.close()


if __name__ == "__main__":
    server()
