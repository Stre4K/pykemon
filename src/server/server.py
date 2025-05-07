import socket
import pickle
from utils import utils

HOST = '0.0.0.0'
PORT = 65432

def game_loop(conn, player1, player2):
    while player1.current_hp > 0 and player2.current_hp > 0:
        print("\nYour turn to choose a spell!")
        spell1 = utils.choose_spell(player1)  # Player 1 input

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
        print(f"{utils.YELLOW}It's a draw!{utils.RESET}")
    elif player2.current_hp <= 0:
        print(f"{utils.GREEN}You win!{utils.RESET}")
    else:
        print(f"{utils.RED}You lose!{utils.RESET}")
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
    player2 = pickle.loads(conn.recv(4096))

    #for spell in all_spells:
    #    if spell.spell_type == player2.type:
    #        player2.learn_spell(spell)

    print(f"{utils.CYAN}Your opponent chose {player2.name}!{utils.RESET}")
    print(player2.spells)

    # Reset HP
    player1.reset()
    player2.reset()

    game_loop(conn, player1, player2)

    conn.close()

if __name__ == "__main__":
    server()

