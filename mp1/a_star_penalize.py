from maze import Maze
import os
import sys
import pdb
from time import sleep
from math import sqrt

MAZES = './mazes/'

def manhattanDist(curr, endCoord):
    return abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y']) + curr.cost

def euclideanDist(curr, endCoord):
    return sqrt(abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y'])) + curr.cost

def chebyshevDist(curr, endCoord):
    return max(abs(curr.coordinates['x'] - endCoord['x']), abs(curr.coordinates['y'] - endCoord['y'])) + curr.cost

def crossDist(curr, endCoord):
    dx1 = curr.coordinates['x'] - endCoord['x']
    dy1 = curr.coordinates['y'] - endCoord['y']
    dx2 = curr.starting['x'] - endCoord['x']
    dy2 = curr.starting['y'] - endCoord['y']

    return abs(dx1 * dy2 - dx2 * dy1) + curr.cost

def comparisonFunc(comp, best):
    return comp > best

def costAssignment(parent, child):
    if (parent.currDirection == child.currDirection):
        return parent.cost + 1
    else:
        return parent.cost + 2

def A_Star(parsedMaze, timeseries, startingNode):

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

    traversed = currNode.getTraversal()

    for currNode in traversed:
        parsedMaze[currNode.coordinates['y']][currNode.coordinates['x']] = 'X'
        move += 1
        timelapse.append(parsedMaze)

        for row in parsedMaze:
            for elem in row:
                print elem,
            print '\n',

        sleep(0.1)

    print len(traversed)



def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    m.solveUsing(A_Star, timeseries=True, heuristic=crossDist, comparisonFunc=comparisonFunc, costAssign=costAssignment)

if __name__ == "__main__":
    main()
