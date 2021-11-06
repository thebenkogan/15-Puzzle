import board

depth = 50
order = {
    0: 1,
    1: 5,
    2: 2,
    3: 6,
    4: 3,
    5: 4,
    6: 7,
    7: 8,
    8: 9,
    9: 13,
    10: 10,
    11: 14,
    12: 11,
    13: 12,
    14: 15,
    15: 16,
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
    if next_insertion(bd) > num:
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
def next_insertion(bd):
    count = 1
    for i in range(0, 16):
        if bd.board[i % 4][3 - int(i / 4)] == i + 1:
            count += 1
        else:
            break
    return count


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
    return new_diff < old_diff


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
