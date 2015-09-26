import sys
import os
from maze import Maze
import pdb
from time import sleep

MAZES = "./mazes/"

def DFS(parsedMaze, timeseries, startingNode):
    nodeStack = list()

    if (timeseries):
        move = 0
        timelapse = list()
        timelapse.append(parsedMaze)

    startingNode.visitNode()
    nodeStack.append(startingNode)
    currNode = startingNode

    while (not currNode.isEnding()):
        currNode.addChildren(parsedMaze)
        prevNode = currNode
        currNode = currNode.getNextChild()


        while (currNode == None):
            if (len(nodeStack) == 0):
                return None

            prevNode = nodeStack.pop()
            currNode = prevNode.getNextChild()

            if (prevNode.hasMoreChildren()):
                nodeStack.append(prevNode)

            if currNode is not None:
                nodeStack.append(currNode)

        currNode.visitNode()

        if timeseries:

            parsedMaze[currNode.coordinates['y']][currNode.coordinates['x']] = '.'
            move += 1
            timelapse.append(parsedMaze)
            for row in parsedMaze:
                for elem in row:
                    print elem,
                print '\n',

            sleep(0.0)

        if (prevNode.hasMoreChildren()):
            nodeStack.append(prevNode)

        nodeStack.append(currNode)

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

    print len(traversed)

    return parsedMaze

def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    solved = m.solveUsing(DFS, True)

    print m.expandedNodes()

    with open(argv[1] + '_dfs.out', 'w') as f:
        for row in solved:
            for elem in row:
                f.write(elem)
            f.write('\n')

if __name__ == "__main__":
    main()

