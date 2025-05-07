import socket
import pickle
from utils import utils

HOST = '0.0.0.0'
PORT = 65432

def game_loop(conn, player1, player2):
    while player1.current_hp > 0 and player2.current_hp > 0:
        print(f"\n{utils.BOLD}--- New Turn ---{utils.RESET}")
        print(f"{player1.name}: {utils.render_hp_bar(player1.current_hp, player1.max_hp)}")
        print(f"{player2.name}: {utils.render_hp_bar(player2.current_hp, player2.max_hp)}\n")

        print("Your turn to choose a spell!")
        spell1 = utils.choose_spell(player1)

        # Send signal to client it's their turn
        conn.sendall(b'YOUR_TURN')

        # Receive spell from client
        print("\nWaiting for Player 2 to choose a spell...")
        spell2 = pickle.loads(conn.recv(4096))

        # Determine turn order
        if player1.speed >= player2.speed:
            first, first_spell, second, second_spell = player1, spell1, player2, spell2
        else:
            first, first_spell, second, second_spell = player2, spell2, player1, spell1

        # First attack
        print(f"\n{first.name} attacks first!")
        first.cast_spell(first_spell, second)

        if second.current_hp <= 0:
            break

        # Second attack
        print(f"\n{second.name} attacks second!")
        second.cast_spell(second_spell, first)

        # Send updated states of both players to client
        conn.sendall(pickle.dumps({
            'attacks': [
                {'attacker': first.name, 'spell': first_spell.name, 'target': second.name, 'target_hp': second.current_hp},
                {'attacker': second.name, 'spell': second_spell.name, 'target': first.name, 'target_hp': first.current_hp}
            ],
            'player1': player1,
            'player2': player2
        }))

    # Game over message
    if player1.current_hp <= 0 and player2.current_hp <= 0:
        result_msg = f"{utils.YELLOW}It's a draw!{utils.RESET}"
    elif player2.current_hp <= 0:
        result_msg = f"{utils.GREEN}You win!{utils.RESET}"
    else:
        result_msg = f"{utils.RED}You lose!{utils.RESET}"

    print(result_msg)
    conn.sendall(b'GAMEOVER')

def server():
    # Set up Pykemon
    pykemon_list = utils.setup_pykemon()

    print(f"{utils.BOLD}Waiting for player 2 to connect...{utils.RESET}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    conn, addr = server.accept()
    print(f"{utils.GREEN}Player 2 connected from {addr}{utils.RESET}")

    # Player 1 picks Pokémon
    player1 = utils.choose_pokemon(pykemon_list)

    # Send Pokémon list to Player 2
    conn.sendall(pickle.dumps(pykemon_list))

    # Send Pokémon to Player 2
    conn.sendall(pickle.dumps(player1))

    # Receive Pokémon from Player 2
    player2 = pickle.loads(conn.recv(4096))

    print(f"{utils.CYAN}Your opponent chose {player2.name}!{utils.RESET}")
    print(player2.spells)

    # Reset HP
    player1.reset()
    player2.reset()

    game_loop(conn, player1, player2)

    conn.close()


if __name__ == "__main__":
    server()
