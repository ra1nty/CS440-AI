import sys
import os
from maze import Maze

MAZES = "./mazes/"

def main():
    files = os.listdir(MAZES)

    for f in files:
        m = Maze(MAZES + f)
        solved = m.solveUsing(BFS, True)

    print "blah"


def BFS(parsedMaze, timeseries, startingNode):

    return None


main()