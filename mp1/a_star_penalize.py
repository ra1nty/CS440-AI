from maze import Maze
import os
import sys
import pdb
from time import sleep

MAZES = './mazes/'

def manhattanDist(curr, endCoord):
    return abs(curr.coordinates['x'] - endCoord['x']) + abs(curr.coordinates['y'] - endCoord['y']) + curr.cost

def comparisonFunc(comp, best):
    return comp > best

def costAssignment(parent, child):
    if (parent.currDirection == child.currDirection):
        return parent.cost + 2
    else:
        return parent.cost + 1

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
    m.solveUsing(A_Star, timeseries=True, heuristic=manhattanDist, comparisonFunc=comparisonFunc, costAssign=costAssignment)

if __name__ == "__main__":
    main()
