from helper import *
import random
import copy

solved = [[i, i - 4, i - 8, i - 12] for i in range(13, 16)] + [[0, 12, 8, 4]]


class Board:
    def __init__(self, board=copy.deepcopy(solved), hole=(3, 0)):
        # Current board in column major 2D list, initialized to 'board'
        self.board = board

        # Current position of the hole, represented as a 0
        self.hole = hole

    # String rep of board with newlines before each row
    def __str__(self):
        out = ""
        for i in range(3, -1, -1):
            for j in range(4):
                out += str(self.board[j][i]) + " "
            out += "\n" if i != 0 else ""
        return out

    # Returns a list of coordinates surrounding the hole
    def hole_squares(self):
        out = [(self.hole[0], self.hole[1] + 1)]
        out.append((self.hole[0], self.hole[1] - 1))
        out.append((self.hole[0] + 1, self.hole[1]))
        out.append((self.hole[0] - 1, self.hole[1]))
        return list(filter(is_valid_square, out))

    # Moves the number at 'pos' to the hole and returns True
    # if legal, False otherwise
    def move(self, pos):
        if pos in self.hole_squares():
            num = self.board[pos[0]][pos[1]]
            self.board[self.hole[0]][self.hole[1]] = num
            self.board[pos[0]][pos[1]] = 0
            self.hole = pos
            return True
        else:
            return False

    # Finds the coordinate of 'num' in the board, None if is not on the board
    def find_num(self, num):
        for i, _ in enumerate(self.board):
            for j, el in enumerate(self.board[i]):
                if el == num:
                    return (i, j)
        return None

    # Shuffles the board into a random orientation by making 5,000 random
    # moves with no repeats (moving the same number back and forth)
    def shuffle(self):
        count = 0
        prev = self.hole
        next = random.choice(self.hole_squares())
        while count < 5000:
            self.move(next)
            next_nums = self.hole_squares()
            next_nums.remove(prev)
            next = random.choice(next_nums)
            prev = self.hole
            count += 1

    # Creates a new board dereferenced from the old board.
    def copy(self):
        out = []
        for col in self.board:
            out.append(list(col))
        return Board(out, self.hole)


# Returns the solved position of 'num', None if not on board
def solved_pos(num):
    for i in range(0, 16):
        if solved[i % 4][3 - int(i / 4)] == num:
            return (i % 4, 3 - int(i / 4))
