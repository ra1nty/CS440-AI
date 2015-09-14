import sys
import os

class Maze:

    WALL = '%'
    GOAL = '.'
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

        for c in maze:
            if c != '\n':
                mazeRow.append(c)
            else:
                arrayMaze.append(mazeRow)
                mazeRow = list()

        return arrayMaze

    def solveUsing(self, method=None, timeseries=False):
        if method != None:
            method(self.parsedMaze, timeseries)
        else:
            return None

if __name__ == "__main__":
    Maze("./mazes/sample.maze")

