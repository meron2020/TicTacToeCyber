import socket


class Client:
    def __init__(self):
        self.my_socket = socket.socket()
        self.my_socket.connect(("127.0.0.1", 8820))
        self.board = [[], [], []]

    # Sends game move to server.
    def send_game_coordinates(self, coordinates):
        message = "Game:" + str(coordinates)
        self.my_socket.send(message.encode())

        if message == "EXIT":
            data = self.my_socket.recv(1024).decode()
            if data == "Confirmed":
                self.my_socket.close()
                exit(0)

    # Awaits server chat response.
    def await_response(self):
        while True:
            data = self.my_socket.recv(1024).decode()
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
        if data[:4] == "Game":
            self.receive_game_directions(data)
        if data[:4] == "Chat":
            Client.receive_chat_message(data)

    # Receives updated game position.
    def receive_game_directions(self, data):
        if data[:4] == "Game":
            if data[6:] == "Tie":
                return "Tie"
            if data[6:12] == "Winner":
                return data[13:]
            self.board = data[6:]
            return "No Winner"
