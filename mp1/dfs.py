import sys
import os
from maze import Maze

MAZES = "./mazes/"

def DFS(parsedMaze, timeseries, startingNode, mazeClass):
    nodeStack = list()

    if (timeseries):
        move = 0
        timelapse = list()
        timelapse.append(parsedMaze)

    startingNode.visitNode()
    nodeStack.append(startingNode)
    currNode = startingNode

    while (not currNode.isEnding()):
        currNode.addChildren(parsedMaze, mazeClass)
        currNode = currNode.getNextChild()

        while (currNode == None):
            currNode = nodeStack.pop()
            currNode = currNode.getNextChild()
            nodeStack.append(currNode)

        currNode.visitNode()

        if timeseries:
            parsedMaze[currNode.coordinates['y']][currNode.coordinates['x']] = '.'
            move += 1
            timelapse.append(parsedMaze)

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

