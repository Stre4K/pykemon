# main.py
from server.server import server
from client.client import client
from utils.utils import show_splash

def main():
    show_splash()

    print("Welcome to Pykemon Battle!")
    print("1. Host Game (Server)")
    print("2. Join Game (Client)")

    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        server()
    elif choice == "2":
        client()
    else:
        print("Invalid choice. Please restart the game.")

if __name__ == "__main__":
    main()

