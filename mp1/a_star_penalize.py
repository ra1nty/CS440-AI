from maze import Maze
import os
import sys

def manhattanDist(curr, end):
    return abs(curr['x'] - end['x']) + abs(curr['y'] - end['y'])

def comparisonFunc(comp, best):
    return comp > best

def A_Star(parsedMaze, timeSeries, startingNode):

    currNode = startingNode
    move = 0

    while (not currNode.isEnding()):
        pass


def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1])
    m.solveUsing(A_Star, timeseries=True, heuristic=manhattanDist, comparisonFunc=comparisonFunc)


if __name__ == "__main__":
    main()
