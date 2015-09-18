import sys
import os
import Queue
from maze import Maze

MAZES = "./mazes/"

# maze constants to improve readability
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

def BFS(parsedMaze, timeseries, startingNode):
    solvedMaze = parsedMaze
    q = Queue.Queue()
    q.put(startingNode)
    startx = startingNode.coordinates['x']
    starty = startingNode.coordinates['y']

    while(not q.empty()):
        t = q.get()
        solvedMaze[t.coordinates['y']][t.coordinates['x']] = '~'
       # printMaze(solvedMaze)
        if t.end: # found solution
            solvedMaze[t.coordinates['y']][t.coordinates['x']] = '.'
            solvedMaze[starty][startx] = 'P'
            return solvedMaze
        else:
            t.addChildren(parsedMaze)
            for n in t.children:
                if n is not None:
                    posx = n.coordinates['x']
                    posy = n.coordinates['y']
                    if solvedMaze[posy][posx] != '~':
                        q.put(n)


    return False

def main():
    files = os.listdir(MAZES)

   # for f in files:
    m = Maze(MAZES + "big.maze")
    solved = m.solveUsing(BFS, True)

    if not solved:
        return "No solution"
    else:
        printMaze(solved)


def printMaze(maze):
    for row in maze:
        for elem in row:
            print elem,
        print '\n',

main()