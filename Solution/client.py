import socket
import pickle


class Client:
    def __init__(self):
        self.my_socket = socket.socket()
        self.my_socket.connect(("127.0.0.1", 8820))
        self.board = [[], [], []]
        self.start_game()
        while True:
            self.turn()

    def start_game(self):
        self.my_socket.send("Start Game".encode())
        self.receive_message()

    # Sends game move to server.
    def send_game_coordinates(self, coordinates):
        message = "Game:" + str(coordinates)
        self.my_socket.send(message.encode())

    def present_board(self):
        print("  1  2  3")
        for i in range(len(self.board)):
            row = self.board[i]
            completed_row = str(i + 1)
            for element in row:
                if element == "user":
                    completed_row += "  X"
                if element == "server":
                    completed_row += "  O"
                if element == 0:
                    completed_row += "  "
            print(completed_row)

    def get_user_choice(self):
        while True:
            try:
                row = int(input("Row >>"))
                column = int(input("Column >>"))
                return tuple((row, column))
            except ValueError:
                print("Wrong input please try again...")
                continue

    # Awaits server chat response.
    def await_response(self):
        while True:
            data = self.my_socket.recv(5).decode()
            if data != "" and data != "Received and Forwarded":
                return data
            continue

    # Receives chat message
    @classmethod
    def receive_chat_message(cls, data):
        if data == "Client exited chat.":
            print("\n[+] Chat ended by other client.")
            exit(0)

        if data == "Received and Forwarded":
            return
        else:
            print("Friend: " + data)
            return

    # Receives generic message.
    def receive_message(self):
        data = self.await_response()
        if data == "Game:":
            self.receive_game_directions()
        if data[:4] == "Chat:":
            Client.receive_chat_message(data)

    # Receives updated game position.
    def receive_game_directions(self):
        message_length = self.my_socket.recv(2).decode()
        data = pickle.loads(self.my_socket.recv(int(message_length)))
        if type(data) == str:
            if data == "Tie":
                return "Tie"
            if data[:6] == "Winner":
                return data[6:]
        else:
            self.board = data
            return "No Winner"

    def turn(self):
        self.present_board()
        coordinates = self.get_user_choice()
        self.send_game_coordinates(coordinates)
        winner = self.receive_message()
        if winner != "No Winner":
            print(winner)
            exit()


client = Client()
