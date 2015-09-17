import sys
import os

def makeSearchNode(x, y, parent=None, start=False, end=False):
    temp = searchNode(x=x, y=y, start=start, end=end, parent=parent)
    return temp

class searchNode:

    WALL = '%'
    GOAL = '.'

    def __init__(self, x, y, parent=None, start=False, end=False):
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

    def visitNode(self):
        self.visited = True

    def isEnding(self):
        return self.end

    def getNextChild(self):
        if self.currChild >= len(self.children):
            temp = None
        else:
            temp = self.children[self.currChild]
            self.currChild += 1
        return temp

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

    def printNode(self):
        print "%s; visited %s" % (str(self.coordinates), self.visited)

    def addChildren(self, maze):
        # Right
        y = self.coordinates['y']
        x = self.coordinates['x']

        if maze[y][x + 1] != self.WALL and self.parent != dict(x=x+1, y=y):
            if maze[y][x + 1] == self.GOAL:
                self.children.append(makeSearchNode(y, x + 1, parent=self, end=True))
            else:
                self.children.append(makeSearchNode(y, x + 1, parent=self))

        # Down
        if maze[y + 1][x] != self.WALL and self.parent != dict(x=x, y=y+1):
            if maze[y + 1][x] == self.GOAL:
                self.children.append(makeSearchNode(y + 1, x, parent=self, end=True))
            else:
                self.children.append(makeSearchNode(y + 1, x, parent=self))

        # Left
        if maze[y][x - 1] != self.WALL and self.parent != dict(x=x-1, y=y):
            if maze[y][x - 1] == self.GOAL:
                self.children.append(makeSearchNode(y, x - 1, parent=self, end=True))
            else:
                self.children.append(makeSearchNode(y, x - 1, parent=self))

        # Up
        if maze[y - 1][x] != self.WALL and self.parent != dict(x=x, y=y-1):
            if maze[y - 1][x] == self.GOAL:
                self.children.append(makeSearchNode(y - 1, x, parent=self, end=True))
            else:
                self.children.append(makeSearchNode(y - 1, x, parent=self))

class Maze:

    WALL = '%'
    ENDING = '.'
    STARTING = 'P'
    startingCoord = {}
    endingCoord = {}

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

    def solveUsing(self, method=None, timeseries=False):
        if method != None:
            return method(self.parsedMaze,
                          timeseries,
                          searchNode(x=self.startingCoord['x'],
                                     y=self.startingCoord['y'],
                                     start=True))
        else:
            return None

if __name__ == "__main__":
    m = Maze("./mazes/big.maze")
    m.printMaze()


