import socket
import random
from game_algorithm import Game
import pickle


class Server:
    def __init__(self, port):
        self.server_socket = None
        self.message = ""
        self.port = port
        self.setup_server()
        self.accept_client_connections()
        self.game = Game()
        self.start_game()
        self.run_game()

    def send_board_status(self, socket_to_send):
        socket_to_send.send("Game:".encode())
        message = pickle.dumps(self.game.board)
        socket_to_send.send((str(len(message)).encode()))
        socket_to_send.send(message)

    def start_game(self):
        while True:
            request_type = self.first_client_socket.recv(10).decode()
            if request_type == "Start Game":
                return
            continue

    def send_winner_message(self, winner):
        self.forward_message(self.message, self.first_client_socket)
        self.first_client_socket.send("Game:".encode())
        message = pickle.dumps("Winner:" + winner)
        self.first_client_socket.send(str(len(message)).encode())
        self.first_client_socket.send(message)

        self.second_client_socket.send("Game:".encode())
        message = pickle.dumps("Winner:" + winner)
        self.second_client_socket.send(str(len(message)).encode())
        self.second_client_socket.send(message)

    # Tells user the game ended in tie.
    def send_tie_message(self):
        message = "Game: Tie"
        self.first_client_socket.send(str(len(message)).encode())
        self.first_client_socket.send(message)

        self.second_client_socket.send(str(len(message)).encode())
        self.second_client_socket.send(message)

    @classmethod
    # Function accepts client message and returns the game coordinates.
    def accept_client_move(cls, client_socket):
        while True:
            try:
                request_length = client_socket.recv(2).decode()
                request_type = client_socket.recv(int(request_length)).decode()
                if request_type[:4] == "Game":
                    return tuple((int(request_type[5]), int(request_type[6])))
                continue
            except ValueError:
                continue

    @classmethod
    def accept_client_chat(cls, client_socket):
        while True:
            try:
                message_length = int(client_socket.recv(2).decode())
                message = client_socket.recv(message_length).decode()
                return message
            except ValueError:
                continue

    def turn(self):
        self.forward_message(self.message, self.first_client_socket)
        self.send_board_status(self.first_client_socket)
        coordinates = self.accept_client_move(self.first_client_socket)
        self.message = self.accept_client_chat(self.first_client_socket)
        self.game.add_input(coordinates, "user 1")
        self.forward_message(self.message, self.second_client_socket)
        if self.game.check_if_winner("user 1"):
            self.send_winner_message("user 1")
            return True

        self.send_board_status(self.second_client_socket)
        coordinates = self.accept_client_move(self.second_client_socket)
        self.message = self.accept_client_chat(self.second_client_socket)
        self.game.add_input(coordinates, "user 2")
        if self.game.check_if_winner("user 2"):
            self.send_winner_message("user 2")
            return True

        if self.game.check_if_tie():
            self.send_tie_message()
            return True
        return False

    @classmethod
    def forward_message(cls, message, receiver):
        print("\nReceived: " + message)
        print("Forwarding...")
        message_length = str(len(message))
        if len(message_length) == 1:
            message_length = "0" + message_length
        receiver.send(message_length.encode())
        receiver.send(message.encode())

    def accept_client_connections(self):
        self.first_client_socket, self.first_client_address = self.server_socket.accept()
        print("[+] First client connected.")
        self.first_client_socket.send("Awaiting other client.".encode())
        self.second_client_socket, self.second_client_address = self.server_socket.accept()
        self.first_client_socket.send("Other client connected".encode())
        self.second_client_socket.send("Other client connected".encode())
        print("[+] Clients connected.")

    def setup_server(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen()

        print("Server is up and running.")

    def run_game(self):
        while True:
            win = self.turn()
            if win:
                break
            continue


server = Server(8820)
