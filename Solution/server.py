import socket
import random
from game_algorithm import Game
import pickle


class ServerPlayer:
    # Runs one server turn. Server randomly picks coordinates and checks if they can be inputed.
    # If they can be, they are entered. If not, the loop runs again.
    @classmethod
    def server_turn(cls, game):
        while True:
            column = random.randint(0, 2)
            row = random.randint(0, 2)
            selection = (row, column)
            if game.check_if_move_able(selection):
                game.add_input(selection, "server")
                break
            continue


class Server:
    def __init__(self, port):
        self.server_socket = None
        self.port = port
        self.client_socket = None
        self.setup_server()
        self.game = Game()
        self.accept_client_connection()
        self.game_started = False
        self.start_game()
        if self.game_started:
            self.run_game()

    # Awaits user sending request to start the game.
    def start_game(self):
        while True:
            request_type = self.client_socket.recv(10).decode()
            if request_type == "Start Game":
                self.game_started = True
                self.send_board_status()
                return
            continue

    # Accepts clients connection to server.
    def accept_client_connection(self):
        (self.client_socket, self.client_address) = self.server_socket.accept()
        print("Client connected")

    # Sends user the boards current position.
    def send_board_status(self):
        self.client_socket.send("Game:".encode())
        message = pickle.dumps(self.game.board)
        self.client_socket.send((str(len(message)).encode()))
        self.client_socket.send(message)

    # Tells user who won.
    def send_winner_message(self, winner):
        self.client_socket.send("Game:".encode())
        message = pickle.dumps("Winner:" + winner)
        self.client_socket.send(str(len(message)).encode())
        self.client_socket.send(message)

    # Tells user the game ended in tie.
    def send_tie_message(self):
        message = "Game: Tie"
        self.client_socket.send(str(len(message)).encode())
        self.client_socket.send(message)

    # Function runs one turn. Player plays first, then server. Each time a player plays, the game checks if someone won.
    def turn(self):
        coordinates = self.accept_client_response()
        self.game.add_input(coordinates, "user")
        if self.game.check_if_winner("user"):
            self.send_winner_message("user")
            return True
        ServerPlayer.server_turn(self.game)
        if self.game.check_if_winner("server"):
            self.send_winner_message("server")
            return True
        if self.game.check_if_tie():
            self.send_tie_message()
            return True
        self.send_board_status()
        return False

    # Functions runs looped turns until someone wins.
    def run_game(self):
        while True:
            win = self.turn()
            if win:
                break
            continue

    # Function sets up server.
    def setup_server(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen()

        print("Server is up and running.")

    # Function accepts client message and returns the game coordinates.
    def accept_client_response(self):
        while True:
            try:
                request_length = int(self.client_socket.recv(2).decode())
                request_type = self.client_socket.recv(request_length).decode()
                if request_type[:4] == "Game":
                    return tuple((int(request_type[5]), int(request_type[6])))
                continue
            except ValueError:
                continue


server = Server(8820)
