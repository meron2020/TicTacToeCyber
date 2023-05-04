import pickle
import socket


class Client:
    def __init__(self):
        self.my_socket = socket.socket()
        self.my_socket.connect(("127.0.0.1", 8820))
        self.board = [[], [], []]
        self.comm_option = None
        self.first = False
        self.initialize_communications()
        while True:
            self.turn()
            continue

    def await_response(self):
        while True:
            data = self.my_socket.recv(1024).decode()
            if data != "" and data != "Received and Forwarded":
                return data
            continue

    # Sends game move to server.
    def send_game_coordinates(self, coordinates):
        message = "Game:" + coordinates
        self.my_socket.send(str(len(message)).encode())
        self.my_socket.send(message.encode())

    def present_board(self):
        print("\n   1  2  3")
        for i in range(len(self.board)):
            row = self.board[i]
            completed_row = str(i + 1) + " "
            for element in row:
                if element == "user 1":
                    completed_row += " X "
                if element == "user 2":
                    completed_row += " O "
                if element == 0:
                    completed_row += "   "
            print(completed_row)

    @classmethod
    def get_user_choice(cls):
        while True:
            try:
                row = int(input("Row >>")) - 1
                column = int(input("Column >>")) - 1
                if row in range(3) and column in range(3):
                    return str(row) + str(column)
                else:
                    print("Wrong input. Please try again...")
                    continue
            except ValueError:
                print("Wrong input. please try again...")
                continue

    # Awaits server chat response.
    def await_response(self):
        while True:
            data = self.my_socket.recv(2).decode()
            if data != "" and data != "Received and Forwarded":
                return data
            continue

    # Receives chat message
    def receive_chat_message(self):
        while True:
            message_length = self.my_socket.recv(2).decode()
            message = self.my_socket.recv(int(message_length)).decode()
            if message == "Client exited chat.":
                print("\n[+] Chat ended by other client.")
                exit(0)

            if message == "Received and Forwarded":
                return
            else:
                print("Friend: " + message)
                return

    # Receives generic message.
    def receive_message(self):
        self.receive_chat_message()
        data = self.await_response()
        if data == "Game:":
            return self.receive_game_directions()

    # Receives updated game position.
    def receive_game_directions(self):
        message_length = self.my_socket.recv(2).decode()
        data = pickle.loads(self.my_socket.recv(int(message_length)))
        if type(data) == str:
            if data == "Tie":
                return "Tie"
            if data[:6] == "Winner":
                return data[7:]
        else:
            self.board = data
            return "No Winner"

    def send_message(self):
        message = input("Me >> ")
        message_length = str(len(message))
        if len(message_length) == 1:
            message_length = "0" + message_length
        self.my_socket.send(message_length.encode())
        self.my_socket.send(message.encode())

        if message == "EXIT":
            data = self.my_socket.recv(1024).decode()
            if data == "Confirmed":
                self.my_socket.close()
                exit(0)

    def turn(self):
        self.receive_message()
        self.present_board()
        coordinates = self.get_user_choice()
        self.send_game_coordinates(coordinates)
        self.send_message()

    def await_response(self):
        while True:
            data = self.my_socket.recv(1024).decode()
            if data != "" and data != "Received and Forwarded":
                return data
            continue

    def initialize_communications(self):
        data = self.await_response()
        if data == "Awaiting other client.":
            self.first = True
            while True:
                data = self.my_socket.recv(1024).decode()
                if data == "Other client connected":
                    print("[+] Chat connected.")
                    while True:
                        self.my_socket.send("Start Game".encode())
                        break
                    break
                continue
        elif data == "Other client connected":
            print("[+] Chat connected.")

            return


client = Client()
