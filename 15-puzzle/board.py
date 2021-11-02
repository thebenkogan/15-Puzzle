from helper import *


class Board:

    # Current board, initialized in solved state
    board = [[i, i - 4, i - 8, i - 12] for i in range(13, 16)] + [[0, 12, 8, 4]]

    # Current position of the hole
    hole = (3, 0)

    # String rep of board with newlines before each row
    def __str__(self):
        out = ""
        for i in range(3, -1, -1):
            for j in range(4):
                out += str(self.board[j][i]) + " "
            out += "\n" if i != 0 else ""
        return out

    # Returns a list of numbers surrounding the hole
    def __hole_squares(self):
        potential = [(self.hole[0], self.hole[1] + 1)]
        potential.append((self.hole[0], self.hole[1] - 1))
        potential.append((self.hole[0] + 1, self.hole[1]))
        potential.append((self.hole[0] - 1, self.hole[1]))
        return list(filter(isValidSquare, potential))

    # Moves the number at 'pos' to the hole and returns True
    # if legal, False otherwise
    def move(self, pos):
        if pos in self.__hole_squares():
            num = self.board[pos[0]][pos[1]]
            self.board[self.hole[0]][self.hole[1]] = num
            self.board[pos[0]][pos[1]] = 0
            return True
        else:
            return False


bd = Board()
bd.move((3, 0))
print(bd)
