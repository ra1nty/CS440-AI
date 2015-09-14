import sys
import os
from maze import Maze

MAZES = "./mazes/"

def DFS(parsedMaze, timeseries, getNextBranches):


def main():
    files = os.readdir(MAZES)

    for f in files:
        m = Maze(f)
        m.solveUsing(DFS, True,



if __name__ == "__main__":
    main()

