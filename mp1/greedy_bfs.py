from maze import Maze
import sys
import os
from time import sleep
import pdb
from math import sqrt

MAZES = './mazes/'

def manhattanDist(curr, endCoord):
    return abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y'])

def euclideanDist(curr, endCoord):
    return sqrt(abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y']))

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

            sleep(0.0)

    traversed = currNode.getTraversal()

    for currNode in traversed:
        parsedMaze[currNode.coordinates['y']][currNode.coordinates['x']] = 'X'
        move += 1
        timelapse.append(parsedMaze)

        for row in parsedMaze:
            for elem in row:
                print elem,
            print '\n',

        sleep(0.0)

    return parsedMaze

def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    solved = m.solveUsing(greedyBFS, True, euclideanDist, comparisonFunc)

    print m.expandedNodes()

    with open(argv[1] + '_greedy_bfs.out', 'w') as f:
        for row in solved:
            for elem in row:
                f.write(elem)
            f.write('\n')


if __name__ == "__main__":
    main()
