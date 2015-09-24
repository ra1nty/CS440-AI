from maze import Maze
import sys
import os
from time import sleep
import pdb
from math import sqrt

MAZES = './mazes/'

def manhattanDist(curr, end):
    return abs(curr['x'] - end['x']) + abs(curr['y'] - end['y'])

def euclideanDist(curr, end):
    return sqrt(abs(curr['x'] - end['x']) + abs(curr['y'] - end['y']))

def comparisonFunc(comp, best):
    return comp > best

def greedyBFS(parsedMaze, timeseries, startingNode):

    currNode = startingNode
    move = 0
    timelapse = []

    while (not currNode.isEnding()):
        currNode.visitNode()
        currNode.addChildren(parsedMaze)
        currNode = currNode.nextBestNode()

        if currNode is None:
            break

        if timeseries:
            parsedMaze[currNode.coordinates['y']][currNode.coordinates['x']] = '.'
            move += 1
            timelapse.append(parsedMaze)

            for row in parsedMaze:
                for elem in row:
                    print elem,
                print '\n',

            sleep(0.1)

    if timeseries:
        return (move, timelapse)

def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    solved = m.solveUsing(greedyBFS, True, manhattanDist, comparisonFunc)

    print solved[0]

if __name__ == "__main__":
    main()
