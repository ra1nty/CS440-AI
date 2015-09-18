import sys
import os
import Queue
from maze import Maze

MAZES = "./mazes/"
# maze constants to improve readability

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

def BFS(parsedMaze, timeseries, startingNode):
    q = Queue.Queue()
    q.put(startingNode)
    t = startingNode
    while(not q.empty() and not t.isEnding()):
        t = q.get()
        t.visitNode()
        t.addChildren(parsedMaze)

        for n in t.children:
            if n is not None and not n.visited:
                n.visitNode()
                q.put(n)






    return None

def main():
    files = os.listdir(MAZES)

    for f in files:
        m = Maze(MAZES + f)
        print f
        solved = m.solveUsing(BFS, True)

    if solved is None:
        return "No solution"
    else:
        print solved


main()