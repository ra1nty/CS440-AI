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
        currNode.printNode()
        currNode.addChildren(parsedMaze)
        prevNode = currNode
        currNode = currNode.getNextChild()


        while (currNode == None):
            if (len(nodeStack) == 0):
                return None

            prevNode = nodeStack.pop()
            currNode = prevNode.getNextChild()

            if (prevNode.hasMoreChildren()):
                nodeStack.append(tempNode)

            if currNode is not None:
                nodeStack.append(currNode)

        currNode.visitNode()

        if timeseries:
            parsedMaze[currNode.coordinates['y']][currNode.coordinates['x']] = '.'
            for row in parsedMaze:
                for elem in row:
                    print elem,
                print '\n',
            print ""

            sleep(.2)

            move += 1
            timelapse.append(parsedMaze)

        if (prevNode.hasMoreChildren()):
            nodeStack.append(prevNode)

        nodeStack.append(currNode)


    if timeseries:
        return (move, timelapse)
    else:
        return None

def main():
    files = os.listdir(MAZES)

    for f in files:
        m = Maze(MAZES + f)
        solved = m.solveUsing(DFS, True)

    print solved

if __name__ == "__main__":
    main()

