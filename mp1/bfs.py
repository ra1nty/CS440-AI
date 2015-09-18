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
        t.visitNode()
        solvedMaze[t.coordinates['y']][t.coordinates['x']] = '~'
        if t.end: # found solution
            solvedMaze[t.coordinates['y']][t.coordinates['x']] = '.'
            solvedMaze[starty][startx] = 'P'

            return solvedMaze
        else:
            t.addChildren(parsedMaze)
            for n in t.children:
                if n is not None and not n.visited:
                    q.put(n)


    return False

def main():
    files = os.listdir(MAZES)

   # for f in files:
    m = Maze(MAZES + "medium.maze")
    solved = m.solveUsing(BFS, True)

    if not solved:
        return "No solution"
    else:
         for row in solved:
            for elem in row:
                print elem,
            print '\n',



main()