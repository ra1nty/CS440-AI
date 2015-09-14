import sys
import os

class Maze:

    WALL = '%'
    ENDING = '.'
    STARTING = 'P'
    startingCoord = {}
    endingCoord = {}

    class searchNode:

        visited = False
        children = list()
        coordinates = dict(x=0, y=0)
        start = False
        end = False
        parent = None
        WALL = '%'
        GOAL = '.'
        currChild = 0

        def __init__(self, x, y, parent=None, start=False, end=False):
            self.coordinates['x'] = x
            self.coordinates['y'] = y
            self.start = start
            self.end = end
            self.parent = parent

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


        def addChildren(self, maze):
            # Right
            y = self.coordinates['y']
            x = self.coordinates['x']
            if maze[y][x + 1] != self.WALL:
                if maze[y][x + 1] == self.GOAL:
                    self.children.append(Maze.searchNode(y, x + 1, parent=self, end=True))
                else:
                    self.children.append(Maze.searchNode(y, x + 1, self))

            # Down
            elif maze[y + 1][x] != self.WALL:
                if maze[y + 1][x] == self.GOAL:
                    self.children.append(Maze.searchNode(y + 1, x, parent=self, end=True))
                else:
                    self.children.append(Maze.searchNode(y + 1, x, self))

            # Left
            elif maze[y][x - 1] != self.WALL:
                if maze[y][x - 1] == self.GOAL:
                    self.children.append(Maze.searchNode(y, x - 1, parent=self, end=True))
                else:
                    self.children.append(Maze.searchNode(y, x - 1, self))

            # Up
            elif maze[y - 1][x] != self.WALL:
                if maze[y - 1][x] == self.GOAL:
                    self.children.append(Maze.searchNode(y - 1, x, parent=self, end=True))
                else:
                    self.children.append(Maze.searchNode(y - 1, x, self))

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
                          self.searchNode(x=self.startingCoord['x'],
                                          y=self.startingCoord['y'],
                                          start=True))
        else:
            return None

if __name__ == "__main__":
    m = Maze("./mazes/big.maze")
    m.printMaze()


