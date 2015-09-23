import sys
import os
from Queue import PriorityQueue

class searchNode:

    WALL = '%'
    GOAL = '.'

    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    # Should probably use a set not a hash
    allNodes = dict()

    # Heuristic and heuristic comparison function for deciding the priority queue
    heuristic = None
    comparisonFunc = None

    # Shared queue and shared set of frontiers
    frontierQueue = PriorityQueue()
    frontier = dict()
    destination = dict()

    def __init__(self, y, x, parent=None, start=False, end=False, heuristic=None, comparisonFunc=None, dest=None, direction=None):
        self.coordinates = dict()
        self.coordinates['x'] = x
        self.coordinates['y'] = y
        self.start = start
        self.end = end
        self.parent = parent
        self.children = list()
        self.visited = False
        self.currChild = 0
        self.weight = 0
        self.g = 0
        self.h = 0
        self.f = 0
        self.destination = dest
        self.allNodes[str(self.coordinates)] = self
        self.heuristic = heuristic
        self.comparisonFunc = comparisonFunc
        self.currDirection = direction

        if parent is not None:
            self.heuristic = parent.heuristic
            self.comparisonFunc = parent.comparisonFunc
            self.destination = parent.destination

    def visitNode(self):        #marks node as visited
        self.visited = True

    def isEnding(self):     #returns the ending point
        return self.end

    def getNextChild(self):
        if self.currChild >= len(self.children):
            temp = None
        else:
            temp = self.children[self.currChild]
            self.currChild += 1
        return temp

    def getNextBestChildNode(self):
        bestHeuristic = 0
        bestChild = None

        for child in self.children:
            temp = self.heuristic(self.coordinates, self.destination)
            if self.comparisonFunc(temp, bestHeuristic):
                bestChild = child

        return bestChild

    def setHeuristic(self, heuristic, comparisonFunc):
        # Heuristic prototype
        # def heuristic(curr, end)
        # Curr format: { 'x': __, 'y': __ }

        self.heuristic = heuristic
        self.compare = comparisonFunc

    def hasMoreChildren(self):
        return self.currChild < len(self.children)

    def __eq__(self, coord):
        if coord is None:
            return False

        return (self.coordinates['x'] == coord['x'] and
                self.coordinates['y'] == coord['y'])

    def __ne__(self, coord):
        if coord is None:
            return False

        return (self.coordinates != coord)

    def __cmp__(self, other):
        if (self.heuristic is not None):
            return self.comparisonFunc(self.heuristic(self.coordinates, self.destination), self.heuristic(other.coordinates, self.destination))

    def getTraversal(self):
        traversal = list()
        currNode = self

        while (currNode is not None):
            traversal.append(currNode)
            currNode = currNode.parent

        return traversal

    def printNode(self):
        print "%s; visited %s" % (str(self.coordinates), self.visited)

    def nextBestNode(self):
        return self.frontierQueue.get()

    def addChildren(self, maze):
        # Right
        y = self.coordinates['y']
        x = self.coordinates['x']
        temp = None

        if str(dict(x=x+1, y=y)) in self.allNodes:
            if not self.allNodes[str(dict(x=x+1, y=y))].visited:
                temp = self.allNodes[str(dict(x=x+1, y=y))]
                self.children.append(temp)

            self.right = temp
        elif maze[y][x + 1] != self.WALL and self.parent != dict(x=x+1, y=y):
            if maze[y][x + 1] == self.GOAL:
                temp = searchNode(y, x + 1, parent=self, end=True, direction=self.RIGHT)
                self.children.append(temp)
            else:
                temp = searchNode(y, x + 1, parent=self, direction=self.RIGHT)
                self.children.append(temp)

            self.right = temp
        else:
            self.right = None

        # Down
        if str(dict(x=x, y=y+1)) in self.allNodes:
            if not self.allNodes[str(dict(x=x, y=y+1))].visited:
                temp = self.allNodes[str(dict(x=x, y=y+1))]
                self.children.append(temp)

            self.down = temp
        elif maze[y + 1][x] != self.WALL and self.parent != dict(x=x, y=y+1):
            if maze[y + 1][x] == self.GOAL:
                temp = searchNode(y + 1, x, parent=self, end=True, direction=self.DOWN)
                self.children.append(temp)
            else:
                temp = searchNode(y + 1, x, parent=self, direction=self.DOWN)
                self.children.append(temp)

            self.down = temp
        else:
            self.down = None

        # Left
        if str(dict(x=x-1, y=y)) in self.allNodes:
            if not self.allNodes[str(dict(x=x-1, y=y))].visited:
                temp = self.allNodes[str(dict(x=x-1, y=y))]
                self.children.append(temp)

            self.left = temp
        elif maze[y][x - 1] != self.WALL and self.parent != dict(x=x-1, y=y):
            if maze[y][x - 1] == self.GOAL:
                temp = searchNode(y, x - 1, parent=self, end=True, direction=self.LEFT)
                self.children.append(temp)
            else:
                temp = searchNode(y, x - 1, parent=self, direction=self.LEFT)
                self.children.append(temp)

            self.left = temp
        else:
            self.left = None

        # Up
        if str(dict(x=x, y=y-1)) in self.allNodes:
            if not self.allNodes[str(dict(x=x, y=y-1))].visited:
                temp = self.allNodes[str(dict(x=x, y=y-1))]
                self.children.append(temp)

            self.up = temp
        elif maze[y - 1][x] != self.WALL and self.parent != dict(x=x, y=y-1):
            if maze[y - 1][x] == self.GOAL:
                temp = searchNode(y - 1, x, parent=self, end=True, direction=self.UP)
                self.children.append(temp)
            else:
                temp = searchNode(y - 1, x, parent=self, direction=self.UP)
                self.children.append(temp)
        else:
            self.up = None

        if self.heuristic is not None:
            for child in self.children:
                if str(child.coordinates) not in self.frontier:
                    self.frontier[str(child.coordinates)] = child
                    self.frontierQueue.put(child)

class Maze:

    WALL = '%'
    ENDING = '.'
    STARTING = 'P'

    def __init__(self, filename):
        maze = self.__loadFile(filename)
        self.parsedMaze = self.__parseMaze(maze)

    def __loadFile(self, filename):
        with open(filename, 'r') as f:
            temp = f.read()

        return temp

    def __parseMaze(self, maze):
        arrayMaze = list()
        mazeRow = list()
        currX = 0
        currY = 0

        for c in maze:
            if c != '\n':
                if c == self.STARTING:
                    self.startingCoord = dict(x=currX, y=currY)
                elif c == self.ENDING:
                    self.endingCoord = dict(x=currX, y=currY)
                mazeRow.append(c)
                currX += 1
            else:
                arrayMaze.append(mazeRow)
                mazeRow = list()
                currX = 0
                currY += 1

        return arrayMaze

    def printMaze(self):
        for row in self.parsedMaze:
            for elem in row:
                print elem,
            print '\n',

        print "Starting (%d, %d)" % (self.startingCoord['x'], self.startingCoord['y'])
        print "Ending (%d, %d)" % (self.endingCoord['x'], self.endingCoord['y'])

    def solveUsing(self, method=None, timeseries=False, heuristic=None, comparisonFunc=None):
        if method != None:
            return method(self.parsedMaze,
                          timeseries,
                          searchNode(x=self.startingCoord['x'],
                                     y=self.startingCoord['y'],
                                     start=True,
                                     heuristic=heuristic,
                                     comparisonFunc=comparisonFunc,
                                     dest=self.endingCoord))
        else:
            return None

if __name__ == "__main__":
    m = Maze("./mazes/big.maze")
    m.printMaze()
