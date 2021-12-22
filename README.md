# 15 Puzzle REPL Game With a Solver!

Use `make run` to play.

## How the Solver Works

Initially, I went for a full A* search from the start position to the goal state. As I quickly realized, my heuristics were not good enough and the solver did not terminate in a reasonable time. For my heuristic, I use the Manhattan distance of every number to its target position, along with an addition of two moves for all linear conflicts (two numbers in the right row but in the wrong order). 

To reduce the search space, I decided to insert the first four numbers with four separate A* searches. This provides a more human solution for the first row, and I am able to run the full A* search on the remaining orientation relatively well. The solve time really depends on the scramble. Sometimes it gets a solution in one second, while other times, it takes over ten seconds. The generated solve path has an average of about 75 moves, which is quite good. Obviously, the human-like solution to the first four numbers inflates the move count, but that's the tradeoff for the faster solve time.
