import sys
import os
from maze import Maze
import pdb
import Queue as q


MAZES = "./mazes/"

def ManhattanDist(current, end):
    return abs(end.coordinates['x']-current.coordinates['x'])+ abs(end.coordinates['y']-current.coordinates['y'])

def ASTAR(parsedMaze, timeseries, startingNode):
    frontier = q.PriorityQueue()    #initialize frontier queue
    frontier.put(0,startingNode)
    g = {}   #cost so far:(key: node, value: cost so far of node)
    path = {}   #remembers solution path (key: node, value: node before it)
    g[startingNode] = 0
    path[startingNode]=None

    while (not.frontier.empty()):
        curr = frontier.get()

            if curr == goal:
                    break

            curr.addChildren(parsedMaze)

            for next in curr.children:
                next_cost = cost_so_far[current]+1
                if next not in g or next_cost < g[next]:
                    g[next] = next_cost
                    cost = next_cost + ManhattanDist(next, next.end)
                    frontier.put(cost, next)
                    path[next] = curr

    curr.visitNode()
    curr = next
    while (not path[curr] == None):
        prev = path[curr]
        prev.visitNode()
        curr = prev
    

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