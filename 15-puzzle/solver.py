import board

depth = 20
counter = 0


def next_moves(bd):
    global counter
    num_insert = next_insertion(bd)
    if num_insert == 16:
        return []
    next_nums = bd.hole_squares()
    best_path = [0] * (depth + 2)
    for pos in next_nums:
        stale = 1 if bd.board[pos[0]][pos[1]] != num_insert else 0
        opt = bd.copy()
        opt.move(pos)
        path = eval_insert(
            opt, bd.hole, pos, depth, num_insert, board.solved_pos(num_insert), stale
        )
        print(pos)
        print(counter)
        counter = 0
        if path == None:
            continue
        if len(path) < len(best_path):
            best_path = path
    if len(best_path) > depth + 1:
        return []
    return best_path


def eval_insert(bd, prev, start, depth, num, num_pos, stale):
    global counter
    counter += 1
    if stale == 6:
        return None
    if next_insertion(bd) > num:
        return [start]
    if depth == 0:
        return None
    next_nums = bd.hole_squares()
    next_nums.remove(prev)

    i = 0
    while i < len(next_nums):
        if not makes_progress(bd, next_nums[i], num, num_pos):
            next_nums.remove(next_nums[i])
        i += 1

    best_path = None
    for pos in next_nums:
        if bd.board[pos[0]][pos[1]] != num:
            stale += 1
        else:
            stale = 0
        next = bd.copy()
        next.move(pos)
        path = eval_insert(next, bd.hole, pos, depth - 1, num, num_pos, stale)
        if path != None and best_path == None:
            path.insert(0, start)
            best_path = path
            break
        # if path != None and len(path) < len(best_path):
        #    path.insert(0, start)
        #    best_path = path
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
def makes_progress(bd, pos, num, target):
    if bd.board[pos[0]][pos[1]] != num:
        return True
    old_diff = abs(target[0] - pos[0]) + abs(target[1] - pos[1])
    new_diff = abs(target[0] - bd.hole[0]) + abs(target[1] - bd.hole[1])
    return new_diff < old_diff


# Measures the exactness of the board by checking how many numbers
# are in the correct position with respect to the solved state. Returns
# a number in [0, 1], with 1 corresponding to the solved state.
def exactness(bd):
    count = 0
    for i in range(len(bd.board)):
        for j, el in enumerate(bd.board[i]):
            if el == board.solved[i][j]:
                count += 0.0625
    return count
