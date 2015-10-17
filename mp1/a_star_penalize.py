from maze import Maze
import os
import sys
import pdb
from time import sleep
from math import sqrt

MAZES = './mazes/'

def manhattanDist(curr, endCoord):
    return abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y']) + curr.cost

def rawManhattanDist(curr, endCoord):
    if (curr.direction == curr.parent.direction):
        reduction = 0
    else:
        reduction = 1

    return abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y']) + (curr.cost - reduction)

def euclideanDist(curr, endCoord):
    return sqrt(abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y'])) + curr.cost

def jeffDist(curr, endCoord):
    return curr + curr.cost

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
    marked = 0

    while (not currNode.isEnding()):
        currNode.visitNode()
        currNode.addChildren(parsedMaze)
        currNode = currNode.nextBestNode()

        if currNode is None:
            break

        if timeseries:
            marked += 1
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

    print traversed[0].cost
    print marked
    return parsedMaze



def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    solved =m.solveUsing(A_Star, timeseries=True, heuristic=manhattanDist, comparisonFunc=comparisonFunc, costAssign=costAssignment)
    print m.expandedNodes()

    with open(argv[1] + '_a_star_+1forward_newheur.out', 'w') as f:
        for row in solved:
            for elem in row:
                f.write(elem)
            f.write('\n')

if __name__ == "__main__":
    main()
