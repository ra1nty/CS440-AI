from maze import Maze
import os
import sys
import pdb

MAZES = './mazes/'

def ManhattanDist(curr, goal):
    return abs(curr.coordinates['x'] - goal['x']) + abs(curr.coordinates['y'] - goal['y']) + curr.cost

def compare(comp, best):
    return comp > best

def cost(parent, child):
        return parent.cost + 1

def a_star(parsedMaze, timeseris, startingNode):

    current = startingNode
    expanded = 0

    while (not current.isEnding()):
        expanded += 1
        current.visitNode()
        current.addChildren(parsedMaze)
        current = current.nextBestNode()

        if current is None:
            break

    path = current.getTraversal()

    for currNode in path:
        if ( not((currNode.coordinates['y'] == startingNode.coordinates['y'])and(currNode.coordinates['x'] == startingNode.coordinates['x']))):
            parsedMaze[currNode.coordinates['y']][currNode.coordinates['x']] = '.'

    for row in parsedMaze:
            for elem in row:
                print elem,
            print '\n',

    print "path cost of solution:", len(path)
    print "no of nodes expanded: ", expanded



def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    m.solveUsing(a_star, timeseries=True, heuristic=ManhattanDist, comparisonFunc=compare, costAssign=cost)

if __name__ == "__main__":
    main()


