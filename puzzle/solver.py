from puzzle import board
import heapq as hq

# Returns a path specifying the list of input moves to solve 'bd'.
def solve(bd):
    bd = bd.copy()
    path = []
    while bd.board != board.solved:
        res = insert_next(bd)
        path += res
        for mv in res:
            bd.move(mv)
    return path


# Returns a path specifying the list of input moves to insert the number.
def insert_next(bd):
    frontier = []
    current = bd
    solved_path = []
    num = next_insertion(bd)

    while len(solved_path) == 0:
        next_nums = current.hole_squares()
        if current.prev != None:
            next_nums.remove(current.prev)
        for pos in next_nums:
            next = current.copy()
            next.prev = next.hole
            next.move(pos)
            next.path.append(pos)
            f = len(next.path) + closeness_one(next, num)
            hq.heappush(frontier, (f, next))

        best = hq.heappop(frontier)

        if best[1].board == board.solved or order[next_insertion(best[1])] > order[num]:
            solved_path = best[1].path

        current = best[1]

    return solved_path


# Returns a path specifying the list of input moves to insert the number.
def solve_full(bd):
    frontier = []
    current = bd
    solved_path = []

    while len(solved_path) == 0:
        next_nums = current.hole_squares()
        if current.prev != None:
            next_nums.remove(current.prev)
        for pos in next_nums:
            next = current.copy()
            next.prev = next.hole
            next.move(pos)
            next.path.append(pos)
            f = len(next.path) + closeness_all(next) + linear_conflicts(bd)
            hq.heappush(frontier, (f, next))

        best = hq.heappop(frontier)

        if best[1].board == board.solved:
            solved_path = best[1].path

        current = best[1]

    return solved_path


# Returns the next number in [1, 15] to insert on the board with lower
# numbers of 'order' already in their correct position. If solved, this
# is 16.
def next_insertion(bd):
    next = 16
    for num in order:
        target = solved_dict[num]
        if bd.board[target[0]][target[1]] != num:
            next = num
            break
    return next


# Returns the Manhattan distance of 'num_insert' to its target position.
def closeness_one(bd, num_insert):
    for i in range(len(bd.board)):
        for j, num in enumerate(bd.board[i]):
            if num == num_insert:
                target = solved_dict[num]
                return abs(target[0] - i) + abs(target[1] - j)


# Measures the closeness of the board by checking how close every
# number is to its solved position using the Manhattan distance. A
# low value corresponds to a close-to-solved orientation.
def closeness_all(bd):
    total = 0
    for i in range(len(bd.board)):
        for j, num in enumerate(bd.board[i]):
            if num != 0:
                target = solved_dict[num]
                dist = abs(target[0] - i) + abs(target[1] - j)
                total += dist
    return total


# Adds 2 for every linear conflict on the board. A linear conflict is
# any 2 numbers in the same row with the same target row, but are in the
# wrong order relative to the solved position.
def linear_conflicts(bd):
    total = 0
    for i in range(4):
        seen = []
        for j in range(4):
            if bd.board[j][i] != 0 and row_dict[bd.board[j][i]] == i:
                for el in seen:
                    if bd.board[j][i] < el:
                        total += 2
                seen.append(bd.board[j][i])
    return total


# The order of insertions specified by the keys, value is ascending
order = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7,
    9: 8,
    13: 9,
    10: 10,
    14: 11,
    11: 12,
    12: 13,
    15: 14,
}

# Maps number to solved position
solved_dict = {
    1: (0, 3),
    2: (1, 3),
    3: (2, 3),
    4: (3, 3),
    5: (0, 2),
    6: (1, 2),
    7: (2, 2),
    8: (3, 2),
    9: (0, 1),
    10: (1, 1),
    11: (2, 1),
    12: (3, 1),
    13: (0, 0),
    14: (1, 0),
    15: (2, 0),
}

# Maps number to solved row
row_dict = {
    1: 3,
    2: 3,
    3: 3,
    4: 3,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 1,
    10: 1,
    11: 1,
    12: 1,
    13: 0,
    14: 0,
    15: 0,
}
