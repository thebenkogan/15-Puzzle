import board
import heapq as hq

depth = 25

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

# Returns a path to the solved position from the current state of the board,
# empty if no path found.
def solve(bd):
    bd = bd.copy()
    path = []
    while bd.board != board.solved:
        num_insert = next_insertion(bd)
        res = eval_insert(bd, None, None, depth, num_insert)
        if res == None:
            print(bd)
            return []
        else:
            path += res
            for mv in res:
                bd.move(mv)
    return path


def eval_insert(bd, prev, start, depth, num):
    if bd.stale == 7:
        return None
    if depth == 0:
        return None
    if bd.board == board.solved or order[next_insertion(bd)] > order[num]:
        return [start]
    next_nums = bd.hole_squares()
    if prev != None:
        next_nums.remove(prev)

    i = 0
    while i < len(next_nums):
        if not makes_progress(bd, next_nums[i], num):
            next_nums.remove(next_nums[i])
        i += 1

    boards = []
    for pos in next_nums:
        next = bd.copy()
        next.progress = bd.progress
        next.move(pos)
        if bd.board[pos[0]][pos[1]] != num:
            next.stale = bd.stale + 1
        else:
            next.stale = 0
        boards.append(next)
    boards.sort(key=heuristic)

    best_path = None
    for opt in boards:
        path = eval_insert(opt, bd.hole, opt.hole, depth - 1, num)
        if path != None:
            if start != None:
                path.insert(0, start)
            return path
    return best_path


def new_solver(bd):
    bd = bd.copy()
    path = []
    while bd.board != board.solved:
        res = solve2(bd)
        path += res
        for mv in res:
            bd.move(mv)
    return path


def func(x):
    return x[0]


def solve2(bd):
    print("")
    print(bd)
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
            f = len(next.path) + closeness2(next, num)
            hq.heappush(frontier, (f, next))

        best = hq.heappop(frontier)

        if best[1].board == board.solved or order[next_insertion(best[1])] > order[num]:
            solved_path = best[1].path

        current = best[1]

    return solved_path


# Returns the next number in [1, 15] to insert on the board with lower
# numbers of 'order' already in their correct position. If solved, this
# is 16.
def next_insertion(bd):
    next = 16
    for num in order:
        target = board.solved_dict[num]
        if bd.board[target[0]][target[1]] != num:
            next = num
            break
    return next


# True if moving 'pos' to the hole progresses 'num' to its target
# position. A number does not make progress to its position if it
# moves away from the target. If the number does not move, then it
# is considered as making progress.
def makes_progress(bd, pos, num):
    if bd.board[pos[0]][pos[1]] != num:
        return True
    target = board.solved_dict[num]
    old_diff = abs(target[0] - pos[0]) + abs(target[1] - pos[1])
    new_diff = abs(target[0] - bd.hole[0]) + abs(target[1] - bd.hole[1])
    if new_diff < old_diff:
        return True
    else:
        out = bd.progress
        bd.progress = False
        return out


# Evaluates a board based on closeness to solved position and number
# of linear conflicts.
def heuristic(bd):
    return closeness(bd) + linear_conflicts(bd)


# Measures the closeness of the board by checking how close every
# number is to its solved position using the Manhattan distance. A
# low value corresponds to a close-to-solved orientation.
def closeness(bd):
    total = 0
    for i in range(len(bd.board)):
        for j, num in enumerate(bd.board[i]):
            if num != 0:
                target = board.solved_dict[num]
                dist = abs(target[0] - i) + abs(target[1] - j)
                total += dist
    return total


# Measures the closeness of the board by checking how close every
# number is to its solved position using the Manhattan distance, with
# favor towards 'num'.
def closeness2(bd, num_insert):
    for i in range(len(bd.board)):
        for j, num in enumerate(bd.board[i]):
            if num == num_insert:
                target = board.solved_dict[num]
                return abs(target[0] - i) + abs(target[1] - j)


# Adds 2 for every linear conflict on the board. A linear conflict is
# any 2 numbers in the same row with the same target row, but are in the
# wrong order relative to the solved position.
def linear_conflicts(bd):
    total = 0
    for i in range(4):
        seen = []
        for j in range(4):
            if bd.board[j][i] != 0 and board.row_dict[bd.board[j][i]] == i:
                for el in seen:
                    if bd.board[j][i] < el:
                        total += 2
                seen.append(bd.board[j][i])
    return total
