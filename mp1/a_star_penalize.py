from maze import Maze
import os
import sys

def A_Star(parsedMaze, timeSeries, startingNode):
    pass


def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1])
    m.solveUsing(A_Star, timeseries=True, heuristic=None, comparisonFunc=None)


if __name__ == "__main__":
    main()
