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
    expanded = 0

    while (not frontier.empty()):
        curr = frontier.get()
        expanded = expanded+1

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

    curr = next
    while (not path[curr] == None):
        prev = path[curr]
        parsedMaze[prev.coordinates['y']][prev.coordinates['x']] = '.'
        curr = prev
      
    print "Nodes expanded: %d", expanded
    print "Path cost of solution: %d", len(path)
      
    for row in parsedMaze:
            for elem in row:
                print elem,
            print '\n',


def main():
    argv = sys.argv

    m = Maze(MAZES + argv[1] + '.maze')
    solved = m.solveUsing(ASTAR, True, heuristic=None, comparisonFunc=None, costAssign=None)
        

if __name__ == "__main__":
    main()