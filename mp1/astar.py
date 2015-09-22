import sys
import os
from maze import Maze
import pdb
import Queue as q


MAZES = "./mazes/"

def ASTAR(parsedMaze, timeseries, startingNode):
    frontier = q.PriorityQueue()    #initialize frontier queue
    frontier.put(0,startingNode)
    g = {}   #cost so far:(key: node, value: cost so far of node)
    path = {}   #remembers solution path (key: node, value: node before it)
    g[startingNode] = 0
    path[startingNode]=None

        while not frontier.empty():
            curr = frontier.get()
            if curr.isEnding:
                break


def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    solved = m.solveUsing(ASTAR, True)

    with open(argv[1] + '.out', 'w') as f:
        for frame in solved:
            f.write(str(frame))
            f.write('\n')

if __name__ == "__main__":
    main()