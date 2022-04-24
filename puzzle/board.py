import random
import copy


# Solved board
solved = [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [0, 12, 8, 4]]


class Board:
    def __init__(self, board=copy.deepcopy(solved), hole=(3, 0), path=[], prev=None):
        # Current board in column major 2D list, initialized to 'board'
        self.board = board

        # Current position of the hole, represented as a 0
        self.hole = hole

        # The path to this board from some other board, represented
        # by numbers corresponding to the order of tiles moves.
        self.path = path

        # The coordinate of the last hole position.
        self.prev = prev

    # String rep of board with newlines before each row
    def __str__(self):
        out = ""
        for i in range(3, -1, -1):
            for j in range(4):
                out += str(self.board[j][i]) + " "
            out += "\n" if i != 0 else ""
        return out

    def __lt__(self, _):
        return True

    ## True if 'pos' is a legal coordinate
    def __is_valid_square(self, pos):
        return pos[0] >= 0 and pos[0] <= 3 and pos[1] >= 0 and pos[1] <= 3

    # Returns a list of coordinates surrounding the hole
    def hole_squares(self):
        out = [0] * 4
        out[0] = (self.hole[0], self.hole[1] + 1)
        out[1] = (self.hole[0], self.hole[1] - 1)
        out[2] = (self.hole[0] + 1, self.hole[1])
        out[3] = (self.hole[0] - 1, self.hole[1])
        return list(filter(self.__is_valid_square, out))

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
        return Board(out, self.hole, list(self.path), self.prev)
