import sys
import os
import Queue
from maze import Maze

MAZES = "./mazes/"

def BFS(parsedMaze, timeseries, startingNode):
    q = Queue.Queue()
    q.put(startingNode)
    t = startingNode
    while(not q.empty() and not t.isEnding()):
        t = q.get()
        t.visitNode()
        t.addChildren(parsedMaze)

        for n in t.children:
            print "test"



    return None

def main():
    files = os.listdir(MAZES)

    for f in files:
        m = Maze(MAZES + f)
        solved = m.solveUsing(BFS, True)

    if solved is None:
        return "No solution"
    else:
        print solved


main()