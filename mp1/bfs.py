import sys
import os
import Queue
from maze import Maze

MAZES = "./mazes/"

def BFS(parsedMaze, timeseries, startingNode):
    q = Queue.Queue()
    q.put(startingNode)


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