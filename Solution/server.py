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
        self.setup_server()
        self.game = Game()
        self.accept_client_connection()
        self.game_started = False
        self.start_game()
        if self.game_started:
            self.run_game()

    def setup_server(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen()

        print("Server is up and running.")

    def accept_client_connections(self):
        self.first_client_socket, self.first_client_address = self.server_socket.accept()
        print("[+] First client connected.")
        self.first_client_socket.send("Awaiting other client.".encode())
        self.second_client_socket, self.second_client_address = self.server_socket.accept()
        self.first_client_socket.send("Other client connected".encode())
        self.second_client_socket.send("Other client connected".encode())
        print("[+] Clients connected.")

    def receive_first_message(self):
        return self.first_client_socket.recv(1024).decode()

    def receive_and_forward_message(self, sender, receiver):
        while True:
            data = sender.recv(1024).decode()
            if data != "":
                break
            continue
        if data == "EXIT":
            receiver.send("Client exited chat.".encode())
            sender.send("Confirmed".encode())
            print("[+] Chat closed. Shutting Down...")
            sender.close()
            receiver.close()
            exit(0)

        if self.game.check_if_winner("user"):
            self.send_winner_message("user")
            return True

        print("\nReceived: " + data)
        print("Forwarding...")
        receiver.send(data.encode())
        sender.send("Received and Forwarded".encode())

    def one_message_cycle(self):
        Server.receive_and_forward_message(self.first_client_socket, self.second_client_socket)
        Server.receive_and_forward_message(self.second_client_socket, self.first_client_socket)

    # Awaits user sending request to start the game.
    def start_game(self):
        while True:
            request_type = self.first_client_socket.recv(10).decode()
            if request_type == "Start Game":
                self.game_started = True
                self.send_board_status(self.first_client_socket)
                return
            continue

    # Accepts clients connection to server.
    def accept_client_connection(self):
        (self.client_socket, self.client_address) = self.server_socket.accept()
        print("Client connected")

    # Sends user the boards current position.
    def send_board_status(self, socket_to_send):
        socket_to_send.send("Game:".encode())
        message = pickle.dumps(self.game.board)
        socket_to_send.send((str(len(message)).encode()))
        socket_to_send.send(message)

    # Tells user who won.
    def send_winner_message(self, winner):
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
        self.client_socket.send(str(len(message)).encode())
        self.client_socket.send(message)
    @classmethod
    def forward_message(cls, message, receiver):
        print("\nReceived: " + message)
        print("Forwarding...")
        receiver.send(message.encode())

    # Function runs one turn. Player plays first, then server. Each time a player plays, the game checks if someone won.
    def turn(self):
        coordinates = self.accept_client_move(self.first_client_socket)
        message = self.accept_client_chat(self.first_client_socket)
        self.game.add_input(coordinates, "user 1")
        self.forward_message(message, self.second_client_socket)
        if self.game.check_if_winner("user 1"):
            self.send_winner_message("user 1")
            return True

        coordinates = self.accept_client_move(self.second_client_socket)
        message = self.accept_client_chat(self.second_client_socket)
        self.game.add_input(coordinates, "user 2")
        self.forward_message(message, self.first_client_socket)
        if self.game.check_if_winner("user 2"):
            self.send_winner_message("user 2")
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
    def accept_client_move(self, client_socket):
        while True:
            try:
                request_length = int(client_socket.recv(2).decode())
                request_type = client_socket.recv(request_length).decode()
                if request_type[:4] == "Game":
                    return tuple((int(request_type[5]), int(request_type[6])))
                continue
            except ValueError:
                continue

    def accept_client_chat(self, client_socket):
        while True:
            try:
                request_length = int(client_socket.recv(9).decode())
                request_type = client_socket.recv(request_length).decode()
                if request_type[:5] == "Game:":
                    return client_socket.recv(request_type[5:10].decode())
                continue
            except ValueError:
                continue


server = Server(8820)
