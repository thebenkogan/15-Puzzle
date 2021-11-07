import board

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


def next_moves(bd):
    num_insert = next_insertion(bd)
    if num_insert == 16:
        return []
    path = eval_insert(bd, None, None, depth, num_insert)
    if path == None:
        return []
    return path


def eval_insert(bd, prev, start, depth, num):
    if bd.stale == 7:
        return None
    if bd.board == board.solved or order[next_insertion(bd)] > order[num]:
        return [start]
    if depth == 0:
        return None
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
    boards.sort(key=closeness)

    best_path = None
    for opt in boards:
        path = eval_insert(opt, bd.hole, opt.hole, depth - 1, num)
        if path != None:
            if start != None:
                path.insert(0, start)
            return path
    return best_path


# Returns the next number in [1, 15] to insert on the board with lower
# numbers already in their correct position. If solved, this is 16.
def next_insertion_new(bd):
    count = 1
    for i in range(0, 16):
        if bd.board[i % 4][3 - int(i / 4)] == i + 1:
            count += 1
        else:
            break
    return count


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


# FIX: Only allow the number to move backwards once. This causes too many
# branches with forward and backward movement.

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
