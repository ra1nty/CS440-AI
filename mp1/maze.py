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

        def __init__(self, x, y):
            self.x = x
            self.y = y


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
            method(self.parsedMaze, timeseries, self.getNextBranchs)
        else:
            return None

if __name__ == "__main__":
    m = Maze("./mazes/big.maze")
    m.printMaze()


