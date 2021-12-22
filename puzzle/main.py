from . import board
from . import solver
import datetime as dt

print("")
print("Enter a valid number to make a move.")
print("Enter 's' to scramble.")
print("Enter 'solve' to find a solution.")
print("Enter 'q' to exit. ")
print("")

bd = board.Board()
print(bd)

while True:
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
        start = dt.datetime.now()
        path = solver.solve(bd)
        end = dt.datetime.now()
        delta = (end - start).seconds
        print("")
        print(f"Solution found in {delta} seconds!")
        print("Enter 'n' to see next move.")
        print("Enter 'q' to resume from current orientation.")
        for mv in path:
            choice = ""
            while choice == "":
                inp = input()
                if inp == "q" or inp == "n":
                    choice = inp
                else:
                    print("Try again.")

            if choice == "q":
                print(bd)
                break

            bd.move(mv)
            print(bd)
            if bd.board == board.solved:
                print("Solved in " + str(len(path)) + " moves!")
            else:
                print("")
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

# Benchmarking
bd = board.Board()
results = []
for i in range(50):
    bd.shuffle()
    path = solver.solve_halves(bd)
    results.append(len(path))
    print(i)
print(sum(results) / len(results))
