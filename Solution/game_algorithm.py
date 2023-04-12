class Game:
    def __init__(self):
        self.board = [[], [], []]
        self.setup_board()
        print(self.board)

    # Initializes a board.
    def setup_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i].append(0)

    # Checks if there's a tie
    def check_if_tie(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return True

    # Checks if someone won by a row.
    def check_rows(self, user):
        for row in self.board:
            if row[0] == user and row[1] == user and row[2] == user:
                return True

    # Checks if someone won by a column.
    def check_columns(self, user):
        for i in range(3):
            winner = True
            for row in self.board:
                if row[i] != user:
                    winner = False
            if winner:
                return True
        return False

    # Check if there is a winner on the diagonals.
    def check_diagonals(self, user):
        winner = True
        for i in range(3):
            if self.board[i][i] != user:
                winner = False

        if winner:
            return True
        winner = True
        for i in range(3):
            if self.board[i][2 - i] != user:
                winner = False

        if winner:
            return True

        return False

    # Checks if a there's a winner.
    def check_if_winner(self, user):
        return self.check_columns(user) or self.check_rows(user) or self.check_diagonals(user)

    # Adds coordinates
    def add_input(self, move_coordinates, user):
        self.board[move_coordinates[0]][move_coordinates[1]] = user

    # Checks if move is possible.
    def check_if_move_able(self, move_coordinates):
        return self.board[move_coordinates[0]][move_coordinates[1]] == 0
