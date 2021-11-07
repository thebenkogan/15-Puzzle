import board
import solver
import time
from datetime import datetime

bd = board.Board()
bd.shuffle()

while False:
    moves = solver.next_moves(bd)
    if len(moves) == 0:
        if bd.board == board.solved:
            print("Solved")
        else:
            print("Could not find path")
        exit()
    for move in moves:
        bd.move(move)
        print("")
        print(bd)
        time.sleep(0.1)

i = 0
good = 0
bad_boards = []
move_counts = []
start = datetime.now()
while i < 50:
    print(i)
    bd.shuffle()
    move_count = 0
    while bd.board != board.solved:
        moves = solver.next_moves(bd)
        if len(moves) == 0:
            bad_boards.append(bd.copy())
            break
        move_count += len(moves)
        for move in moves:
            bd.move(move)
    if bd.board == board.solved:
        move_counts.append(move_count)
        good += 1
    i += 1
end = datetime.now()

solve_time = (end - start).seconds

print("Solved " + str(good) + " boards out of 50.")
avg = sum(move_counts) / len(move_counts)
print("Solve move average = " + str(avg))
print("Solve time = " + str(solve_time))

print("Bad boards:")
for bd in bad_boards:
    print("")
    print(bd)
