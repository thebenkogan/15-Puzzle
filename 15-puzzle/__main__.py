import board
import solver
import time
from datetime import datetime

bd = board.Board()
bd.shuffle()
print(bd)
path = solver.new_solver(bd)
print(len(path))
for mv in path:
    bd.move(mv)
print(bd)

while False:
    print("")
    num = input()
    if num == "q":
        exit()
    if num == "s":
        bd.shuffle()
        print(bd)
        continue
    if num == "solve":
        if bd.board == board.solved:
            print("Already solved.")
            continue
        path = solver.solve(bd)
        if len(path) == 0:
            print("No path found.")
        else:
            for mv in path:
                bd.move(mv)
                print(bd)
                if bd.board == board.solved:
                    print("Solved!")
                else:
                    print("")
                time.sleep(0.7)
        continue
    try:
        num = int(num)
    except:
        print("Try again.")
        continue
    coord = bd.find_num(num)
    if coord == None:
        print("Number not on board, try again.")
    else:
        if bd.move(coord):
            print(bd)
        else:
            print("Illegal move.")
